from .utils import AtlanticBase

class AtlanticSSHKey(AtlanticBase):
    def __init__(self, access_key, private_key):
        AtlanticBase.__init__(self, access_key, private_key)

    def list(self):
        """
        This method enables the client to retrieve the details of all
        SSH Keys that they have added to their account. The client can
        then specify an SSH Key to embed into their Cloud Server at
        the time of creation.

        Link: https://www.atlantic.net/docs/api/?shell#list-sshkeys
        """
        params = {
            "Action": "list-sshkeys"
        }
        return self.request(params)
