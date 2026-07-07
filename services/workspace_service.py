from __future__ import annotations

from core.project_manager import ProjectManager


class WorkspaceService:
    """Connects selected project workspace to app-level services."""

    def __init__(self):
        self.project_manager = ProjectManager()

    def get_workspace_status(self) -> dict:
        current = self.project_manager.get_current_project()
        projects = self.project_manager.list_projects()
        config = self.project_manager.load_project_config(current)
        return {
            "current_project": current,
            "project_count": len(projects),
            "projects": projects,
            "config": config,
        }

    def switch_project(self, name: str) -> dict:
        self.project_manager.set_current_project(name)
        return self.get_workspace_status()

    def create_project(self, name: str, description: str = "") -> dict:
        self.project_manager.create_project(name, description)
        self.project_manager.set_current_project(name)
        return self.get_workspace_status()

    def backup_current_project(self):
        return self.project_manager.backup_project()
