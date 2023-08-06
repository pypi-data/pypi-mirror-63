#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Libraries
import appdirs
import os
import requests
import click
import pyperclip
import json

# Variables
APPNAME = "transfersh"
APPAUTHOR = "orangemax"
CONF_FILE = 'config.json'


@click.group()
def transfersh_cli():
    pass


@click.command()
def config():
    filename = os.path.join(appdirs.user_config_dir(APPNAME, APPAUTHOR), CONF_FILE)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    transfersh_url = click.prompt('Enter your transfer sh path:')
    data = {'transfershUrl': transfersh_url}
    with open(os.path.join(appdirs.user_config_dir(APPNAME, APPAUTHOR), CONF_FILE), 'w') as conf:
        json.dump(data, conf)
    click.echo('Transfersh is configured!')


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-m', '--mark', is_flag=True)
def push(filename, mark):
    """ Program that uploads a file to Transfer.sh """
    try:
        with open(os.path.join(appdirs.user_config_dir(APPNAME, APPAUTHOR), CONF_FILE), 'r') as conf:
            config = json.load(conf)
    except:
        click.echo('Transfersh is not configured.')
        return

    try:
        # Open file
        with open(filename, 'rb') as data:
            click.echo('Uploading file')
            # Upload file
            if mark:
                filename = 'tsh_{}'.format(filename)
            r = requests.put('{}/{}'.format(config['transfershUrl'], filename), data=data)
            # Shows route to download
            download_url = r.text
            click.echo(f'Download from here: {download_url}')
            # Copy route to clipboard
            pyperclip.copy(download_url)
            click.echo(f'It has also been copied to the clipboard!')
    except:
        click.echo('Something has failed. The file could not be uploaded.')


transfersh_cli.add_command(config)
transfersh_cli.add_command(push)

transfersh_cli()
