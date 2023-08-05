# -*- coding: utf-8 -*-
#
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
"""VMrun class"""

from __future__ import absolute_import

import os
import sys
import re
import logging
import subprocess
import tempfile

from .compat import b2s
from . import utils


LOGGER = logging.getLogger('mech')


class VMrun():  # pylint: disable=too-many-public-methods
    """Interface class for the 'vmrun' command.
       The 'vmrun' command is used to interact with VMware.
       To add/update vmware functionality, run the 'vmrun' command with '--help'.
    """

    def __init__(self, vmx_file=None,  # pylint: disable=too-many-arguments
                 user=None, password=None, executable=None, provider=None,
                 test_mode=False):
        """Constructor - set sane defaults."""
        self.vmx_file = vmx_file
        self.user = user
        self.password = password
        self.executable = executable
        self.provider = provider

        if self.executable is None:
            if sys.platform == 'darwin':
                self.executable = utils.get_darwin_executable()
            elif sys.platform == 'win32':
                self.executable = utils.get_win32_executable()
            else:
                self.executable = utils.get_fallback_executable()
        if self.provider is None:
            if self.executable is not None:
                self.provider = utils.get_provider(self.get_executable())
                LOGGER.debug('self.get_executable():%s self.provider:%s',
                             self.get_executable(), self.provider)
        # If test_mode is True, then do not perform the action
        # just return the command info
        self.test_mode = test_mode

    def installed(self):
        """Returns True if vmware is installed (based on whether we
           could find the vmrun command."""
        if self.get_executable() is not None and os.path.exists(self.get_executable()):
            return True
        else:
            return False

    def get_executable(self):
        """Return the executable value. (could be None or a string)."""
        return self.executable

    def vmrun(self, cmd, *args, **kwargs):
        """Execute a 'vmrun' command."""
        quiet = kwargs.pop('quiet', False)
        arguments = kwargs.pop('arguments', ())

        cmds = [self.executable]
        cmds.append('-T')
        cmds.append(self.provider)
        if self.user:
            cmds.append('-gu')
            cmds.append(self.user)
        if self.password:
            cmds.append('-gp')
            cmds.append(self.password)
        cmds.append(cmd)
        cmds.extend(filter(None, args))
        cmds.extend(filter(None, arguments))

        LOGGER.debug(
            " ".join(
                "'{}'".format(
                    c.replace(
                        "'",
                        "\\'")) if ' ' in c else c for c in cmds))

        if self.test_mode:
            return cmds

        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.SW_HIDE | subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.Popen(
            cmds,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=startupinfo)
        stdoutdata, stderrdata = map(b2s, proc.communicate())

        if stderrdata and not quiet:
            LOGGER.error(stderrdata.strip())
        LOGGER.debug("(⏎ %s)", proc.returncode)

        if not proc.returncode:
            stdoutdata = stdoutdata.strip()
            LOGGER.debug(repr(stdoutdata))
            return stdoutdata

        if stdoutdata and not quiet:
            LOGGER.error(stdoutdata.strip())

    ############################################################################
    # POWER COMMANDS           PARAMETERS           DESCRIPTION
    # --------------           ----------           -----------
    # start                    Path to vmx file     Start a VM or Team
    #                          [gui|nogui]
    #
    # stop                     Path to vmx file     Stop a VM or Team
    #                          [hard|soft]
    #
    # reset                    Path to vmx file     Reset a VM or Team
    #                          [hard|soft]
    #
    # suspend                  Path to vmx file     Suspend a VM or Team
    #                          [hard|soft]
    #
    # pause                    Path to vmx file     Pause a VM
    #
    # unpause                  Path to vmx file     Unpause a VM
    #

    def start(self, gui=False, quiet=False):
        '''Start a VM or Team'''
        return self.vmrun('start', self.vmx_file, 'gui' if gui else 'nogui', quiet=quiet)

    def stop(self, mode='soft', quiet=False):
        '''Stop a VM or Team'''
        return self.vmrun('stop', self.vmx_file, mode, quiet=quiet)

    def reset(self, mode='soft', quiet=False):
        '''Reset a VM or Team'''
        return self.vmrun('reset', self.vmx_file, mode, quiet=quiet)

    def suspend(self, mode='soft', quiet=False):
        '''Suspend a VM or Team'''
        return self.vmrun('suspend', self.vmx_file, mode, quiet=quiet)

    def pause(self, quiet=False):
        '''Pause a VM'''
        return self.vmrun('pause', self.vmx_file, quiet=quiet)

    def unpause(self, quiet=False):
        '''Unpause a VM'''
        return self.vmrun('unpause', self.vmx_file, quiet=quiet)

    ############################################################################
    # SNAPSHOT COMMANDS        PARAMETERS           DESCRIPTION
    # -----------------        ----------           -----------
    # listSnapshots            Path to vmx file     List all snapshots in a VM
    #                          [showTree]
    #
    # snapshot                 Path to vmx file     Create a snapshot of a VM
    #                          Snapshot name
    #
    # deleteSnapshot           Path to vmx file     Remove a snapshot from a VM
    #                          Snapshot name
    #                          [andDeleteChildren]
    #
    # revertToSnapshot         Path to vmx file     Set VM state to a snapshot
    #                          Snapshot name
    #

    def list_snapshots(self, show_tree=False, quiet=False):
        '''List all snapshots in a VM'''
        return self.vmrun(
            'listSnapshots',
            self.vmx_file,
            'showTree' if show_tree else None,
            quiet=quiet)

    def snapshot(self, snap_name, quiet=False):
        '''Create a snapshot of a VM'''
        return self.vmrun('snapshot', self.vmx_file, snap_name, quiet=quiet)

    def delete_snapshot(self, snap_name, and_delete_children=False, quiet=False):
        '''Remove a snapshot from a VM'''
        return self.vmrun(
            'deleteSnapshot',
            self.vmx_file,
            snap_name,
            'andDeleteChildren' if and_delete_children else None,
            quiet=quiet)

    def revert_to_snapshot(self, snap_name, quiet=False):
        '''Set VM state to a snapshot'''
        return self.vmrun('revertToSnapshot', self.vmx_file, snap_name, quiet=quiet)

    ############################################################################
    # NETWORKADAPTER COMMANDS  PARAMETERS           DESCRIPTION
    # -----------------------  ----------           -----------
    # listNetworkAdapters      Path to vmx file     List all network adapters in a VM
    #
    #
    # addNetworkAdapter        Path to vmx file     Add a network adapter on a VM
    #                          Network adapter type
    #                          [Host nework]
    #
    #
    # setNetworkAdapter        Path to vmx file     Update a network adapter on a VM
    #                          Network adapter index
    #                          Network adapter type
    #                          [Host network]
    #
    #
    # deleteNetworkAdapter     Path to vmx file     Remove a network adapter on a VM
    #                          Network adapter index

    def list_network_adapters(self, quiet=False):
        '''List all network adapters in a VM'''
        return self.vmrun('listNetworkAdapters', self.vmx_file, quiet=quiet)

    def add_network_adapter(self, adapter_type, host_network=None, quiet=False):
        '''Add a network adapter on a VM'''
        return self.vmrun(
            'addNetworkAdapter',
            self.vmx_file,
            adapter_type,
            host_network,
            quiet=quiet)

    def set_network_adapter(self, adapter_index, adapter_type, host_network=None, quiet=False):
        '''Update a network adapter on a VM'''
        return self.vmrun(
            'setNetworkAdapter',
            self.vmx_file,
            adapter_index,
            adapter_type,
            host_network,
            quiet=quiet)

    def delete_network_adapter(self, adapter_index, quiet=False):
        '''Remove a network adapter on a VM'''
        return self.vmrun('deleteNetworkAdapter', self.vmx_file, adapter_index, quiet=quiet)

    ############################################################################
    # HOST NETWORK COMMANDS    PARAMETERS           DESCRIPTION
    # ---------------------    ----------           -----------
    # listHostNetworks                              List all networks in the host
    #
    # listPortForwardings      Host network name    List all available port
    #                                               forwardings on a host network
    #
    #
    # setPortForwarding        Host network name    Add or update a port
    #                                               forwarding on a host network
    #                          Protocol
    #                          Host port
    #                          Guest ip
    #                          Guest port
    #                          [Description]
    #
    # deletePortForwarding     Host network name    Delete a port forwarding on a host network
    #                          Protocol
    #                          Host port

    def list_host_networks(self, quiet=False):
        '''List all networks in the host.
           Note: Not available on linux.
        '''
        return self.vmrun('listHostNetworks', quiet=quiet)

    def list_port_forwardings(self, host_network, quiet=False):
        '''List all available port forwardings on a host network'''
        return self.vmrun('listPortForwardings', host_network, quiet=quiet)

    def set_port_forwarding(  # pylint: disable=too-many-arguments
            self,
            host_network,
            protocol,
            host_port,
            guest_ip,
            guest_port,
            description=None,
            quiet=False):
        '''Add or update a port forwarding on a host network'''
        return self.vmrun(
            'setPortForwarding',
            host_network,
            protocol,
            host_port,
            guest_ip,
            guest_port,
            description,
            quiet=quiet)

    def delete_port_forwarding(self, host_network, protocol, host_port,
                               quiet=False):  # pylint: disable=too-many-arguments
        '''Delete a port forwarding on a host network'''
        return self.vmrun('deletePortForwarding', host_network, protocol, host_port, quiet=quiet)

    ############################################################################
    # GUEST OS COMMANDS        PARAMETERS           DESCRIPTION
    # -----------------        ----------           -----------
    # runProgramInGuest        Path to vmx file     Run a program in Guest OS
    #                          [-noWait]
    #                          [-activeWindow]
    #                          [-interactive]
    #                          Complete-Path-To-Program
    #                          [Program arguments]
    #
    # fileExistsInGuest        Path to vmx file     Check if a file exists in Guest OS
    #                          Path to file in guest
    #
    # directoryExistsInGuest   Path to vmx file     Check if a directory exists in Guest OS
    #                          Path to directory in guest
    #
    # setSharedFolderState     Path to vmx file     Modify a Host-Guest shared folder
    #                          Share name
    #                          Host path
    #                          writable | readonly
    #
    # addSharedFolder          Path to vmx file     Add a Host-Guest shared folder
    #                          Share name
    #                          New host path
    #
    # removeSharedFolder       Path to vmx file     Remove a Host-Guest shared folder
    #                          Share name
    #
    # enableSharedFolders      Path to vmx file     Enable shared folders in Guest
    #                          [runtime]
    #
    # disableSharedFolders     Path to vmx file     Disable shared folders in Guest
    #                          [runtime]
    #
    # listProcessesInGuest     Path to vmx file     List running processes in Guest OS
    #
    # killProcessInGuest       Path to vmx file     Kill a process in Guest OS
    #                          process id
    #
    # runScriptInGuest         Path to vmx file     Run a script in Guest OS
    #                          [-noWait]
    #                          [-activeWindow]
    #                          [-interactive]
    #                          Interpreter path
    #                          Script text
    #
    # deleteFileInGuest        Path to vmx file     Delete a file in Guest OS
    #                          Path in guest
    #
    # createDirectoryInGuest   Path to vmx file     Create a directory in Guest OS
    #                          Directory path in guest
    #
    # deleteDirectoryInGuest   Path to vmx file     Delete a directory in Guest OS
    #                          Directory path in guest
    #
    # createTempfileInGuest    Path to vmx file     Create a temporary file in Guest OS
    #
    # listDirectoryInGuest     Path to vmx file     List a directory in Guest OS
    #                          Directory path in guest
    #
    # copyFileFromHostToGuest  Path to vmx file     Copy a file from host OS to guest OS
    #                          Path on host
    #                          Path in guest
    #
    # copyFileFromGuestToHost  Path to vmx file     Copy a file from guest OS to host OS
    #                          Path in guest
    #                          Path on host
    #
    # renameFileInGuest        Path to vmx file     Rename a file in Guest OS
    #                          Original name
    #                          New name
    #
    # typeKeystrokesInGuest    Path to vmx file     Type Keystrokes in Guest OS
    #                          keystroke string
    #
    # connectNamedDevice       Path to vmx file     Connect the named device in the Guest OS
    #                          device name
    #
    # disconnectNamedDevice    Path to vmx file     Disconnect the named device in the Guest OS
    #                          device name
    #
    # captureScreen            Path to vmx file     Capture the screen of the VM to a local file
    #                          Path on host
    #
    # writeVariable            Path to vmx file     Write a variable in the VM state
    #                          [runtimeConfig|guestEnv|guestVar]
    #                          variable name
    #                          variable value
    #
    # readVariable             Path to vmx file     Read a variable in the VM state
    #                          [runtimeConfig|guestEnv|guestVar]
    #                          variable name
    #
    # getGuestIPAddress        Path to vmx file     Gets the IP address of the guest
    #                          [-wait]
    #

    def run_program_in_guest(  # pylint: disable=too-many-arguments
            self,
            program_path,
            program_arguments=None,
            wait=True,
            activate_window=False,
            interactive=False,
            quiet=False):
        """Run a program in the guest vm."""
        if program_arguments is None:
            program_arguments = []
        return self.vmrun(
            'runProgramInGuest',
            self.vmx_file,
            None if wait else '-noWait',
            '-activateWindow' if activate_window else None,
            '-interactive' if interactive else None,
            program_path,
            arguments=program_arguments,
            quiet=quiet)

    def set_shared_folder_state(self, share_name, new_path, mode='readonly', quiet=False):
        '''Modify a Host-Guest shared folder'''
        return self.vmrun(
            'setSharedFolderState',
            self.vmx_file,
            share_name,
            new_path,
            mode,
            quiet=quiet)

    def add_shared_folder(self, share_name, host_path, quiet=False):
        '''Add a Host-Guest shared folder'''
        return self.vmrun('addSharedFolder', self.vmx_file, share_name, host_path, quiet=quiet)

    def remove_shared_folder(self, share_name, quiet=False):
        '''Remove a Host-Guest shared folder'''
        return self.vmrun('removeSharedFolder', self.vmx_file, share_name, quiet=quiet)

    def enable_shared_folders(self, runtime=None, quiet=False):
        '''Enable shared folders.'''
        return self.vmrun('enableSharedFolders', self.vmx_file, runtime, quiet=quiet)

    def disable_shared_folders(self, runtime=None, quiet=False):
        '''Disable shared folders in Guest'''
        return self.vmrun('disableSharedFolders', self.vmx_file, runtime, quiet=quiet)

    def list_processes_in_guest(self, quiet=False):
        '''List running processes in Guest OS'''
        return self.vmrun('listProcessesInGuest', self.vmx_file, quiet=quiet)

    def kill_process_in_guest(self, pid, quiet=False):
        '''Kill a process in Guest OS'''
        return self.vmrun('killProcessInGuest', self.vmx_file, pid, quiet=quiet)

    def run_script_in_guest(  # pylint: disable=too-many-arguments
            self,
            interpreter_path,
            script,
            wait=True,
            activate_window=False,
            interactive=False,
            quiet=False):
        '''Run a script in Guest OS'''
        return self.vmrun(
            'runScriptInGuest',
            self.vmx_file,
            interpreter_path,
            script,
            None if wait else '-noWait',
            '-activateWindow' if activate_window else None,
            '-interactive' if interactive else None,
            quiet=quiet)

    def delete_file_in_guest(self, filename, quiet=False):
        '''Delete a file in Guest OS'''
        return self.vmrun('deleteFileInGuest', self.vmx_file, filename, quiet=quiet)

    def create_directory_in_guest(self, path, quiet=False):
        '''Create a directory in Guest OS'''
        return self.vmrun('createDirectoryInGuest', self.vmx_file, path, quiet=quiet)

    def delete_directory_in_guest(self, path, quiet=False):
        '''Delete a directory in Guest OS'''
        return self.vmrun('deleteDirectoryInGuest', self.vmx_file, path, quiet=quiet)

    def create_tempfile_in_guest(self, quiet=False):
        '''Create a temporary file in Guest OS'''
        return self.vmrun('createTempfileInGuest', self.vmx_file, quiet=quiet)

    def list_directory_in_guest(self, path, quiet=False):
        '''List a directory in Guest OS'''
        return self.vmrun('listDirectoryInGuest', self.vmx_file, path, quiet=quiet)

    def copy_file_from_host_to_guest(self, host_path, guest_path, quiet=False):
        '''Copy a file from host OS to guest OS'''
        return self.vmrun(
            'copyFileFromHostToGuest',
            self.vmx_file,
            host_path,
            guest_path,
            quiet=quiet)

    def copy_file_from_guest_to_host(self, guest_path, host_path, quiet=False):
        '''Copy a file from guest OS to host OS'''
        return self.vmrun(
            'copyFileFromGuestToHost',
            self.vmx_file,
            guest_path,
            host_path,
            quiet=quiet)

    def rename_file_in_guest(self, original_name, new_name, quiet=False):
        '''Rename a file in Guest OS'''
        return self.vmrun('renameFileInGuest', self.vmx_file, original_name, new_name, quiet=quiet)

    def type_keystrokes_in_guest(self, keystroke, quiet=False):
        '''Type Keystrokes in Guest OS'''
        return self.vmrun('typeKeystrokesInGuest', self.vmx_file, keystroke, quiet=quiet)

    def connect_named_device(self, device_name, quiet=False):
        '''Connect the named device in the Guest OS'''
        return self.vmrun('connectNamedDevice', self.vmx_file, device_name, quiet=quiet)

    def disconnect_named_device(self, device_name, quiet=False):
        '''Disconnect the named device in the Guest OS'''
        return self.vmrun('disconnectNamedDevice', self.vmx_file, device_name, quiet=quiet)

    def capture_screen(self, path_on_host, quiet=False):
        '''Capture the screen of the VM to a local file'''
        return self.vmrun('captureScreen', self.vmx_file, path_on_host, quiet=quiet)

    def write_variable(self, var_name, var_value, mode=None, quiet=False):
        '''Write a variable in the VM state'''
        return self.vmrun('writeVariable', self.vmx_file, mode, var_name, var_value, quiet=quiet)

    def read_variable(self, var_name, mode=None, quiet=False):
        '''Read a variable in the VM state'''
        return self.vmrun('readVariable', self.vmx_file, mode, var_name, quiet=quiet)

    def get_guest_ip_address(self, wait=True, quiet=False, lookup=False):
        '''Gets the IP address of the guest'''
        if lookup is True:
            guest_tmp_filename = '/tmp/.ip_address'
            cmd = "ifconfig | grep -Eo 'inet (addr:)?([0-9]*\\.){3}[0-9]*'"
            cmd += "| grep -Eo '([0-9]*\\.){3}[0-9]*' | grep -v '127.0.0.1' > " + guest_tmp_filename
            LOGGER.debug("cmd:%s", cmd)
            self.run_script_in_guest('/bin/sh', cmd, quiet=quiet)
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            try:
                temp_file.close()
                self.copy_file_from_guest_to_host(guest_tmp_filename, temp_file.name, quiet=quiet)
                ip_addresses = open(temp_file.name).read().split()
                # clean up the guest tmp file
                self.run_script_in_guest(
                    '/bin/sh',
                    "rm {}".format(guest_tmp_filename),
                    quiet=False)
                if ip_addresses:
                    return ip_addresses[0]
                else:
                    return None
            finally:
                os.unlink(temp_file.name)
        else:
            ip_address = self.vmrun('getGuestIPAddress', self.vmx_file,
                                    '-wait' if wait else None, quiet=quiet)
            if ip_address == 'unknown':
                ip_address = ''
        return ip_address

    ############################################################################
    # GENERAL COMMANDS         PARAMETERS           DESCRIPTION
    # ----------------         ----------           -----------
    # list                                          List all running VMs
    #
    # upgradevm                Path to vmx file     Upgrade VM file format, virtual hw
    #
    # installTools             Path to vmx file     Install Tools in Guest
    #
    # checkToolsState          Path to vmx file     Check the current Tools state
    #
    # deleteVM                 Path to vmx file     Delete a VM
    #
    # clone                    Path to vmx file     Create a copy of the VM
    #                          Path to destination vmx file
    #                          full|linked
    #                          [-snapshot=Snapshot Name]
    #                          [-cloneName=Name]

    def list(self, quiet=False):
        '''List all running VMs'''
        return self.vmrun('list', self.vmx_file, quiet=quiet)

    def upgradevm(self, quiet=False):
        '''Upgrade VM file format, virtual hw.
           Note: The vm must be stopped before running this command.
        '''
        return self.vmrun('upgradevm', self.vmx_file, quiet=quiet)

    def install_tools(self, quiet=False):
        '''Install Tools in Guest OS'''
        return self.vmrun('installTools', self.vmx_file, quiet=quiet)

    def check_tools_state(self, quiet=False):
        '''Check the current Tools state'''
        return self.vmrun('checkToolsState', self.vmx_file, quiet=quiet)

    def register(self, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''Register a VM'''
        return self.vmrun('register', self.vmx_file, quiet=quiet)

    def unregister(self, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''Unregister a VM'''
        return self.vmrun('unregister', self.vmx_file, quiet=quiet)

    def list_registered_vm(self, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''List registered VMs'''
        return self.vmrun('listRegisteredVM', self.vmx_file, quiet=quiet)

    def delete_vm(self, quiet=False):
        '''Delete a VM'''
        return self.vmrun('deleteVM', self.vmx_file, quiet=quiet)

    def clone(self, dest_vmx, mode, snap_name=None, quiet=False):
        '''Create a copy of the VM'''
        return self.vmrun('clone', self.vmx_file, dest_vmx, mode, snap_name, quiet=quiet)

    ############################################################################
    # RECORD/REPLAY COMMANDS   PARAMETERS           DESCRIPTION
    # ----------------------   ----------           -----------
    # beginRecording           Path to vmx file     Begin recording a VM
    #                          Snapshot name
    #
    # endRecording             Path to vmx file     End recording a VM
    #
    # beginReplay              Path to vmx file     Begin replaying a VM
    #                          Snapshot name
    #
    # endReplay                Path to vmx file     End replaying a VM

    def begin_recording(self, snap_name, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''Begin recording a VM'''
        return self.vmrun('beginRecording', self.vmx_file, snap_name, quiet=quiet)

    def end_recording(self, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''End recording a VM'''
        return self.vmrun('endRecording', self.vmx_file, quiet=quiet)

    def begin_replay(self, snap_name, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''Begin replaying a VM'''
        return self.vmrun('beginReplay', self.vmx_file, snap_name, quiet=quiet)

    def end_replay(self, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''End replaying a VM'''
        return self.vmrun('endReplay', self.vmx_file, quiet=quiet)

    ############################################################################
    # VPROBE COMMANDS          PARAMETERS           DESCRIPTION
    # ---------------          ----------           -----------
    # vprobeVersion            Path to vmx file     List VP version
    #
    # vprobeLoad               Path to vmx file     Load VP script
    #                          'VP script text'
    #
    # vprobeLoadFile           Path to vmx file     Load VP file
    #                          Path to VP file
    #
    # vprobeReset              Path to vmx file     Disable all vprobes
    #
    # vprobeListProbes         Path to vmx file     List probes
    #
    # vprobeListGlobals        Path to vmx file     List global variables

    def vprobe_version(self, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''List VP version'''
        return self.vmrun('vprobeVersion', self.vmx_file, quiet=quiet)

    def vprobe_load(self, script, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''Load VP script'''
        return self.vmrun('vprobeLoad', self.vmx_file, script, quiet=quiet)

    def vprobe_load_file(self, vprobe, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''Load VP file'''
        return self.vmrun('vprobeLoadFile', self.vmx_file, vprobe, quiet=quiet)

    def vprobe_reset(self, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''Disable all vprobes'''
        return self.vmrun('vprobeReset', self.vmx_file, quiet=quiet)

    def vprobe_list_probes(self, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''List probes'''
        return self.vmrun('vprobeListProbes', self.vmx_file, quiet=quiet)

    def vprobe_list_globals(self, quiet=False):
        # unavailable in VMware Fusion 10 (OS X)?
        '''List global variables'''
        return self.vmrun('vprobeListGlobals', self.vmx_file, quiet=quiet)

    ############################################################################

    def installed_tools(self, quiet=False):
        '''Return True if VMware tools is in either 'installed' or 'running',
           otherwise, return False.
        '''
        state = self.check_tools_state(quiet=quiet)
        return state in ('installed', 'running')

    def vm_state(self, quiet=False):
        '''Return info about the state of the VM.

           Note: This is totally a hack as the VMware vmrun api does not provide much of
                 this info.

           Look in the vmware.log in same dir as .vmx file.
           Read file in reverse order until we find one of these strings

        '''
        if self.vmx_file:
            vmware_log = os.path.join(os.path.dirname(self.vmx_file), "vmware.log")
            if os.path.isfile(vmware_log):
                for line in reversed(list(open(vmware_log))):
                    if re.search(r"Reporting power state change \(opcode=2, err=0\)", line):
                        return "started"  # could also be "reset"
                    if re.search(r"VMX exit \(0\)", line):
                        return "stopped"  # could also be "suspend"
                    if re.search("VMAutomation_Pause: pause = FALSE", line):
                        return "unpaused"
                    if re.search("VMAutomation_Pause: pause = TRUE", line):
                        return "paused"
            return 'unknown'
