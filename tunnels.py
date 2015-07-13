#!/usr/bin/env python3

import click
import json
import subprocess
import sys

from clickclick import Action

stack_name = sys.argv[1]
port = int(sys.argv[2])
jump_host = sys.argv[3]

out = subprocess.check_output(['senza', 'instances', '--output=json', stack_name])
data = json.loads(out.decode('utf-8'))

opts = []
for row in data:
    ip = row['private_ip']
    with Action('Adding IP {}..'.format(ip)):
        subprocess.call(['sudo', 'ip', 'a', 'a', 'dev', 'lo', ip])
        opts += ['-L', '{}:{}:{}:{}'.format(ip, port, ip, port)]

click.secho('Starting SSH tunnels..', bold=True)
subprocess.call(['ssh'] + opts + [jump_host, 'while true; do echo -n .; sleep 60; done'])
