from core.update_manager import UpdateManager


if __name__ == "__main__":
    manager = UpdateManager()
    result = manager.simulate_update()
    print(result["message"])
    print("백업 위치:", result["backup_path"])
    print("발견된 업데이트 패키지:", result["packages_found"])
