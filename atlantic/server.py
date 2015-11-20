from .utils import AtlanticBase

class AtlanticServer(AtlanticBase):
    def __init__(self, access_key, private_key):
        AtlanticBase.__init__(self, access_key, private_key)

    def run(self, servername, imageid, planname, vm_location,
            enablebackup="N", serverqty=1, cloneimage=None):
        """
        This method enables you to create new cloud servers by specifying a
        flexible set of configuration parameters.

        Link: https://www.atlantic.net/docs/api/?shell#run-instance
        """
        params = {
            "Action": "run-instance",
            "servername": servername,
            "imageid": imageid,
            "planname": planname,
            "vm_location": vm_location,
            "enablebackup": enablebackup,
            "serverqty": serverqty
        }
        if cloneimage:
            params.update({"cloneimage": cloneimage})
        return self.request(params).json()

    def list(self):
        """
        This method enables the client to retrieve the list of currently
        active cloud servers.

        Link: https://www.atlantic.net/docs/api/?shell#list-instances
        """
        params = {
            "Action": "list-instances"
        }
        return self.request(params).json()

    def describe(self, instanceid):
        """
        This method enables the you to retrieve the details of a specific
        cloud cerver.

        Link: https://www.atlantic.net/docs/api/?shell#describe-instance
        """
        params = {
            "Action": "describe-instance",
            "instanceid": instanceid
        }
        return self.request(params).json()

    def reboot(self, instanceid, reboottype="soft"):
        """
        This method enables the you to restart a specific cloud server.

        Link: https://www.atlantic.net/docs/api/?shell#reboot-instance
        """
        params = {
            "Action": "reboot-instance",
            "instanceid": instanceid,
            "reboottype": reboottype
        }
        return self.request(params).json()

    def terminate(self, instanceid):
        """
        This method enables the you to remove a specific cloud server.

        Link: https://www.atlantic.net/docs/api/?shell#terminate-instance
        """
        params = {
            "Action": "terminate-instance",
            "instanceid": instanceid
        }
        return self.request(params).json()
