from __future__ import annotations

import json
import shutil
from pathlib import Path
from datetime import datetime


class ProjectManager:
    """Multi-project manager for DAEJUNG NEXT."""

    def __init__(self, root_dir: str | Path = "projects"):
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self.current_file = Path("data/projects/current_project.json")
        self.current_file.parent.mkdir(parents=True, exist_ok=True)
        self.ensure_default_project()

    def ensure_default_project(self) -> None:
        if not (self.root_dir / "DEFAULT").exists():
            self.create_project("DEFAULT", "기본 프로젝트")
        if not self.current_file.exists():
            self.set_current_project("DEFAULT")

    def list_projects(self) -> list[str]:
        return sorted([p.name for p in self.root_dir.iterdir() if p.is_dir()])

    def create_project(self, name: str, description: str = "") -> Path:
        safe_name = self._safe_name(name)
        if not safe_name:
            raise ValueError("프로젝트명이 비어 있습니다.")

        project_dir = self.root_dir / safe_name
        project_dir.mkdir(parents=True, exist_ok=True)

        for sub in ["config", "logs", "results", "backups", "runtime"]:
            (project_dir / sub).mkdir(parents=True, exist_ok=True)

        config_path = project_dir / "config" / "project.json"
        if not config_path.exists():
            config = {
                "project_name": safe_name,
                "description": description,
                "created_at": datetime.now().isoformat(timespec="seconds"),
                "updated_at": datetime.now().isoformat(timespec="seconds"),
                "exchange": "",
                "strategy": "",
                "symbol": "",
                "simulation_mode": True,
            }
            config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

        return project_dir

    def delete_project(self, name: str) -> bool:
        safe_name = self._safe_name(name)
        if safe_name == "DEFAULT":
            raise ValueError("DEFAULT 프로젝트는 삭제할 수 없습니다.")
        project_dir = self.root_dir / safe_name
        if project_dir.exists():
            shutil.rmtree(project_dir)
            if self.get_current_project() == safe_name:
                self.set_current_project("DEFAULT")
            return True
        return False

    def copy_project(self, source: str, target: str) -> Path:
        source_name = self._safe_name(source)
        target_name = self._safe_name(target)
        source_dir = self.root_dir / source_name
        target_dir = self.root_dir / target_name

        if not source_dir.exists():
            raise FileNotFoundError(f"원본 프로젝트가 없습니다: {source_name}")
        if target_dir.exists():
            raise FileExistsError(f"대상 프로젝트가 이미 있습니다: {target_name}")

        shutil.copytree(source_dir, target_dir)
        config_path = target_dir / "config" / "project.json"
        if config_path.exists():
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["project_name"] = target_name
            config["updated_at"] = datetime.now().isoformat(timespec="seconds")
            config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
        return target_dir

    def set_current_project(self, name: str) -> None:
        safe_name = self._safe_name(name)
        if not (self.root_dir / safe_name).exists():
            raise FileNotFoundError(f"프로젝트가 없습니다: {safe_name}")
        self.current_file.write_text(
            json.dumps({"current_project": safe_name}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def get_current_project(self) -> str:
        if not self.current_file.exists():
            return "DEFAULT"
        data = json.loads(self.current_file.read_text(encoding="utf-8"))
        return data.get("current_project", "DEFAULT")

    def get_project_config_path(self, name: str | None = None) -> Path:
        project = self._safe_name(name or self.get_current_project())
        return self.root_dir / project / "config" / "project.json"

    def load_project_config(self, name: str | None = None) -> dict:
        path = self.get_project_config_path(name)
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def save_project_config(self, config: dict, name: str | None = None) -> Path:
        project = self._safe_name(name or config.get("project_name") or self.get_current_project())
        self.create_project(project, config.get("description", ""))
        config["project_name"] = project
        config["updated_at"] = datetime.now().isoformat(timespec="seconds")
        path = self.get_project_config_path(project)
        path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def backup_project(self, name: str | None = None) -> Path:
        project = self._safe_name(name or self.get_current_project())
        project_dir = self.root_dir / project
        if not project_dir.exists():
            raise FileNotFoundError(project)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_base = project_dir / "backups" / f"{project}_backup_{timestamp}"
        archive = shutil.make_archive(str(backup_base), "zip", root_dir=project_dir)
        return Path(archive)

    @staticmethod
    def _safe_name(name: str) -> str:
        return "".join(ch for ch in str(name).strip().replace(" ", "_") if ch.isalnum() or ch in "_-").upper()
