from __future__ import annotations

try:
    from PySide6.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
        QListWidget, QTextEdit, QMessageBox, QGroupBox
    )
except Exception:
    pass

from services.workspace_service import WorkspaceService


class ProjectSelectorPage(QWidget):
    """Sprint 9 - Multi project selector page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.workspace = WorkspaceService()
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = QHBoxLayout(self)

        left = QGroupBox("프로젝트 목록")
        left_layout = QVBoxLayout(left)
        self.project_list = QListWidget()
        self.project_list.itemClicked.connect(self.select_project)
        left_layout.addWidget(self.project_list)

        btn_refresh = QPushButton("새로고침")
        btn_switch = QPushButton("선택 프로젝트 적용")
        btn_backup = QPushButton("현재 프로젝트 백업")
        btn_refresh.clicked.connect(self.refresh)
        btn_switch.clicked.connect(self.apply_selected)
        btn_backup.clicked.connect(self.backup_project)
        left_layout.addWidget(btn_refresh)
        left_layout.addWidget(btn_switch)
        left_layout.addWidget(btn_backup)

        right = QGroupBox("프로젝트 생성 / 상태")
        right_layout = QVBoxLayout(right)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("예: BTC_AUTO")
        self.desc_edit = QTextEdit()
        self.desc_edit.setPlaceholderText("프로젝트 설명")
        self.desc_edit.setFixedHeight(80)

        btn_create = QPushButton("새 프로젝트 생성")
        btn_create.clicked.connect(self.create_project)

        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)

        right_layout.addWidget(QLabel("프로젝트명"))
        right_layout.addWidget(self.name_edit)
        right_layout.addWidget(QLabel("설명"))
        right_layout.addWidget(self.desc_edit)
        right_layout.addWidget(btn_create)
        right_layout.addWidget(QLabel("현재 상태"))
        right_layout.addWidget(self.status_text)

        root.addWidget(left, 1)
        root.addWidget(right, 2)

    def refresh(self):
        self.project_list.clear()
        status = self.workspace.get_workspace_status()
        current = status["current_project"]
        for name in status["projects"]:
            label = f"{name}  ← 현재" if name == current else name
            self.project_list.addItem(label)
        self.status_text.setPlainText(
            f"현재 프로젝트: {current}\n"
            f"프로젝트 수: {status['project_count']}\n"
            f"목록: {', '.join(status['projects'])}"
        )

    def selected_name(self) -> str:
        item = self.project_list.currentItem()
        if not item:
            return ""
        return item.text().replace("← 현재", "").strip()

    def select_project(self, item):
        name = item.text().replace("← 현재", "").strip()
        self.name_edit.setText(name)

    def apply_selected(self):
        name = self.selected_name()
        if not name:
            return
        self.workspace.switch_project(name)
        self.refresh()
        QMessageBox.information(self, "프로젝트 변경", f"현재 프로젝트: {name}")

    def create_project(self):
        name = self.name_edit.text().strip()
        desc = self.desc_edit.toPlainText().strip()
        if not name:
            QMessageBox.warning(self, "확인", "프로젝트명을 입력하세요.")
            return
        self.workspace.create_project(name, desc)
        self.refresh()
        QMessageBox.information(self, "생성 완료", f"프로젝트 생성: {name}")

    def backup_project(self):
        path = self.workspace.backup_current_project()
        QMessageBox.information(self, "백업 완료", f"백업 파일:\n{path}")
