#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jorge Niedbalski R. <jnr@pyrosome.org>'

from fabric.api import task, run, sudo, settings, put
from fabric.context_managers import shell_env
from awsfabrictasks.decorators import ec2instance

import os

_HERE = os.path.abspath(os.path.dirname(__file__))


@task
@ec2instance(nametag='puppet_01')
def setup_master():
    modules = [
        ('https://github.com/armstrong/puppet-pip', 'pip'),
        ('https://github.com/puppetlabs/puppetlabs-vcsrepo',
         'puppetlabs-vcsrepo'),
        ('https://github.com/stankevich/puppet-python', 'python')
    ]

    sudo("apt-get update")
    sudo("apt-get -yyq install puppetmaster puppetmaster-common git-core puppet python-pip")
    sudo("echo '*' > /etc/puppet/autosign.conf")
 
    with settings(warn_only=True):
        for module in modules:
            (repo, name) = module
            sudo("git clone %s /etc/puppet/modules/%s" % (repo, name))

    manifest = os.path.join(_HERE, 'puppet', 'site.pp')
    put(manifest, '/etc/puppet/manifests/site.pp', use_sudo=True)

    sudo("/etc/init.d/puppetmaster restart")
    sudo("puppet apply /etc/puppet/manifests/site.pp")


from awsfabrictasks.ec2.tasks import *
from awsfabrictasks.regions import *
from awsfabrictasks.conf import *
