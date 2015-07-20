#!/usr/bin/env python3

import click
import json
import subprocess

from clickclick import Action


@click.command()
@click.argument('stack_name')
@click.argument('port', type=int)
@click.argument('jump_host')
@click.option('--region')
def cli(stack_name, port, jump_host, region):
    out = subprocess.check_output(['senza', 'instances', '--output=json', stack_name])
    data = json.loads(out.decode('utf-8'))

    opts = []
    endpoints = []
    for row in data:
        if row['state'] == 'RUNNING':
            ip = row['private_ip']
            with Action('Adding IP {}..'.format(ip)):
                subprocess.call(['sudo', 'ip', 'a', 'a', 'dev', 'lo', ip])
                hostname = 'ip-{}.{}.compute.internal'.format(ip.replace('.', '-'), region)
                subprocess.call(['sudo', 'su', '-c', 'echo "{} {}" >> /etc/hosts'.format(ip, hostname)])
                opts += ['-L', '{}:{}:{}:{}'.format(ip, port, ip, port)]
                endpoints.append('{}:{}'.format(ip, port))

    if not endpoints:
        raise click.UsageError('No instances for Senza stack "{}" found.'.format(stack_name))

    click.secho('Endpoints: {}'.format(','.join(endpoints)), bold=True, fg='blue')

    click.secho('Starting SSH tunnels..', bold=True)
    subprocess.call(['ssh'] + opts + [jump_host, 'while true; do echo -n .; sleep 60; done'])

if __name__ == '__main__':
    cli()
