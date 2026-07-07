from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class PluginInfo:
    category: str
    name: str
    version: str
    description: str
    path: str
    instance: Optional[Any] = None


class PluginManager:
    """Simple local plugin loader for exchanges, strategies, indicators, and reports."""

    def __init__(self, plugin_root: str = "plugins"):
        self.plugin_root = Path(plugin_root)
        self.plugins: Dict[str, List[PluginInfo]] = {
            "exchanges": [],
            "strategies": [],
            "indicators": [],
            "reports": [],
        }

    def scan(self) -> Dict[str, List[PluginInfo]]:
        self.clear()
        for category in self.plugins.keys():
            category_dir = self.plugin_root / category
            if not category_dir.exists():
                continue
            for plugin_dir in category_dir.iterdir():
                if not plugin_dir.is_dir():
                    continue
                plugin_file = plugin_dir / "plugin.py"
                if not plugin_file.exists():
                    continue
                info = self._load_plugin(category, plugin_dir.name, plugin_file)
                if info:
                    self.plugins[category].append(info)
        return self.plugins

    def clear(self) -> None:
        for category in self.plugins:
            self.plugins[category] = []

    def get_plugins(self, category: Optional[str] = None):
        if category:
            return self.plugins.get(category, [])
        return self.plugins

    def names(self, category: str) -> List[str]:
        return [plugin.name for plugin in self.plugins.get(category, [])]

    def get_instance(self, category: str, name: str) -> Optional[Any]:
        for plugin in self.plugins.get(category, []):
            if plugin.name == name:
                return plugin.instance
        return None

    def _load_plugin(self, category: str, folder_name: str, plugin_file: Path) -> Optional[PluginInfo]:
        module_name = f"daejungnext_plugin_{category}_{folder_name}"
        spec = importlib.util.spec_from_file_location(module_name, plugin_file)
        if not spec or not spec.loader:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        plugin_class = getattr(module, "Plugin", None)
        if plugin_class is None:
            return None
        instance = plugin_class()
        meta = getattr(instance, "metadata", lambda: {})()
        return PluginInfo(
            category=category,
            name=meta.get("name", folder_name),
            version=meta.get("version", "0.1.0"),
            description=meta.get("description", ""),
            path=str(plugin_file),
            instance=instance,
        )
