
import json
import requests
import os
from rest_framework.exceptions import PermissionDenied


class OPAAuthService:

    def __init__(self):

        pass
    @staticmethod
    def request_auth(user, resource, action):

        try:
            input = json.dumps({
                "user": user,
                "resource": resource,
                "action": action
            }, indent=2)
            url = os.environ.get("OPA_URL", "http://localhost:8181")
            response = requests.post(url, data=input)
        except Exception as e:
            raise e

        if response.status_code != 200:
            raise PermissionDenied

        allowed = response.json()
        return allowed