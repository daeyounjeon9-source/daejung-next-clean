from core.update_manager import UpdateManager


def main():
    manager = UpdateManager()
    version = manager.load_version()
    packages = manager.check_local_updates()
    print("DAEJUNGNEXT Update Checker")
    print("현재 버전:", version.get("version"))
    print("채널:", version.get("channel"))
    print("업데이트 패키지 수:", len(packages))
    for item in packages:
        print("-", item["name"], item["modified"])


if __name__ == "__main__":
    main()
