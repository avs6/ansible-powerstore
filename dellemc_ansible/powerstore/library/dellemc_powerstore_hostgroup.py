#!/usr/bin/python
# Copyright: (c) 2019, DellEMC

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils import dellemc_ansible_utils as utils
import logging

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_powerstore_hostgroup
version_added: '2.6'
short_description:  Manage host group on PowerStore Storage System
description:
- Managing host group on PowerStore storage system includes create
  host group with a set of hosts, add/remove hosts from host group, rename
  host group and delete host group.
- Deletion of a host group results in deletion of the containing hosts as well.
  Remove hosts from the host group first to retain them.
author:
- Manisha Agrawal (manisha.agrawal@dell.com)
extends_documentation_fragment:
  - dellemc.dellemc_powerstore
options:
  hostgroup_name:
    description:
    - The host group name. This value must contain 128 or fewer printable
      Unicode characters.
    - Creation of empty host group is not allowed.
    - Required when creating a host group.
    - Use either hostgroup_id or hostgroup_name for modify and delete tasks.
  hostgroup_id:
    description:
    - The 36 character long host group id, automatically generated when a
      host group is created.
    - Use either hostgroup_id or hostgroup_name for modify and delete tasks.
    - hostgroup_id cannot be used while creating host group, as it is
      generated by the array after creation of host group.
  hosts:
    description:
    - List of hosts to be added or removed from the host group.
    - Child hosts in a host group can only be of one type, either FC or iSCSI.
    - Required when creating a host group.
    - To represent host, both name or ID can be used interchangeably. The module
      will detect both.
  state:
    description:
    - Define whether the host group should exist or not.
    - present - indicates that the host group should exist on system.
    - absent - indicates that the host group should not exist on system.
    - Deletion of a host group results in deletion of the containing hosts as
      well. Remove hosts from the host group first to retain them.
    required: True
    choices: [absent, present]
  host_state:
    description:
    - Define whether the hosts should be present or absent in host group.
    - present-in-group - indicates that the hosts should exist on host group.
    - absent-in-group - indicates that the hosts should not exist on host group.
    - Required when creating a host group with hosts or adding/removing hosts
      from existing host group.
    choices: [present-in-group, absent-in-group]
  new_name:
    description:
    - The new name for host group renaming function. This value must contain
      128 or fewer printable Unicode characters.
  '''


EXAMPLES = r'''
  - name: Create host group with hosts using host name
    dellemc_powerstore_hostgroup:
      array_ip: "{{array_ip}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      hostgroup_name: "{{hostgroup_name}}"
      hosts:
        - host1
        - host2
      state: 'present'
      host_state: 'present-in-group'

  - name: Create host group with hosts using host ID
    dellemc_powerstore_hostgroup:
      array_ip: "{{array_ip}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      hostgroup_name: "{{hostgroup_name}}"
      hosts:
        - c17fc987-bf82-480c-af31-9307b89923c3
      state: 'present'
      host_state: 'present-in-group'

  - name: Get host group details
    dellemc_powerstore_hostgroup:
      array_ip: "{{array_ip}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      hostgroup_name: "{{hostgroup_name}}"
      state: 'present'

  - name: Get host group details using ID
    dellemc_powerstore_hostgroup:
      array_ip: "{{array_ip}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      hostgroup_id: "{{host group_id}}"
      state: 'present'

  - name: Add hosts to host group
    dellemc_powerstore_hostgroup:
      array_ip: "{{array_ip}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      hostgroup_name: "{{hostgroup_name}}"
      hosts:
        - host3
      host_state: 'present-in-group'
      state: 'present'

  - name: Remove hosts from host group
    dellemc_powerstore_hostgroup:
      array_ip: "{{array_ip}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      hostgroup_name: "{{hostgroup_name}}"
      hosts:
        - host3
      host_state: 'absent-in-group'
      state: 'present'

  - name: Rename host group
    dellemc_powerstore_hostgroup:
      array_ip: "{{array_ip}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      hostgroup_name: "{{hostgroup_name}}"
      new_name: "{{new_hostgroup_name}}"
      state: 'present'

  - name: Delete host group
    dellemc_powerstore_hostgroup:
      array_ip: "{{array_ip}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      hostgroup_name: "{{hostgroup_name}}"
      state: 'absent'
'''

RETURN = r'''
        "hostgroup_details": {
        "description": null,
        "hosts": [
            {
                "id": "01dedad0-375b-4b6d-901d-94a054d60afe",
                "name": "host1"
            },
            {
                "id": "0f626dc9-d2c6-416e-85e7-4a650b8c9dd7",
                "name": "host3"
            }
        ],
        "id": "50eea718-4beb-4a0b-84f2-9140f99b4437",
        "name": "Ansible_Test_Hostgroup"
        },
        "invocation": {
            "module_args": {
                "array_ip": "10.230.45.71",
                "host_state": "present-in-group",
                "hostgroup_id": null,
                "hostgroup_name": "Ansible_Test_Hostgroup",
                "hosts": [
                    "host3",
                    "01dedad0-375b-4b6d-901d-94a054d60afe"
                ],
                "new_name": null,
                "password": "VALUE_SPECIFIED_IN_NO_LOG_PARAMETER",
                "state": "present",
                "user": "admin"
            }
    }

'''
LOG = utils.get_logger('dellemc_powerstore_hostgroup', log_devel=logging.INFO)

py4ps_sdk = utils.has_pyu4ps_sdk()
HAS_PY4PS = py4ps_sdk['HAS_Py4PS']
IMPORT_ERROR = py4ps_sdk['Error_message']

py4ps_version = utils.py4ps_version_check()
IS_SUPPORTED_PY4PS_VERSION = py4ps_version['supported_version']
VERSION_ERROR = py4ps_version['unsupported_version_message']

# Application type
APPLICATION_TYPE = 'Ansible/1.0'

class PowerStoreHostgroup(object):
    '''Class with host group operations'''

    def __init__(self):
        # Define all parameters required by this module
        self.module_params = utils.get_powerstore_management_host_parameters()
        self.module_params.update(self.get_powerstore_hostgroup_parameters())
        # Initialize the Ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=True
        )

        LOG.info(
            'HAS_PY4PS = {0} , IMPORT_ERROR = {1}'.format(
                HAS_PY4PS, IMPORT_ERROR))
        if HAS_PY4PS is False:
            self.module.fail_json(msg=IMPORT_ERROR)
        LOG.info(
            'IS_SUPPORTED_PY4PS_VERSION = {0} , VERSION_ERROR = {1}'.format(
                IS_SUPPORTED_PY4PS_VERSION,
                VERSION_ERROR))
        if IS_SUPPORTED_PY4PS_VERSION is False:
            self.module.fail_json(msg=VERSION_ERROR)

        # result is a dictionary that contains changed status and host group
        # details
        self.result = {"changed": False, "hostgroup_details": {}}

        self.conn = utils.get_powerstore_connection(self.module.params,
                                                    application_type=APPLICATION_TYPE)
        LOG.info(
            'Got Python library connection instance for provisioning on PowerStore {0}'.format(
                self.conn))

    def get_powerstore_hostgroup_parameters(self):
        return dict(
            hostgroup_name=dict(
                required=False,
                type='str'),
            hostgroup_id=dict(
                required=False,
                type='str'),
            hosts=dict(
                required=False,
                type='list'),
            state=dict(
                required=True,
                choices=[
                    'present',
                    'absent'],
                type='str'),
            host_state=dict(
                required=False,
                choices=[
                    'absent-in-group',
                    'present-in-group'],
                type='str'),
            new_name=dict(
                required=False,
                type='str'),
        )

    def get_hostgroup(self, hostgroup_id):
        '''
        Get details of a given host group
        '''
        try:
            LOG.info('Getting host group {0} details'.format(hostgroup_id))
            return self.conn.provisioning.get_host_group_details(hostgroup_id)
        except Exception as e:
            LOG.error('Unable to get details of host group ID: {0} -- error: {1}'
                      .format(hostgroup_id, str(e)))

    def get_hostgroup_id_by_name(self, hostgroup_name):
        host_group_info = self.conn.provisioning.get_host_group_by_name(
            hostgroup_name)
        if host_group_info:
            if len(host_group_info) > 1:
                error_msg = 'Multiple host groups by the same name found'
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)
            return host_group_info[0]['id']
        return None

    def get_host(self, host_id):
        '''
        Get details of a given host
        '''
        try:
            LOG.info('Getting host {0} details'.format(host_id))
            return self.conn.provisioning.get_host_details(host_id)
        except Exception as e:
            LOG.error('Unable to get details of host ID: {0} -- error: {1}'
                      .format(host_id, str(e)))

    def create_host_list(self, hosts):
        '''
        A function which takes the hosts list given by the user (which could be
        either name or ID of each host), and converts it to a list of IDs.
        '''
        host_list = []
        for host in hosts:
            try:
                # Since the ID format of PowerStore is 36 characters long
                # check if host is host_id
                if len(host) == 36 and self.get_host(host):
                    host_list.append(host)
                else:
                    # check if host is host_name
                    id = self.get_host_id_by_name(host)
                    if id:
                        host_list.append(id)
                    else:
                        error_msg = ("Host {0} not found".format(host))
                        LOG.error(error_msg)
                        self.module.fail_json(msg=error_msg)
            except Exception as e:
                error_msg = ("Host {0} not found, error={1}".format(
                    host, str(e)))
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)
        return host_list

    def get_host_id_by_name(self, host_name):
        host_info = self.conn.provisioning.get_host_by_name(host_name)
        if host_info:
            if len(host_info) > 1:
                error_msg = 'Multiple hosts by the same name found'
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)
            return host_info[0]['id']
        return None

    def create_hostgroup(self, hostgroup_name, hosts):
        '''
        Create host group with given hosts
        '''
        if hosts is None or not len(hosts):
            error_msg = ("Create host group {0} failed as no hosts or invalid"
                         " hosts specified".format(hostgroup_name))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)
        
        host_state = self.module.params['host_state']
        if host_state != 'present-in-group':
                error_msg = (
                "Please provide correct host_state while trying to create a"
                " host group. Empty host group creation not allowed")
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)

        try:
            msg = "Creating host group {0} with hosts {1}"
            LOG.info(msg.format(hostgroup_name, hosts))
            resp = self.conn.provisioning.create_host_group(hostgroup_name,
                                                            hosts)
            LOG.info("the response is {}".format(resp))
            return True

        except Exception as e:
            error_msg = 'Create host group {0} failed with error {1}'.format(
                hostgroup_name, e)
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)
        return None

    def _get_add_hosts(self, existing, requested):
        all_hosts = existing + requested
        add_hosts = list(set(all_hosts) - set(existing))
        return add_hosts

    def _get_remove_hosts(self, existing, requested):
        rem_hosts = list(set(existing).intersection(set(requested)))
        return rem_hosts

    def add_hostgroup_hosts(self, hostgroup, hosts):

        existing_hosts = []
        if 'hosts' in hostgroup:
            current_hosts = hostgroup['hosts']
            for host in current_hosts:
                existing_hosts.append(host['id'])

        LOG.info('existing hosts {0}'.format(existing_hosts))
        if hosts and (set(hosts).issubset(set(existing_hosts))) :
            LOG.info('Hosts are already present in host group {0}'
                     .format(hostgroup['name']))
            return False

        add_list = self._get_add_hosts(existing_hosts, hosts)

        if len(add_list) > 0:
            try:
                LOG.info('Adding hosts {0} to host group {1}'.format(
                    add_list, hostgroup['name']))
                self.conn.provisioning.add_hosts_to_host_group(
                    hostgroup['id'], add_list)
                return True
            except Exception as e:
                error_msg = (
                    ("Adding hosts {0} to host group {1} failed with"
                     "error {2}").format(
                        add_list, hostgroup['name'], str(e)))
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)
        else:
            LOG.info('No hosts to add to host group {0}'.format(
                hostgroup['name']))
            return False

    def remove_hostgroup_hosts(self, hostgroup, hosts):

        existing_hosts = []
        if 'hosts' in hostgroup:
            current_hosts = hostgroup['hosts']
            for host in current_hosts:
                existing_hosts.append(host['id'])

        if existing_hosts is None or not len(existing_hosts):
            LOG.info(
                'No hosts are present in host group {0}'.format(
                    hostgroup['name']))
            return False

        remove_list = self._get_remove_hosts(existing_hosts, hosts)

        if len(remove_list) > 0:
            try:
                LOG.info('Removing hosts {0} from host group {1}'.format(
                    remove_list, hostgroup['name']))
                self.conn.provisioning.remove_hosts_from_host_group(
                    hostgroup['id'], remove_list)
                return True
            except Exception as e:
                error_msg = (("Removing hosts {0} from host group {1} failed"
                              "with error {2}").format(
                    remove_list,
                    hostgroup['name'],
                    str(e)))
                LOG.error(error_msg)
                self.module.fail_json(msg=error_msg)
        else:
            LOG.info('No hosts to remove from host group {0}'.format(
                hostgroup['name']))
            return False

    def rename_hostgroup(self, hostgroup, new_name):
        try:
            self.conn.provisioning.modify_host_group(
                hostgroup['id'], name=new_name)
            return True
        except Exception as e:
            error_msg = 'Renaming of host group {0} failed with error {1}'.format(
                hostgroup['name'], str(e))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)
            return None

    def delete_hostgroup(self, hostgroup):
        '''
        Delete host group from system
        '''
        try:
            self.conn.provisioning.delete_host_group(hostgroup['id'])
            return True
        except Exception as e:
            error_msg = (
                'Deleting host group {0} failed with error {1}'.format(
                    hostgroup['name'], str(e)))
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

    def _create_result_dict(self, changed):
        self.result['changed'] = changed
        if self.module.params['state'] == 'absent':
            self.result['hostgroup_details'] = {}
        else:
            if self.module.params['hostgroup_name']:
                hostgroup_id = self.get_hostgroup_id_by_name(
                    self.module.params['hostgroup_name'])
                self.result['hostgroup_details'] = self.get_hostgroup(
                    hostgroup_id)
            elif self.module.params['hostgroup_id']:
                self.result['hostgroup_details'] = self.get_hostgroup(
                    self.module.params['hostgroup_id'])

    def perform_module_operation(self):
        '''
        Perform different actions on host group based on user parameters
        chosen in playbook
        '''
        state = self.module.params['state']
        host_state = self.module.params['host_state']
        hostgroup_name = self.module.params['hostgroup_name']
        hostgroup_id = self.module.params['hostgroup_id']
        hosts = self.module.params['hosts']
        new_name = self.module.params['new_name']

        if hostgroup_name and hostgroup_id:
            error_msg = (
                "Operation on host group failed as both hostgroup_id and "
                "hostgroup_name are specified. Please specify either of "
                "them")
            LOG.error(error_msg)
            self.module.fail_json(msg=error_msg)

        if hostgroup_name:
            hostgroup_id = self.get_hostgroup_id_by_name(hostgroup_name)
        if hostgroup_id:
            hostgroup = self.get_hostgroup(hostgroup_id)
        else:
            hostgroup = None
        changed = False
        host_ids_list=[]
        if hosts:
            host_ids_list = self.create_host_list(hosts)

        if state == 'present' and not hostgroup and hostgroup_name:
            LOG.info('Creating host group {0}'.format(hostgroup_name))
            changed = self.create_hostgroup(hostgroup_name, host_ids_list)
            if changed:
                hostgroup_id = self.get_hostgroup_id_by_name(hostgroup_name)

        if (state == 'present' and hostgroup and host_state ==
                'present-in-group' and host_ids_list and len(host_ids_list) > 0):
            LOG.info('Adding hosts to host group {0}'.format(hostgroup['name']))
            changed = (
                self.add_hostgroup_hosts(
                    hostgroup,
                    hosts=host_ids_list) or changed)

        if (state == 'present' and hostgroup and host_state ==
                'absent-in-group' and host_ids_list and len(host_ids_list) > 0):
            LOG.info(
                'Removing hosts from host group {0}'.format(hostgroup['name']))
            changed = (
                self.remove_hostgroup_hosts(
                    hostgroup,
                    hosts=host_ids_list) or changed)

        if state == 'present' and hostgroup and new_name:
            if hostgroup['name'] != new_name:
                LOG.info(
                    'Renaming host group {0} to {1}'.format(
                        hostgroup['name'], new_name))
                changed = self.rename_hostgroup(hostgroup, new_name)
                if changed:
                    self.module.params['hostgroup_name'] = new_name

        if state == 'absent' and hostgroup:
            LOG.info('Deleting host group {0} '.format(hostgroup['name']))
            changed = self.delete_hostgroup(hostgroup) or changed

        self._create_result_dict(changed)
        # Update the module's final state
        LOG.info('changed {0}'.format(changed))
        self.module.exit_json(**self.result)


def main():
    ''' Create PowerStore host group object and perform action on it
        based on user input from playbook'''
    obj = PowerStoreHostgroup()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()