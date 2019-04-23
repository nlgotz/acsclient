import requests
from jinja2 import Environment, FileSystemLoader
import os


class ACSClient(object):

    _object_types = ['Common/AcsVersion', 'Common/ServiceLocation',
                     'Common/ErrorMessage', 'Identity/User', 'Identity/IdentityGroup',
                     'NetworkDevice/Device', 'NetworkDevice/DeviceGroup',
                     'Host']

    _function_types = ['all', 'name', 'id', 'op']

    def __init__(self, hostname, username, password,
                 hide_urllib_warnings=False):
        """ Class initialization method

        :param hostname: Hostname or IP Address of Cisco ACS 5.6 Sever
        :type hostname: str or unicode
        :param username: Cisco ACS admin user name
        :type username: str or unicode
        :param password: Cisco ACS admin user password
        :type password: str or unicode
        :param hide_urllib_warnings: Hide urllib3 warnings (optional)
        :type hide_urllib_warnings: boolean
        """
        self.url = "https://%s/Rest/" % hostname
        self.credentials = (username, password)
        self.session = requests.Session()
        if hide_urllib_warnings:
            #############################################################################
            # Disable "InsecureRequestWarning: Unverified HTTPS request is being made."
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
            #############################################################################

    def _req(self, method, frag, data=None):
        """ Creates the XML REST request to the Cisco ACS 5.6 Server

        :param method: HTTP Method to use (GET, POST, DELETE, PUT)
        :type method: str or unicode
        :param frag: URL fragment for request
        :type frag: str or unicode
        :param data: XML data to send to the server (optional)
        :type data: str or unicode
        """
        method = method.lower()
        headers = {'Content-Type': 'application/xml'}
        ssl_check = False
        self.session.auth = self.credentials
        if method == 'get':
            return self.session.get(self.url + frag, verify=ssl_check, data=data, headers=headers)
        elif method == 'post':
            return self.session.post(self.url + frag, verify=ssl_check, data=data, headers=headers)
        elif method == 'put':
            return self.session.put(self.url + frag, verify=ssl_check, data=data, headers=headers)
        elif method == 'delete':
            return self.session.delete(self.url + frag, verify=ssl_check, data=data, headers=headers)

    def _frag(self, object_type, func, var=None):
        """ Creates the proper URL fragment for HTTP requests

        :param object_type: Cisco ACS Object Type
        :type object_type: str or unicode
        :param func: ACS method function
        :type func: str or unicode
        :param var: ACS variable either the name or id
        :type var: str or unicode
        """
        try:
            if object_type in self._object_types:
                if func in self._function_types:
                    if func == "all":
                        frag = object_type
                    elif func == 'op':
                        frag = object_type + "/" + func + "/query"
                    else:
                        frag = object_type + "/" + func + "/" + str(var)
                    return frag
                else:
                    raise Exception
            else:
                raise Exception
        except (TypeError, Exception):
            print("Invalid object_type or function")

    def create(self, object_type, data):
        """ Create object on the ACS Server

        :param object_type: Cisco ACS Object Type
        :type object_type: str or unicode
        :param data: XML data to send to the ACS Server
        :type data: str or unicode
        """
        return self._req("POST", object_type, data)

    def read(self, object_type, func="all", var=None):
        """ Read data from ACS Server

        :param object_type: Cisco ACS Object Type
        :type object_type: str or unicode
        :param func: ACS method function (optional)
        :type func: str or unicode
        :param var: ACS variable either the name or id (optional)
        :type var: str or unicode
        """
        return self._req("GET", self._frag(object_type, func, var))

    def update(self, object_type, data):
        """ Update object on the ACS Server

        :param object_type: Cisco ACS Object Type
        :type object_type: str or unicode
        :param data: XML data to send to the ACS Server
        :type data: str or unicode
        """
        return self._req("PUT", object_type, data)

    def delete(self, object_type, func, var):
        """ Delete object on the ACS Server

        :param object_type: Cisco ACS Object Type
        :type object_type: str or unicode
        :param func: ACS method function
        :type func: str or unicode
        :param var: ACS variable either the name or id
        :type var: str, unicode, or int
        """
        return self._req("DELETE", self._frag(object_type, func, var))

    def create_device_group(self, name, group_type, description=""):
        """ Create ACS Device Group

        Create a new Device Group on the server. This will generate the proper
        XML to pass to the server.

        :param name: Full name of the Device Group
        :type name: str or unicode
        :param group_type: Device Group Type
        :type group_type: str or unicode
        :param description: Group Description (optional)
        :type description: str or unicode
        :returns: HTTP Response code
        :rtype: requests.models.Response
        """
        ENV = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "templates")))
        template = ENV.get_template("devicegroup.j2")
        var = dict(name=name, group_type=group_type, description=description)
        data = template.render(config=var)
        return self.create("NetworkDevice/DeviceGroup", data)

    def create_tacacs_device(self, name, groups, secret, ip, description="", mask=32):
        """ Create a new Device with TACACS

        :param name: Device name
        :type name: str or unicode
        :param groups: Groups list
        :type groups: dict
        :param secret: TACACS secret key
        :type secret: str or unicode
        :param ip: Device IP address
        :type ip: str or unicode
        :param description: Device description field (optional)
        :type description: str or unicode
        :param mask: Device IP mask (optional)
        :type mask: int
        """
        ENV = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "templates")))
        template = ENV.get_template("device.j2")
        var = dict(name=name, ip=ip, mask=mask, secret=secret, groups=groups, description=description)
        data = template.render(config=var)
        return self.create("NetworkDevice/Device", data)

    def create_radius_device(self, name, groups, secret, ip, mask=32):
        """ Create a new Device with TACACS

        :param name: Device name
        :type name: str or unicode
        :param groups: Groups list
        :type groups: dict
        :param secret: Radius secret key
        :type secret: str or unicode
        :param ip: Device IP address
        :type ip: str or unicode
        :param mask: Device IP mask (optional)
        :type mask: int
        """
        ENV = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "templates")))
        template = ENV.get_template("radius_device.j2")
        var = dict(name=name, ip=ip, mask=mask, secret=secret, groups=groups)
        data = template.render(config=var)
        return self.create("NetworkDevice/Device", data)

    def create_device_simple(self, name, secret, ip, location, device_type):
        """ Simple way to create a new Device with TACACS

        :param name: Device name
        :type name: str or unicode
        :param secret: TACACS secret key
        :type secret: str or unicode
        :param ip: Device IP address
        :type ip: str or unicode
        :param location: Device Group Location
        :type location: str or unicode
        :param device_type: Device Group Device Type
        :type device_type: str or unicode
        """
        groups = [
            {"name": "All Locations:" + location,
                "type": "Location"},
            {"name": "All Device Types:" + device_type,
                "type": "Device Type"},
        ]
        return self.create_tacacs_device(name, groups, secret, ip)

    def search_tacacs(self, object_type, key, value, condition):
        """
        Search for a value within TACACS

        The following conditions are supported for filtering:
            - CONTAINS
            - DOES_NOT_CONTAIN
            - ENDS_WITH
            - EQUALS
            - NOT_EMPTY
            - NOT_EQUALS
            - STARTS_WITH

        :param object_type: Cisco ACS Object Type
        :type object_type: str or unicode
        :param key: Key to search
        :type key: str or unicode
        :param value: value to search for
        :type value: str
        :param condition: condition to match
        :type condition: str
        """
        ENV = Environment(loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "templates")))
        template = ENV.get_template("search.j2")
        var = dict(key=key, filter=condition, value=value)
        data = template.render(config=var)
        return self.update(self._frag(object_type, 'op'), data)
