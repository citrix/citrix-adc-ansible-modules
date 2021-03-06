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
module: citrix_adc_ssl_certkey
short_description: Manage ssl cerificate keys.
description:
    - Manage ssl cerificate keys.

version_added: "1.0.0"

author: George Nikolopoulos (@giorgos-nikolopoulos)

options:

    certkey:
        type: str
        description:
            - >-
                Name for the certificate and private-key pair. Must begin with an ASCII alphanumeric or underscore
                C(_) character, and must contain only ASCII alphanumeric, underscore C(_), hash C(#), period C(.), space C( ),
                colon C(:), at C(@), equals C(=), and hyphen C(-) characters. Cannot be changed after the certificate-key
                pair is created.
            - "The following requirement applies only to the Citrix ADC CLI:"
            - >-
                If the name includes one or more spaces, enclose the name in double or single quotation marks (for
                example, "my cert" or 'my cert').
            - "Minimum length = 1"

    cert:
        type: str
        description:
            - >-
                Name of and, optionally, path to the X509 certificate file that is used to form the certificate-key
                pair. The certificate file should be present on the appliance's hard-disk drive or solid-state drive.
                Storing a certificate in any location other than the default might cause inconsistency in a high
                availability setup. /nsconfig/ssl/ is the default path.
            - "Minimum length = 1"

    key:
        type: str
        description:
            - >-
                Name of and, optionally, path to the private-key file that is used to form the certificate-key pair.
                The certificate file should be present on the appliance's hard-disk drive or solid-state drive.
                Storing a certificate in any location other than the default might cause inconsistency in a high
                availability setup. /nsconfig/ssl/ is the default path.
            - "Minimum length = 1"

    password:
        type: bool
        description:
            - >-
                Passphrase that was used to encrypt the private-key. Use this option to load encrypted private-keys
                in PEM format.

    inform:
        type: str
        choices:
            - 'DER'
            - 'PEM'
            - 'PFX'
        description:
            - >-
                Input format of the certificate and the private-key files. The three formats supported by the
                appliance are:
            - "PEM - Privacy Enhanced Mail"
            - "DER - Distinguished Encoding Rule"
            - "PFX - Personal Information Exchange."

    passplain:
        type: str
        description:
            - >-
                Pass phrase used to encrypt the private-key. Required when adding an encrypted private-key in PEM
                format.
            - "Minimum length = 1"

    expirymonitor:
        type: str
        choices:
            - 'enabled'
            - 'disabled'
        description:
            - "Issue an alert when the certificate is about to expire."

    notificationperiod:
        type: float
        description:
            - >-
                Time, in number of days, before certificate expiration, at which to generate an alert that the
                certificate is about to expire.
            - "Minimum value = C(10)"
            - "Maximum value = C(100)"


extends_documentation_fragment: citrix.adc.citrixadc
requirements:
    - nitro python sdk
'''

EXAMPLES = '''

- name: Setup ssl certkey
  delegate_to: localhost
  citrix_adc_ssl_certkey:
    nitro_user: nsroot
    nitro_pass: nsroot
    nsip: 172.18.0.2

    certkey: certirificate_1
    cert: server.crt
    key: server.key
    expirymonitor: enabled
    notificationperiod: 30
    inform: PEM
    password: False
    passplain: somesecret
'''

RETURN = '''
loglines:
    description: list of logged messages by the module
    returned: always
    type: list
    sample: "['message 1', 'message 2']"

msg:
    description: Message detailing the failure reason
    returned: failure
    type: str
    sample: "Action does not exist"

diff:
    description: List of differences between the actual configured object and the configuration specified in the module
    returned: failure
    type: dict
    sample: "{ 'targetlbvserver': 'difference. ours: (str) server1 other: (str) server2' }"
'''

try:
    from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey import sslcertkey
    from nssrc.com.citrix.netscaler.nitro.exception.nitro_exception import nitro_exception
    PYTHON_SDK_IMPORTED = True
except ImportError as e:
    PYTHON_SDK_IMPORTED = False

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.citrix.adc.plugins.module_utils.citrix_adc import (
    ConfigProxy,
    get_nitro_client,
    netscaler_common_arguments,
    log,
    loglines,
    get_immutables_intersection
)


def key_exists(client, module):
    log('Checking if key exists')
    log('certkey is %s' % module.params['certkey'])
    all_certificates = sslcertkey.get(client)
    certkeys = [item.certkey for item in all_certificates]
    if module.params['certkey'] in certkeys:
        return True
    else:
        return False


def key_identical(client, module, sslcertkey_proxy):
    log('Checking if configured key is identical')
    sslcertkey_list = sslcertkey.get_filtered(client, 'certkey:%s' % module.params['certkey'])
    diff_dict = sslcertkey_proxy.diff_object(sslcertkey_list[0])
    if 'password' in diff_dict:
        del diff_dict['password']
    if 'passplain' in diff_dict:
        del diff_dict['passplain']
    if 'notificationperiod' in diff_dict:
        del diff_dict['notificationperiod']
    if len(diff_dict) == 0:
        return True
    else:
        return False


def diff_list(client, module, sslcertkey_proxy):
    sslcertkey_list = sslcertkey.get_filtered(client, 'certkey:%s' % module.params['certkey'])
    return sslcertkey_proxy.diff_object(sslcertkey_list[0])


def main():

    module_specific_arguments = dict(
        certkey=dict(type='str'),
        cert=dict(type='str'),
        key=dict(type='str'),
        password=dict(type='bool'),
        inform=dict(
            type='str',
            choices=[
                'DER',
                'PEM',
                'PFX',
            ]
        ),
        passplain=dict(
            type='str',
            no_log=True,
        ),
        expirymonitor=dict(
            type='str',
            choices=[
                'enabled',
                'disabled',
            ]
        ),
        notificationperiod=dict(type='float'),
    )

    argument_spec = dict()

    argument_spec.update(netscaler_common_arguments)

    argument_spec.update(module_specific_arguments)

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )
    module_result = dict(
        changed=False,
        failed=False,
        loglines=loglines,
    )

    # Fail the module if imports failed
    if not PYTHON_SDK_IMPORTED:
        module.fail_json(msg='Could not load nitro python sdk')

    # Fallthrough to rest of execution
    client = get_nitro_client(module)

    if not module.params['mas_proxy_call']:
        try:
            client.login()
        except nitro_exception as e:
            msg = "nitro exception during login. errorcode=%s, message=%s" % (str(e.errorcode), e.message)
            module.fail_json(msg=msg)
        except Exception as e:
            if str(type(e)) == "<class 'requests.exceptions.ConnectionError'>":
                module.fail_json(msg='Connection error %s' % str(e))
            elif str(type(e)) == "<class 'requests.exceptions.SSLError'>":
                module.fail_json(msg='SSL Error %s' % str(e))
            else:
                module.fail_json(msg='Unexpected error during login %s' % str(e))

    readwrite_attrs = [
        'certkey',
        'cert',
        'key',
        'password',
        'inform',
        'passplain',
        'expirymonitor',
        'notificationperiod',
    ]

    readonly_attrs = [
        'signaturealg',
        'certificatetype',
        'serial',
        'issuer',
        'clientcertnotbefore',
        'clientcertnotafter',
        'daystoexpiration',
        'subject',
        'publickey',
        'publickeysize',
        'version',
        'priority',
        'status',
        'passcrypt',
        'data',
        'servicename',
    ]

    immutable_attrs = [
        'certkey',
        'cert',
        'key',
        'password',
        'inform',
        'passplain',
    ]

    transforms = {
        'expirymonitor': [lambda v: v.upper()],
    }

    # Instantiate config proxy
    sslcertkey_proxy = ConfigProxy(
        actual=sslcertkey(),
        client=client,
        attribute_values_dict=module.params,
        readwrite_attrs=readwrite_attrs,
        readonly_attrs=readonly_attrs,
        immutable_attrs=immutable_attrs,
        transforms=transforms,
    )

    try:

        if module.params['state'] == 'present':
            log('Applying actions for state present')
            if not key_exists(client, module):
                if not module.check_mode:
                    log('Adding certificate key')
                    sslcertkey_proxy.add()
                    if module.params['save_config']:
                        client.save_config()
                module_result['changed'] = True
            elif not key_identical(client, module, sslcertkey_proxy):

                # Check if we try to change value of immutable attributes
                immutables_changed = get_immutables_intersection(sslcertkey_proxy, diff_list(client, module, sslcertkey_proxy).keys())
                if immutables_changed != []:
                    module.fail_json(
                        msg='Cannot update immutable attributes %s' % (immutables_changed,),
                        diff=diff_list(client, module, sslcertkey_proxy),
                        **module_result
                    )

                if not module.check_mode:
                    sslcertkey_proxy.update()
                    if module.params['save_config']:
                        client.save_config()
                module_result['changed'] = True
            else:
                module_result['changed'] = False

            # Sanity check for state
            if not module.check_mode:
                log('Sanity checks for state present')
                if not key_exists(client, module):
                    module.fail_json(msg='SSL certkey does not exist')
                if not key_identical(client, module, sslcertkey_proxy):
                    module.fail_json(msg='SSL certkey differs from configured', diff=diff_list(client, module, sslcertkey_proxy))

        elif module.params['state'] == 'absent':
            log('Applying actions for state absent')
            if key_exists(client, module):
                log('key exists in state=absent')
                if not module.check_mode:
                    sslcertkey_proxy.delete()
                    if module.params['save_config']:
                        client.save_config()
                module_result['changed'] = True
            else:
                log('key does not exist in state=absent')
                module_result['changed'] = False

            # Sanity check for state
            if not module.check_mode:
                log('Sanity checks for state absent')
                if key_exists(client, module):
                    module.fail_json(msg='SSL certkey still exists')

    except nitro_exception as e:
        msg = "nitro exception errorcode=%s, message=%s" % (str(e.errorcode), e.message)
        module.fail_json(msg=msg, **module_result)

    if not module.params['mas_proxy_call']:
        client.logout()

    module.exit_json(**module_result)


if __name__ == "__main__":
    main()
