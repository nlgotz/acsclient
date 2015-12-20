import requests
from jinja2 import Environment, FileSystemLoader
import os


class ACSClient(object):

    _object_types = ['ACSVersion', 'ServiceLocation', 'ErrorMessage',
                     'User', 'IdentityGroup', 'NetworkDevice/Device',
                     'NetworkDevice/DeviceGroup', 'Host']

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

    def create_device_group(self, name, group_type):
        ENV = Environment(loader=FileSystemLoader(
              os.path.join(os.path.dirname(__file__), "templates")))
        template = ENV.get_template("devicegroup.j2")
        var = dict(name=name, group_type=group_type)
        data = template.render(config=var)
        return self.create("NetworkDevice/DeviceGroup", data)

    def create_tacacs_device(self, name, ip, secret, groups):
        ENV = Environment(loader=FileSystemLoader(
              os.path.join(os.path.dirname(__file__), "templates")))
        template = ENV.get_template("device.j2")
        var = dict(name=name, ip=ip, secret=secret, groups=groups)
        data = template.render(config=var)
        return self.create("NetworkDevice/Device", data)
