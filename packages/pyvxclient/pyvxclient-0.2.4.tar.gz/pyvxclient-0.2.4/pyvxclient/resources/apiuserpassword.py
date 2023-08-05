from pyvxclient.decorators import handle_response
from pyvxclient.resource import Resource


class ApiUserPassword(Resource):

    @handle_response
    def get(self, username_or_email, portal_url):
        return self.client.api.getApiUserPassword(username_or_email=username_or_email, url=portal_url).response()
