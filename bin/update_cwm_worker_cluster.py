#!/usr/bin/env python3

import sys
import datetime
import subprocess
from ruamel import yaml


def get_latest_version(repo_index, chart_name):
    latest_entry_datetime = None
    latest_entry_version = None
    for entry in repo_index['entries'][chart_name]:
        if entry['version'].startswith('0.0.0-'):
            entry_datetime = datetime.datetime.strptime(entry['version'].replace('0.0.0-', ''), '%Y%m%dT%H%M%S')
            if latest_entry_datetime is None or latest_entry_datetime < entry_datetime:
                latest_entry_datetime = entry_datetime
                latest_entry_version = entry['version']
    assert latest_entry_version, 'failed to find latest version ({})'.format(chart_name)
    return latest_entry_version


def main(commit_msg):
    commit_msg = commit_msg.strip()
    update_repo = None
    if commit_msg == "automatic update of cwm-worker-ingress":
        update_repo = "cwm-worker-ingress"
    elif commit_msg == "automatic update of cwm-worker-operator":
        update_repo = "cwm-worker-operator"
    if update_repo:
        print("Updating cwm-worker-cluster chart dependency of {}".format(update_repo))
        with open("{}/index.yaml".format(update_repo)) as f:
            index = yaml.safe_load(f)
        latest_version = get_latest_version(index, update_repo)
        print("latest version: {}".format(latest_version))
        filename = "clusters/{}.latest-chart-version".format(update_repo)
        with open(filename, "w") as f:
            f.write(latest_version)
        subprocess.check_call(["git", "add", filename])
        subprocess.check_call(["git", "commit", "-m", "automatic update of {} latest-chart-version".format(update_repo)])
        subprocess.check_call(["git", "push", "origin", "master"])


if __name__ == "__main__":
    main(*sys.argv[1:])
