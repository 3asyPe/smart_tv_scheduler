def analytics():
    print("Running analytics...")


def check_for_software_updates():
    print("Checking for software updates...")


def launch_application(name: str):
    print(f"Launching {name}...")


TASKS = {
    "analytics": analytics,
    "check_for_software_updates": check_for_software_updates,
    "launch_application": launch_application,
}
