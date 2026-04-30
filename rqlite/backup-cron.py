#!/usr/bin/env python3

import requests
import pathlib
import datetime

DEFAULT_BACKUP_NAME = "rqlite.backup.sqlite3"


def main() -> None:
    home_dir = str(pathlib.Path.home())
    rqlite_service_url = "http://10.10.1.41:4001/db/backup"
    backup_file = home_dir + "/" + DEFAULT_BACKUP_NAME

    response = requests.get(rqlite_service_url, timeout=60)
    response.raise_for_status()

    with open(backup_file, "wb") as f:
        f.write(response.content)

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response_time = response.elapsed.total_seconds()

    print(f'[{time_now}] {rqlite_service_url} took {response_time} secs')


main()
