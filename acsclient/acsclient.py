import requests

class ACSClient(object):
    def __init__(self, hostname, username, password):
        self.url = "https://%s/Rest/" % (hostname)
        self.credentials = (username, password)
        
    def _req(self, method, frag, data=None):
        return requests.request(method, self.url + frag,
            data=data,
            verify=False,
            auth=self.credentials,
            headers={'Content-Type': 'application/xml'})
    
    def createDeviceGroup(self, name, grouptype):
        data = """
<ns1:deviceGroup xmlns:ns1="networkdevice.rest.mgmt.acs.nm.cisco.com">
        <description />
        <name>{name}</name>
        <groupType>{grouptype}</groupType>
</ns1:deviceGroup>
        """.format(
                name=name,
                grouptype=grouptype,
        )
        return self._req("POST", "NetworkDevice/DeviceGroup", data)
    
    def createDevice(self, name, location, devicetype, ip, secret):
        data = """
<ns1:device xmlns:ns1="networkdevice.rest.mgmt.acs.nm.cisco.com">
        <description />
        <name>{name}</name>
        <groupInfo>
            <groupName>All Locations:{location}</groupName>
            <groupType>Location</groupType>
        </groupInfo>
        <groupInfo>
            <groupName>All Device Types:{devicetype}</groupName>
            <groupType>Device Type</groupType>
        </groupInfo>
        <subnets>
            <ipAddress>{ip}</ipAddress>
            <netMask>32</netMask>
        </subnets>
        <tacacsConnection>
            <legacyTACACS>true</legacyTACACS>
            <sharedSecret>{secret}</sharedSecret>
            <singleConnect>false</singleConnect>
        </tacacsConnection>
</ns1:device>
        """.format(
                name=name,
                location=location,
                devicetype=devicetype,
                ip=ip,
                secret=secret
        )
        return self._req("POST", "NetworkDevice/Device", data)
