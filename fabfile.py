#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from fabric.api import sudo, env, settings, cd, shell_env


env.use_ssh_config = True
if not env.hosts:
    env.hosts = ["1ch-dev"]

folder = "/srv/covid-api-tracks"
venv_folder = "/srv/.pyenv/versions/covid-ap-tracks"
git_repo = "git@git.1check.in:covidapp/covidapi-tracks.git"
www_user = "app"


def deploy():
    with cd(folder), settings(
        sudo_user=www_user,
        sudo_prefix="sudo -H -E "
    ), shell_env(
        SIMPLE_SETTINGS="covid_api.confg,instance.staging",
        VIRTUAL_ENV=venv_folder,
        PATH="{}:$PATH".format(os.path.join(venv_folder, 'bin'))
    ):
        sudo('git checkout dev')
        sudo('git pull')
        sudo('{}/bin/pip install -r requirements.txt'.format(venv_folder))
        sudo('make upgrade')

    restart('covid-api-tracks')


def restart(process):
    sudo("supervisorctl restart %s" % process)
