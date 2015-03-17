# Copyright (C) 2014 Universidad Politecnica de Madrid
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

import fiwareclient
import horizon
import migration
import keystone

from conf import settings

from fabric.api import local

def migration_populate(keystone_path=settings.KEYSTONE_ROOT,
                       internal_address=settings.CONTROLLER_INTERNAL_ADDRESS,
                       public_address=settings.CONTROLLER_PUBLIC_ADDRESS,
                       admin_address=settings.CONTROLLER_ADMIN_ADDRESS):
    """Populates the database with migration specifics from the old idm."""
    migration.populate(keystone_path, internal_address, public_address,
        admin_address)


def deploy(dev=False):
    """Fully installs the IdM."""
    # TODO(garcianavalon) PARAMETERS!!!
    set_up(dev=dev)
    keystone_deploy(dev=dev)
    horizon_deploy(dev=dev)
    print 'IdM successfully deployed! :)'

def set_up(dev=False):
    """Install system and python dependencies."""
    _install_dependencies()
    fiwareclient_install(dev=dev)

def _install_dependencies():
    local('{command} {dependencies}').format(
        command=settings.UBUNTU_DEPENDENCIES['install_command'],
        dependencies=' '.join(settings.UBUNTU_DEPENDENCIES['dependencies']))
    print 'Dependencies correctly installed'

def fiwareclient_install(fiwareclient_path=settings.FIWARECLIENT_ROOT,
                         dev=False):
    _install_dependencies()
    fiwareclient.install(fiwareclient_path, dev)

# HORIZON
def horizon_deploy(dev=False):
    horizon.deploy(dev)

def horizon_install(horizon_path=settings.HORIZON_ROOT,
                    fiwareclient_path=settings.FIWARECLIENT_ROOT,
                    dev=False):
    _install_dependencies()
    horizon.install(horizon_path, fiwareclient_path, dev)


def horizon_dev_server(address=settings.HORIZON_DEV_ADDRESS,
                       horizon_path=settings.HORIZON_ROOT):
    horizon.dev_server(horizon_path, address)

# KEYSTONE
def keystone_deploy(dev=False):
    keystone.deploy(dev)

def keystone_install(keystone_path=settings.KEYSTONE_ROOT,
                     dev=False):
    _install_dependencies()
    keystone.install(keystone_path, dev)

def keystone_database_create(keystone_path=settings.KEYSTONE_ROOT, verbose=True):
    keystone.database_create(keystone_path, verbose)

def keystone_service_start():
    keystone.service_start()

def keystone_service_stop():
    keystone.service_stop()

def keystone_service_create(absolute_keystone_path=None):
    if not absolute_keystone_path:
        absolute_keystone_path = os.getcwd() + '/' + settings.KEYSTONE_ROOT
    keystone.service_create(absolute_keystone_path)

def keystone_database_delete(keystone_path=settings.KEYSTONE_ROOT,
                             keystone_db=settings.KEYSTONE_DEV_DATABASE):
    db_path = keystone_path + keystone_db
    keystone.database_delete(db_path)

def keystone_database_populate(keystone_path=settings.KEYSTONE_ROOT,
                           internal_address=settings.CONTROLLER_INTERNAL_ADDRESS,
                           public_address=settings.CONTROLLER_PUBLIC_ADDRESS,
                           admin_address=settings.CONTROLLER_ADMIN_ADDRESS):

    keystone.database_populate(keystone_path, internal_address,
                           public_address, admin_address)

def keystone_test_data(keystone_path=settings.KEYSTONE_ROOT):
    keystone.test_data(keystone_path)

def keystone_dev_server(keystone_path=settings.KEYSTONE_ROOT):
    keystone.dev_server(keystone_path)

def keystone_database_reset(keystone_path=settings.KEYSTONE_ROOT):
    """Deletes keystone's database and create a new one, populated with
    the base data needed by the IdM. Requires a keystone instance running.
    """
    keystone_database_delete(keystone_path=keystone_path)
    keystone_database_create(keystone_path=keystone_path)
    keystone_database_populate(keystone_path=keystone_path)
