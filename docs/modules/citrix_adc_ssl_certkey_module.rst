:orphan:

.. _citrix_adc_ssl_certkey_module:

citrix_adc_ssl_certkey - Manage ssl cerificate keys.
++++++++++++++++++++++++++++++++++++++++++++++++++++

.. versionadded:: 1.0.0

.. contents::
   :local:
   :depth: 2

Synopsis
--------
- Manage ssl cerificate keys.



Requirements
~~~~~~~~~~~~
The below requirements are needed on the host that executes this module.

- nitro python sdk


Parameters
----------

.. list-table::
    :widths: 10 10 60
    :header-rows: 1

    * - Parameter
      - Choices/Defaults
      - Comment
    * - cert

        *(str)*
      -
      - Name of and, optionally, path to the X509 certificate file that is used to form the certificate-key pair. The certificate file should be present on the appliance's hard-disk drive or solid-state drive. Storing a certificate in any location other than the default might cause inconsistency in a high availability setup. /nsconfig/ssl/ is the default path.

        Minimum length = 1
    * - certkey

        *(str)*
      -
      - Name for the certificate and private-key pair. Must begin with an ASCII alphanumeric or underscore ``_`` character, and must contain only ASCII alphanumeric, underscore ``_``, hash ``#``, period ``.``, space `` ``, colon ``:``, at ``@``, equals ``=``, and hyphen ``-`` characters. Cannot be changed after the certificate-key pair is created.

        The following requirement applies only to the Citrix ADC CLI:

        If the name includes one or more spaces, enclose the name in double or single quotation marks (for example, "my cert" or 'my cert').

        Minimum length = 1
    * - expirymonitor

        *(str)*
      - Choices:

          - enabled
          - disabled
      - Issue an alert when the certificate is about to expire.
    * - inform

        *(str)*
      - Choices:

          - DER
          - PEM
          - PFX
      - Input format of the certificate and the private-key files. The three formats supported by the appliance are:

        PEM - Privacy Enhanced Mail

        DER - Distinguished Encoding Rule

        PFX - Personal Information Exchange.
    * - instance_ip

        *(str)*

        *(added in 2.6.0)*
      -
      - The target Citrix ADC instance ip address to which all underlying NITRO API calls will be proxied to.

        It is meaningful only when having set ``mas_proxy_call`` to ``true``
    * - key

        *(str)*
      -
      - Name of and, optionally, path to the private-key file that is used to form the certificate-key pair. The certificate file should be present on the appliance's hard-disk drive or solid-state drive. Storing a certificate in any location other than the default might cause inconsistency in a high availability setup. /nsconfig/ssl/ is the default path.

        Minimum length = 1
    * - mas_proxy_call

        *(bool)*

        *(added in 2.6.0)*
      - Default:

        *False*
      - If true the underlying NITRO API calls made by the module will be proxied through a Citrix ADM node to the target Citrix ADC instance.

        When true you must also define the following options: ``nitro_auth_token``, ``instance_ip``.
    * - nitro_auth_token

        *(str)*

        *(added in 2.6.0)*
      -
      - The authentication token provided by a login operation.
    * - nitro_pass

        *(str)*
      -
      - The password with which to authenticate to the Citrix ADC node.
    * - nitro_protocol

        *(str)*
      - Choices:

          - http
          - https (*default*)
      - Which protocol to use when accessing the nitro API objects.
    * - nitro_timeout

        *(float)*
      - Default:

        *310*
      - Time in seconds until a timeout error is thrown when establishing a new session with Citrix ADC
    * - nitro_user

        *(str)*
      -
      - The username with which to authenticate to the Citrix ADC node.
    * - notificationperiod

        *(float)*
      -
      - Time, in number of days, before certificate expiration, at which to generate an alert that the certificate is about to expire.

        Minimum value = ``10``

        Maximum value = ``100``
    * - nsip

        *(str)*
      -
      - The ip address of the Citrix ADC appliance where the nitro API calls will be made.

        The port can be specified with the colon (:). E.g. 192.168.1.1:555.
    * - passplain

        *(str)*
      -
      - Pass phrase used to encrypt the private-key. Required when adding an encrypted private-key in PEM format.

        Minimum length = 1
    * - password

        *(bool)*
      -
      - Passphrase that was used to encrypt the private-key. Use this option to load encrypted private-keys in PEM format.
    * - save_config

        *(bool)*
      - Default:

        *True*
      - If true the module will save the configuration on the Citrix ADC node if it makes any changes.

        The module will not save the configuration on the Citrix ADC node if it made no changes.
    * - state

        *(str)*
      - Choices:

          - present (*default*)
          - absent
      - The state of the resource being configured by the module on the Citrix ADC node.

        When present the resource will be created if needed and configured according to the module's parameters.

        When absent the resource will be deleted from the Citrix ADC node.
    * - validate_certs

        *(bool)*
      - Default:

        *yes*
      - If ``no``, SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.



Examples
--------

.. code-block:: yaml+jinja
    
    
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


Return Values
-------------
.. list-table::
    :widths: 10 10 60
    :header-rows: 1

    * - Key
      - Returned
      - Description
    * - diff

        *(dict)*
      - failure
      - List of differences between the actual configured object and the configuration specified in the module

        **Sample:**

        { 'targetlbvserver': 'difference. ours: (str) server1 other: (str) server2' }
    * - loglines

        *(list)*
      - always
      - list of logged messages by the module

        **Sample:**

        ['message 1', 'message 2']
    * - msg

        *(str)*
      - failure
      - Message detailing the failure reason

        **Sample:**

        Action does not exist
