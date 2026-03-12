from locust import HttpUser, task, between


class WebsiteUser(HttpUser):

    host = "http://127.0.0.1:8000"

    @task
    def index(self):
        self.client.get("/")