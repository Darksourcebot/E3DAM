#
# Copyright (C) 2021-2022 by TeamElNqYb@Github, < https://github.com/TeamElNqYb >.
#
# This file is part of < https://github.com/TeamElNqYb/ElNqYbMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamElNqYb/ElNqYbMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import time

import psutil

from ElNqYbMusic.misc import _boot_

from .formatters import get_readable_time


async def bot_sys_stats():
    bot_uptime = int(time.time() - _boot_)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    UP = f"{get_readable_time((bot_uptime))}"
    CPU = f"{cpu}%"
    RAM = f"{mem}%"
    DISK = f"{disk}%"
    return UP, CPU, RAM, DISK
