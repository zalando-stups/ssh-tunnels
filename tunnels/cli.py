#!/usr/bin/env python3

import click
import json
import subprocess
import sys

from clickclick import Action

if sys.platform == 'darwin':
    add_if = lambda ip: ['sudo', 'ifconfig', 'lo0', 'alias', ip]
    add_hosts = lambda ip, hostname: ['sudo', 'su', 'root', '-c', 'echo "{} {}" >> /etc/hosts'.format(ip, hostname)]
else:
    add_if = lambda ip: ['sudo', 'ip', 'a', 'a', 'dev', 'lo', ip]
    add_hosts = lambda ip, hostname: ['sudo', 'su', '-c', 'echo "{} {}" >> /etc/hosts'.format(ip, hostname)]


def parse_ports(s):
    """Allows for input of multiple ports such as '8080,8090-8096,9000-9010'.
    """
    ranges = (x.split("-") for x in s.split(","))
    return [i for r in ranges for i in range(int(r[0]), int(r[-1]) + 1)]


@click.command()
@click.argument('stack_name')
@click.argument('ports')
@click.argument('jump_host')
@click.option('--region')
@click.option('-U', '--user')
def cli(stack_name, ports, jump_host, region, user):
    try:
        portlist = parse_ports(ports)
    except ValueError:
        raise click.UsageError('Could not parse ports: ' + ports)

    senza_cmd = ['senza', 'instances', '--output=json', stack_name]
    if region:
        senza_cmd.append('--region=' + region)
    out = subprocess.check_output(senza_cmd)
    data = json.loads(out.decode('utf-8'))

    opts = []
    endpoints = []
    for row in data:
        if row['state'] == 'RUNNING':
            ip = row['private_ip']
            with Action('Adding IP {}..'.format(ip)):
                subprocess.call(add_if(ip))
                hostname = 'ip-{}.{}.compute.internal'.format(ip.replace('.', '-'), region)
                subprocess.call(add_hosts(ip, hostname))
                for port in portlist:
                    opts += ['-L', '{}:{}:{}:{}'.format(ip, port, ip, port)]
                    endpoints.append('{}:{}'.format(ip, port))

    if not endpoints:
        raise click.UsageError('No instances for Senza stack "{}" found.'.format(stack_name))

    click.secho('Endpoints: {}'.format(','.join(endpoints)), bold=True, fg='blue')

    click.secho('Starting SSH tunnels..', bold=True)
    if user:
        ssh_connect = user + '@' + jump_host
    else:
        ssh_connect = jump_host
    subprocess.call(['ssh'] + opts + [ssh_connect, 'while true; do echo -n .; sleep 60; done'])


if __name__ == '__main__':
    cli()
