from locust import HttpUser, task, between


class WebsiteUser(HttpUser):

    @task
    def index(self):
        self.client.get("/")