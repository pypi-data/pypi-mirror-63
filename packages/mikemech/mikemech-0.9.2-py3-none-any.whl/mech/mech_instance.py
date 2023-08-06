# -*- coding: utf-8 -*-
#
# Copyright (c) 2016-2017 Kevin Chung
# Copyright (c) 2018 German Mendez Bravo (Kronuz)
# Copyright (c) 2020 Mike Kinney
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
"""MechInstance class"""

from __future__ import print_function, absolute_import

import os
import re
import sys
import logging

import click

from . import utils
from .vmrun import VMrun
from .vbm import VBoxManage

LOGGER = logging.getLogger('mech')

DEFAULT_USER = 'vagrant'
DEFAULT_PASSWORD = 'vagrant'
INSECURE_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzI
w+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoP
kcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2
hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NO
Td0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcW
yLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQIBIwKCAQEA4iqWPJXtzZA68mKd
ELs4jJsdyky+ewdZeNds5tjcnHU5zUYE25K+ffJED9qUWICcLZDc81TGWjHyAqD1
Bw7XpgUwFgeUJwUlzQurAv+/ySnxiwuaGJfhFM1CaQHzfXphgVml+fZUvnJUTvzf
TK2Lg6EdbUE9TarUlBf/xPfuEhMSlIE5keb/Zz3/LUlRg8yDqz5w+QWVJ4utnKnK
iqwZN0mwpwU7YSyJhlT4YV1F3n4YjLswM5wJs2oqm0jssQu/BT0tyEXNDYBLEF4A
sClaWuSJ2kjq7KhrrYXzagqhnSei9ODYFShJu8UWVec3Ihb5ZXlzO6vdNQ1J9Xsf
4m+2ywKBgQD6qFxx/Rv9CNN96l/4rb14HKirC2o/orApiHmHDsURs5rUKDx0f9iP
cXN7S1uePXuJRK/5hsubaOCx3Owd2u9gD6Oq0CsMkE4CUSiJcYrMANtx54cGH7Rk
EjFZxK8xAv1ldELEyxrFqkbE4BKd8QOt414qjvTGyAK+OLD3M2QdCQKBgQDtx8pN
CAxR7yhHbIWT1AH66+XWN8bXq7l3RO/ukeaci98JfkbkxURZhtxV/HHuvUhnPLdX
3TwygPBYZFNo4pzVEhzWoTtnEtrFueKxyc3+LjZpuo+mBlQ6ORtfgkr9gBVphXZG
YEzkCD3lVdl8L4cw9BVpKrJCs1c5taGjDgdInQKBgHm/fVvv96bJxc9x1tffXAcj
3OVdUN0UgXNCSaf/3A/phbeBQe9xS+3mpc4r6qvx+iy69mNBeNZ0xOitIjpjBo2+
dBEjSBwLk5q5tJqHmy/jKMJL4n9ROlx93XS+njxgibTvU6Fp9w+NOFD/HvxB3Tcz
6+jJF85D5BNAG3DBMKBjAoGBAOAxZvgsKN+JuENXsST7F89Tck2iTcQIT8g5rwWC
P9Vt74yboe2kDT531w8+egz7nAmRBKNM751U/95P9t88EDacDI/Z2OwnuFQHCPDF
llYOUI+SpLJ6/vURRbHSnnn8a/XG+nzedGH5JGqEJNQsz+xT2axM0/W/CRknmGaJ
kda/AoGANWrLCz708y7VYgAtW2Uf1DPOIYMdvo6fxIB5i9ZfISgcJ/bbCUkFrhoH
+vq/5CIWxCPp0f85R4qxxQ5ihxJ0YDQT9Jpx4TMss4PSavPaBH3RXow5Ohe+bYoQ
NE5OgEXk2wVfZczCZpigBKbKZHNYcelXtTt/nP3rsCuGcM4h53s=
-----END RSA PRIVATE KEY-----
"""


class MechInstance():
    """Class to hold a mech instance (aka virtual machine)."""

    def __init__(self, name, mechfile=None):
        """Constructor for the mech instance."""
        if not name or name == "":
            raise AttributeError("Must provide a name for the instance.")
        if not mechfile:
            mechfile = utils.load_mechfile()
        LOGGER.debug("loaded mechfile:%s", mechfile)
        if mechfile.get(name, None):
            self.name = name
        else:
            sys.exit(click.style("Instance ({}) was not found in the "
                                 "Mechfile".format(name), fg="red"))
        self.box = mechfile[name].get('box', None)
        self.box_version = mechfile[name].get('box_version', None)
        self.url = mechfile[name].get('url', None)
        self.box_file = mechfile[name].get('file', None)
        self.provision = mechfile[name].get('provision', None)
        self.enable_ip_lookup = False
        self.config = {}
        self.ip = None
        # Note: providers are 'vmware' (default) or 'virtualbox'.
        self.provider = mechfile[name].get('provider', 'vmware')
        self.tools_state = None
        self.auth = mechfile[name].get('auth', None)
        self.shared_folders = mechfile[name].get('shared_folders', [])
        self.user = DEFAULT_USER
        self.password = DEFAULT_PASSWORD
        self.use_psk = False
        self.path = os.path.join(utils.mech_dir(), name)
        self.vmx = None
        self.vbox = None
        self.created = False
        if self.provider == 'vmware':
            # Note: If vmware vm has not been started vmx will be None
            vmx = utils.locate(self.path, '*.vmx')
            if vmx:
                self.vmx = vmx
                self.created = True
            else:
                self.vmx = None
                self.created = False
        elif self.provider == 'virtualbox':
            # Note: If virtualbox vm has not been started vmx will be None
            vbox = utils.locate(self.path, '*.vbox')
            if vbox:
                self.vbox = vbox
                self.created = True
            else:
                self.vbox = None
                self.created = False

        self.no_nat = False
        self.remove_vagrant = False
        self.gui = False
        self.disable_provisioning = False
        self.disable_shared_folders = False

        # If vmx exists, then the VM has already been created.
        # See if we need to switch to preshared key authentication
        # for interactions with this guest.
        if self.created:
            self.switch_to_psk()

    def switch_to_psk(self):
        """Switch to using preshared key, instead of using user/password."""
        if self.auth:
            mech_use = self.auth.get('mech_use', False)
            username = self.auth.get('username')
            if username and username != '' and mech_use:
                self.user = username
                self.password = None
                self.use_psk = True

    def get_ip(self, wait=False, quiet=True):
        """ Get the ip address."""
        LOGGER.debug("self.ip:%s self.provider:%s", self.ip, self.provider)
        if self.ip:
            return self.ip
        else:
            if self.provider == 'vmware':
                if self.vmx:
                    vmrun = VMrun(self.vmx)
                    ip_address = vmrun.get_guest_ip_address(wait=wait,
                                                            lookup=self.enable_ip_lookup,
                                                            quiet=quiet)
                    self.ip = ip_address
                    return self.ip
            else:
                vbm = VBoxManage()
                self.ip = vbm.ip(self.name, wait=wait, quiet=quiet)
                return self.ip

    def get_vm_state(self):
        """ Get the state of the VM.
            Returns info like: ('running', 'paused', 'powered off')
        """
        if self.provider == 'vmware':
            vmrun = VMrun(self.vmx)
            return vmrun.vm_state()

        if self.provider == 'virtualbox':
            vbm = VBoxManage()
            return vbm.vm_state(self.name)

    def get_vm_info(self):
        """ Get detailed info about the VM.
            There is no equivalent in VMware. :-(
        """
        if self.provider == 'virtualbox':
            vbm = VBoxManage()
            return vbm.get_vm_info(self.name)

    def get_tools_state(self):
        """ Get the tools state."""
        if self.tools_state:
            return self.tools_state
        else:
            if self.vmx:
                vmrun = VMrun(self.vmx)
                self.tools_state = vmrun.installed_tools()
                return self.tools_state

    def __repr__(self):
        """Return a representation of a Mech instance."""
        sep = '\n'
        return ('name:{name}{sep}created:{created}{sep}box:{box}'
                '{sep}box_version:{box_version}'
                '{sep}url:{url}{sep}box_file:{box_file}{sep}provision:{provision}'
                '{sep}vmx:{vmx}{sep}user:{user}'
                '{sep}password:{password}{sep}enable_ip_lookup:{enable_ip_lookup}'
                '{sep}config:{config}{sep}shared_folders:{shared_folders}'
                '{sep}auth:{auth}{sep}use_psk:{use_psk}{sep}provider:{provider}'
                '{sep}no_nat:{no_nat}{sep}remove_vagrant:{remove_vagrant}'
                '{sep}gui:{gui}{sep}disable_provisioning:{disable_provisioning}'
                '{sep}disable_shared_folders:{disable_shared_folders}'.
                format(name=self.name, created=self.created,
                       box=self.box, box_version=self.box_version,
                       url=self.url, box_file=self.box_file,
                       provision=self.provision, vmx=self.vmx,
                       user=self.user, password=self.password,
                       enable_ip_lookup=self.enable_ip_lookup,
                       config=self.config,
                       shared_folders=self.shared_folders,
                       auth=self.auth, use_psk=self.use_psk,
                       provider=self.provider, no_nat=self.no_nat,
                       remove_vagrant=self.remove_vagrant, gui=self.gui,
                       disable_provisioning=self.disable_provisioning,
                       disable_shared_folders=self.disable_shared_folders,
                       sep=sep))

    def config_ssh(self):
        """Configure ssh to work. If needed, create an insecure private key file for ssh/scp."""
        if not self.get_ip():
            sys.exit(click.style(
                "This Mech machine is reporting that it is not yet ready for SSH. "
                "Make sure your machine is created and running and try again. "
                "Additionally, check the output of `mech ls` to verify "
                "that the machine is in the state that you expect.", fg="red"))

        if not self.use_psk:
            key = os.path.abspath(os.path.join(
                utils.mech_dir(), "insecure_private_key"))
            if not os.path.exists(key):
                with open(key, 'w') as the_file:
                    the_file.write(INSECURE_PRIVATE_KEY)
                os.chmod(key, 0o400)
        else:
            key = '~/.ssh/id_rsa'

        self.config = {
            "Host": self.name,
            "User": self.user,
            "Port": "22",
            "UserKnownHostsFile": "/dev/null",
            "StrictHostKeyChecking": "no",
            "PasswordAuthentication": "no",
            "IdentityFile": key,
            "IdentitiesOnly": "yes",
            "LogLevel": "FATAL",
        }
        for key, value in self.config.items():
            key = re.sub(r'[ _]+', r' ', key)
            key = re.sub(r'(?<=[^_])([A-Z])', r' \1', key).lower()
            key = re.sub(r'^( *)(.*?)( *)$', r'\2', key)

            def callback(pat):
                return pat.group(1).upper()

            key = re.sub(r' (\w)', callback, key)
            if key[0].islower():
                key = key[0].upper() + key[1:]
            self.config[key] = value
        self.config.update({
            "HostName": self.ip,
        })
        return self.config

    def winrm_raw_config(self):
        """Print the winrm configuration."""
        if not self.get_ip():
            sys.exit(click.style(
                "This Mech machine is reporting that it is not yet ready. "
                "Make sure your machine is created and running and try again. "
                "Additionally, check the output of `mech ls` to verify "
                "that the machine is in the state that you expect.", fg="red"))

        config = {
            "Host": self.name,
            "HostName": self.ip,
            "User": self.user,
            "Password": self.password,
            "Port": "5985",
            "RDPHostName": self.ip,
            "RDPPort": 3389,
            "RDPUser": self.user,
            "RDPPassword": self.password,
        }
        return config

    def winrm_config(self):
        """Return the winrm configuration formatted."""
        config = self.winrm_raw_config()
        return ('Host {}\n  Hostname {}\n  User {}\n  Password {}\n'
                '  Port {}\n  RDPHostName {}\n  RDPPort {}\n  RDPUser {}\n'
                '  RDPPassword {}\n').format(config.get("Host"), config.get("HostName"),
                                             config.get("User"), config.get("Password"),
                                             config.get("Port"), config.get("RDPHostName"),
                                             config.get("RDPPort"), config.get("RDPUser"),
                                             config.get("RDPPassword"))
