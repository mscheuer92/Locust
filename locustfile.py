import logging
from locust import HttpUser, task, between, events


class UserBehavior(HttpUser):
    wait_time = between(0.5, 1)
    host = "<URL here>"

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.stats = None

    def on_start(self):
        # Called when Locust is started before tasks are schedule
        pass

    def on_stop(self):
        # Called when TaskSet is stopping
        pass

    @task
    def token_endpoint(self):
        self.client.get("<URI HERE>")

    @task
    def auth_title(self):
        with self.client.get("<URI here>", name="<URI here>", catch_response=True) as \
                response:
            # check for response content
            if '{"email":<"expected response here">}' not in response.text:
                response.failure = "Incorrect response for email"
            if response.status_code != 200:
                response.failure = "Incorrect response code for email"

    @events.test_stop.add_listener
    def _(environment):
        if environment.stats.total.fail.ratio > 0.01:
            logging.error("Test failed due to failure ratio > 1%")
            environment.process_exit_code = 1
        elif environment.stats.total.avg_response_time > 200:
            logging.error("Test failed due to average response time ratio > 200 ns")
            environment.process_exit_code = 1
        else:
            environment.process_exit_code = 0
