ACSClient
==========

ACSClient is a Python wrapper for accessing a Cisco ACS server. I only have
access to a Cisco ACS 5.6 Server, so any previous or future ACS versions may not
work with this package.

Install
-------
ACSClient should work with both Python2 and Python3


Python2 Install from pip::

    pip install acsclient

Python3 Install from pip3::

    pip3 install acsclient

Or you can run build this locally::

    git clone https://github.com/nlgotz/acsclient.git
    python setup.py install



How to Use
----------

Example::

    if sys.version_info[0] == 3:
        from acsclient.acsclient import ACSClient
        acs = ACSClient("192.168.1.11", "api", "password123", True)
    else:
        import acsclient
        acs = acsclient.ACSClient("192.168.1.11", "api", "password123", True)

    #Read all Devices
    r = acs.read("NetworkDevice/Device")
    print r.content

    #Read Specific Device
    r = acs.read("NetworkDevice/Device", "name", "ROUTER01")
    print r.content

    #Create new Device
    groups = [
            {"name": "All Locations:Site", "type": "Location"},
            {"name": "All Device Types:My Device", "type": "Device Type"},
            {"name": "CO:My Co", "type": "Company"},
    ]
    r = acs.create_tacacs_device("ROUTER02", groups, "s3cr37", "10.1.1.1")

License
-------

    This software is licensed under the Apache License, version 2 ("ALv2"), quoted below.

    Copyright © 2015 Nathan Gotz.  All rights reserved.

    Licensed under the Apache License, Version 2.0 (the "License"); you may not
    use this file except in compliance with the License. You may obtain a copy of
    the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
    License for the specific language governing permissions and limitations under
    the License.
