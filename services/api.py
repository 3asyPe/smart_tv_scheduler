import random

from enums import TVStatus


def get_tv_status():
    return random.choice([status.value for status in TVStatus])
