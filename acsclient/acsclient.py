import requests
from jinja2 import Environment, FileSystemLoader
import os


class ACSClient(object):

    _object_types = ['Common/ACSVersion', 'Common/ServiceLocation',
                     'ErrorMessage', 'User', 'IdentityGroup',
                     'NetworkDevice/Device', 'NetworkDevice/DeviceGroup',
                     'Host']

    _function_types = ['all', 'name', 'id']

    def __init__(self, hostname, username, password,
                 hide_urllib_warnings=False):
        """ Class initialization method
        :param hostname: Hostname or IP Address of Cisco ACS 5.6 Sever
        :param username: Cisco ACS admin user name
        :param password: Cisco ACS admin user password
        :param hide_urllib_warnings: Hide urllib3 warnings when running queries
                                     (optional)
        """
        self.url = "https://%s/Rest/" % (hostname)
        self.credentials = (username, password)
        if hide_urllib_warnings:
            requests.packages.urllib3.disable_warnings()

    def _req(self, method, frag, data=None):
        """ Creates the XML REST request to the Cisco ACS 5.6 Server
        :param method: HTTP Method to use (GET, POST, DELETE, PUT)
        :param frag: URL fragment for request
        :param data: XML data to send to the server (optional)
        """
        return requests.request(method, self.url + frag,
                                data=data,
                                verify=False,
                                auth=self.credentials,
                                headers={'Content-Type': 'application/xml'})

    def _frag(self, object_type, func, var):
        """ Creates the proper URL fragment for HTTP requests
        :param object_type: Cisco ACS Object Type
        :param func: ACS method function
        :param var: ACS variable either the name or id
        """
        try:
            if object_type in self._object_types:
                if func in self._function_types:
                    if func == "all":
                        frag = object_type
                    else:
                        frag = object_type + "/" + func + "/" + str(var)
                    return frag
            else:
                raise Exception
        except Exception:
            print "Invalid object_type or function"

    def create(self, object_type, data):
        """ Create object on the ACS Server
        :param object_type: Cisco ACS Object Type
        :param data: XML data to send to the ACS Server
        """
        return self._req("POST", object_type, data)

    def read(self, object_type, func="all", var=None):
        """ Read data from ACS Server
        :param object_type: Cisco ACS Object Type
        :param func: ACS method function (optional)
        :param var: ACS variable either the name or id (optional)
        """
        return self._req("GET", self._frag(object_type, func, var))

    def update(self, object_type, data):
        """ Update object on the ACS Server
        :param object_type: Cisco ACS Object Type
        :param data: XML data to send to the ACS Server
        """
        return self._req("PUT", object_type, data)

    def delete(self, object_type, func, var):
        """ Delete object on the ACS Server
        :param object_type: Cisco ACS Object Type
        :param func: ACS method function
        :param var: ACS variable either the name or id
        """
        return self._req("DELETE", self._frag(object_type, func, var))

    def create_device_group(self, name, group_NetworkDevice/Devicetype):
        """ Create a Device Group on the ACS Server.
        This generates the proper XML to pass to the server
        :param name: Full name of the Device Group
        :param group_type: Type of ACS Device Group
                (Location and Device type are the defaults in ACS 5.6)
        """
        ENV = Environment(loader=FileSystemLoader(
              os.path.join(os.path.dirname(__file__), "templates")))
        template = ENV.get_template("devicegroup.j2")
        var = dict(name=name, group_type=group_type)
        data = template.render(config=var)
        return self.create("NetworkDevice/DeviceGroup", data)

    def create_tacacs_device(self, name, groups, secret, ip, mask=32):
        """ Create a new Device with TACACS
        :param name: Device name
        :param groups: dict for the groups. The keys are name and type.
                The name needs to be the full name
        :param secret: TACACS secret key
        :param ip: Device IP address
        :param mask: Device IP mask (optional) (defaults to a /32)
        """
        ENV = Environment(loader=FileSystemLoader(
              os.path.join(os.path.dirname(__file__), "templates")))
        template = ENV.get_template("device.j2")
        var = dict(name=name, ip=ip, mask=mask, secret=secret, groups=groups)
        data = template.render(config=var)
        return self.create("NetworkDevice/Device", data)

    def create_device_simple(self, name, secret, ip, location, device_type):
        """ Simple way to create a new Device with TACACS
        :param name: Device name
        :param secret: TACACS secret key
        :param ip: Device IP address
        :param location: Device Group Location
        :param device_type: Device Group Device Type
        """
        groups = [
                {"name": "All Locations:" + location,
                 "type": "Location"},
                {"name": "All Device Types:" + device_type,
                 "type": "Device Type"},
        ]
        return self.create_tacacs_device(name, groups, secret, ip)
