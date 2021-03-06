#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Citrix Systems, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: citrix_adm_login
short_description: Login to a Citrix ADM instance.
description:
    - Login to a Citrix ADM instance.
    - The session token is returned in the module result.

author:
    - George Nikolopoulos (@giorgos-nikolopoulos)

version_added: "1.0.0"

extends_documentation_fragment: citrix.adm.citrixadm
'''

EXAMPLES = '''
- hosts: citrix_adm

  gather_facts: False

  tasks:
    - name: Login to Citrix ADM
      delegate_to: localhost
      register: login_result
      citrix_adm_login:
        mas_ip: "{{ mas_ip }}"
        mas_user: "{{ mas_user }}"
        mas_pass: "{{ mas_pass }}"

    - name: Setup mpsuser
      delegate_to: localhost
      citrix_adm_mpsuser:
        mas_ip: "{{ mas_ip }}"
        mas_auth_token: "{{ login_result.session_id }}"

        state: absent

        name: playbook_test_mpsuser_2
        password: 1234567

        session_timeout: 10
        session_timeout_unit: Minutes
        external_authentication: false
        enable_session_timeout: true
'''

RETURN = '''
loglines:
    description: list of logged messages by the module
    returned: always
    type: list
    sample: ['message 1', 'message 2']

msg:
    description: Message detailing the failure reason
    returned: failure
    type: str
    sample: "Action does not exist"
session_id:
    description: The session id to be used as authentication token on subsequent module calls.
    returned: success
    type: str
    sample: "##1A44A1437AD74D6158FC51FC95A0009D93FA8C1A8E2CCCEF9F4FD4DA2039"

'''

import copy

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.citrix.adm.plugins.module_utils.citrix_adm import (
    NitroAPIFetcher,
    NitroException,
    netscaler_common_arguments,
    log,
    loglines
)


def main():

    module = AnsibleModule(
        argument_spec=netscaler_common_arguments,
        supports_check_mode=False,
    )

    try:
        fetcher = NitroAPIFetcher(module, api_path='nitro/v2/config')

        module_result = dict(
            changed=False,
            failed=False,
            loglines=loglines,
        )

        post_data = {
            'login': {
                'username': module.params['nitro_user'],
                'password': module.params['nitro_pass'],
            }
        }
        result = fetcher.post(post_data=post_data, resource='login')
        log('POST result %s' % result)
        log(result['nitro_errorcode'])
        if result['nitro_errorcode'] not in (None, 0):
            errorcode = result.get('nitro_errorcode')
            message = result.get('nitro_message')
            severity = result.get('nitro_severity')
            msg = "nitro exception errorcode=%s, message=%s, severity=%s" % (str(errorcode), message, severity)
            module.fail_json(msg=msg, **module_result)
        else:
            module_result.update(dict(session_id=result['data']['login'][0]['sessionid']))
            module.exit_json(**module_result)
    except Exception as e:
        msg = 'Exception %s: %s' % (type(e), str(e))
        module.fail_json(msg=msg, **module_result)


if __name__ == '__main__':
    main()
