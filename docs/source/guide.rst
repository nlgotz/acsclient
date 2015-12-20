Quick Start Guide
=================

ACSClient implements a CRUD interface to a defined Cisco ACS Server. There are 4
main accessible functions: create, read, update, and delete. There are also 3
"special" functions that make it easier to create devices and device groups.

Example::

    import acsclient
    acs = acsclient.ACSClient("192.168.1.11", "api", "password123", True)
    
    #Read all Devices
    r = acs.read("NetworkDevice/Device")
    print r.content
    
    #Read Specific Device
    r = acs.read("NetworkDevice/Device", "name", "ROUTER01")
    print r.content
    
    #Create new Device
    #This shows how to add non-default Device Group data
    groups = [
            {"name": "All Locations:Site", "type": "Location"},
            {"name": "All Device Types:My Device", "type": "Device Type"},
            {"name": "CO:My Co", "type": "Company"},
    ]
    r = acs.create_tacacs_device("ROUTER02", groups, "s3cr37", "10.1.1.1")
