from logging import getLogger


logger = getLogger(__name__)


def analytics():
    logger.info("Running analytics...")


def check_for_software_updates():
    logger.info("Checking for software updates...")


def launch_application(name: str):
    logger.info(f"Launching {name}...")


TASKS = {
    "analytics": analytics,
    "check_for_software_updates": check_for_software_updates,
    "launch_application": launch_application,
}
