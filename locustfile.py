import logging
import login_credentials
from locust import HttpUser, task, between


class UserBehavior(HttpUser):
    wait_time = between(0.5, 1)
    host = "<URL>"

    @task
    def v1_token_endpoint(self):
        CLIENT_ID = login_credentials.CLIENT_ID
        PASSWORD = login_credentials.CLIENT_SECRET
        url = "<URL for login>"
        url = url + "&client_id=" + CLIENT_ID + "&client_secret=" + PASSWORD

        with self.client.post(url, name="v1/token", catch_response=True) as \
                response:
            # check for response content
            if 'token' not in response.text:
                logging.info("Response text is %s", response.text)
                response.failure = "Incorrect Response for v1/Token Endpoint"
            if response.status_code != 201:
                response.failure = "Incorrect response code for token"

    @task
    def v2_token_endpoint(self):
        self.CLIENT_ID = login_credentials.CLIENT_ID
        self.CLIENT_SECRET = login_credentials.CLIENT_SECRET
        self.secrets_body = {"client_id": self.CLIENT_ID,"client_secret": self.CLIENT_SECRET}
        url = "<URL for login>"
        with self.client.post(url, name="v2/token", data=self.secrets_body, catch_response=True) as response:
            if 'token' not in response.text:
                logging.info("Response text is %s", response.text)
                response.failure = "Incorrect response code for v2/Token endpoint"
            if response.status_code != 201:
                response.failure = "Incorrect response code for token"
