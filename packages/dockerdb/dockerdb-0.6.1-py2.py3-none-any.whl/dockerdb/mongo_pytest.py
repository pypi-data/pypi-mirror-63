from __future__ import absolute_import
import os
import shutil
import subprocess
import logging

import pytest
import dockerdb.mongo


CONTAINER_CACHE = {}

LOG = logging.getLogger(__name__)


def insert_data(client, data):
    for db in data:
        for collection in data[db]:
            entries = data[db][collection]
            re = client[db][collection].insert_many(entries)


def mongorestore(service, restore):
    dst = os.path.join(service.share, 'dump')
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(restore, dst)
    command = ['mongorestore', dst]
    exit_code, output = service.container.exec_run(command)

    if exit_code != 0:
        LOG.error(output.decode('utf-8'))

        raise subprocess.CalledProcessError(exit_code, command, output)


def get_service(version):
    service = CONTAINER_CACHE[version]
    service.wait()
    service.factory_reset()
    return service


def ensure_service(version, replicaset, port, client_args):
    if version not in CONTAINER_CACHE:
        CONTAINER_CACHE[version] = dockerdb.mongo.Mongo(
            version, wait=False, replicaset=replicaset, exposed_port=port,
            client_args=client_args)


def mongo_fixture(scope='function', versions=['latest'], data=None,
                  restore=None, reuse=True, replicaset=None, port=27017,
                  client_args=None):
    """create ficture for py.test

    Attributes:
        scope (str): py.test scope for this fixture
        versions (list): mongodb versions that should be tested
        data (dict): A dict containing data to be inserted into the database
            before the test.  The structure must be:
            {'db': {
                'collection': [
                    {'document_data': True},
                    {'another': 'document'},
                    ...
                ]
            }}

        restore (str): path to directory containing a mongo dump
        reuse (bool): wether to reuse containers or create a new container
            for every requested injection
        client_args(dict): arguments that get passed to the pymongo client

    """

    # parallelized start of different versions
    if reuse:
        for version in versions:
            ensure_service(version, replicaset, port, client_args)

    @pytest.fixture(scope=scope,  params=versions)
    def mongo(request):
        if reuse:
            service = get_service(request.param)
        else:
            service = dockerdb.service.Mongo(request.param, wait=True,
                                             replicaset=replicaset,
                                             exposed_port=port,
                                             client_args=client_args)

        client = service.pymongo_client()
        service.wait()

        if data:
            insert_data(client, data)

        if restore:
            mongorestore(service, restore)

        yield service

        if not reuse:
            service.remove()

    return mongo
