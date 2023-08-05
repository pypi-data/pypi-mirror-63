# Copyright (c) 2020 Mike Kinney

"""Common pytest code."""
import json
import pytest


@pytest.fixture
def mechcloudfile_one_entry():
    """Return one mechcloudfile entry."""
    return {
        'tophat': {
            'name': 'tophat',
            'hostname': 'tophat.example.com',
            'directory': '~/test1',
            'username': 'bob'
        }
    }


@pytest.fixture
def ssh_config():
    """Return one ssh_config."""
    return {
        "Host": "first",
        "User": "foo",
        "Port": "22",
        "UserKnownHostsFile": "/dev/null",
        "StrictHostKeyChecking": "no",
        "PasswordAuthentication": "no",
        "IdentityFile": 'blah',
        "IdentitiesOnly": "yes",
        "LogLevel": "FATAL",
    }


@pytest.fixture
def mechfile_one_entry():
    """Return one mechfile entry."""
    return {
        'first': {
            'name': 'first',
            'box': 'bento/ubuntu-18.04',
            'box_version': '201912.04.0'
        }
    }


@pytest.fixture
def mechfile_one_entry_virtualbox():
    """Return one mechfile entry."""
    return {
        'first': {
            'name': 'first',
            'box': 'bento/ubuntu-18.04',
            'box_version': '201912.04.0',
            'provider': 'virtualbox'
        }
    }


@pytest.fixture
def mechfile_one_entry_atari():
    """Return one mechfile entry."""
    return {
        'first': {
            'name': 'first',
            'box': 'bento/ubuntu-18.04',
            'box_version': '201912.04.0',
            'provider': 'atari'
        }
    }


@pytest.fixture
def mechfile_one_entry_without_box_version():
    """Return one mechfile entry."""
    return {
        'first': {
            'name': 'first',
            'box': 'bento/ubuntu-18.04'
        }
    }


@pytest.fixture
def mechfile_one_entry_with_file():
    """Return one mechfile entry."""
    return {
        'name': 'first',
        'box': 'bento/ubuntu-18.04',
        'box_version': '201912.04.0',
        'file': '/tmp/somefile.box'
    }


@pytest.fixture
def mechfile_one_entry_with_auth():
    """Return one mechfile entry with auth."""
    return {
        'first': {
            'name': 'first',
            'box': 'bento/ubuntu-18.04',
            'box_version': '201912.04.0',
            'auth': {
                'username': 'bob',
                'pub_key': 'some_pub_key_data'
            }
        }
    }


@pytest.fixture
def mechfile_one_entry_with_auth_and_mech_use():
    """Return one mechfile entry with auth that has mech_use."""
    return {
        'first': {
            'name': 'first',
            'box': 'bento/ubuntu-18.04',
            'box_version': '201912.04.0',
            'auth': {
                'username': 'bob',
                'mech_use': 'true',
                'pub_key': 'some_pub_key_data'
            }
        }
    }


@pytest.fixture
def mechfile_two_entries():
    """Return two mechfile entries."""
    return {
        'first': {
            'name': 'first',
            'box': 'bento/ubuntu-18.04',
            'box_version': '201912.04.0',
            'shared_folders': [
                {
                    "host_path": ".",
                    "share_name": "mech"
                }
            ],
            'url':
            'https://vagrantcloud.com/bento/boxes/ubuntu-18.04/'
            'versions/201912.04.0/providers/vmware_desktop.box'
        },
        'second': {
            'name': 'second',
            'box': 'bento/ubuntu-18.04',
            'box_version': '201912.04.0',
            'url':
            'https://vagrantcloud.com/bento/boxes/ubuntu-18.04/'
            'versions/201912.04.0/providers/vmware_desktop.box'
        }
    }


CATALOG = """{
    "description": "foo",
    "short_description": "foo",
    "name": "bento/ubuntu-18.04",
    "versions": [
        {
            "version": "aaa",
            "status": "active",
            "description_html": "foo",
            "description_markdown": "foo",
            "providers": [
                {
                    "name": "vmware_desktop",
                    "url": "https://vagrantcloud.com/bento/boxes/ubuntu-18.04/\
versions/aaa/providers/vmware_desktop.box",
                    "checksum": null,
                    "checksum_type": null
                }
            ]
        }
    ]
}"""
@pytest.fixture
def catalog():
    """Return a catalog."""
    return CATALOG


@pytest.fixture
def shell_provision_config():
    return [
        {
            "type": "shell",
            "path": "file1.sh",
            "args": [
                "a=1",
                "b=true",
            ],
        },
        {
            "type": "shell",
            "inline": "echo hello from inline"
        },
        {
            "type": "shell",
            "inline": "echo hello2 from inline",
            "args": []
        }
    ]


@pytest.fixture
def pyinfra_provision_config():
    return [
        {
            "type": "pyinfra",
            "path": "file1.py",
            "args": [
                "sudo=True",
                "b=1",
            ],
        },
        {
            "type": "pyinfra",
            "path": "file2.py",
        }
    ]


@pytest.fixture
def pyinfra_provision_http_config():
    return [
        {
            "type": "pyinfra",
            "path": "https://github.com/Fizzadar/pyinfra/blob/"
            "master/examples/docker_ce.py",
            "args": [
                "sudo=True"
            ],
        }
    ]


@pytest.fixture
def catalog_as_json():
    """Return a catalog as json."""
    return json.loads(CATALOG)


class Helpers:
    @staticmethod
    def get_mock_data_written(a_mock):
        """Helper function to get the data written to a mocked file."""
        written = ''
        for call in a_mock.mock_calls:
            tmp = '{}'.format(call)
            if tmp.startswith('call().write('):
                line = tmp.replace("call().write('", '')
                line = line.replace("')", '')
                line = line.replace("\\n", '\n')
                written += line
        return written


@pytest.fixture
def helpers():
    """Helper functions for testing."""
    return Helpers
