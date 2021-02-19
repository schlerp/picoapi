from threading import Thread
import requests
import time


class HealthCheck(Thread):
    def __init__(self, url: str, interval: int = 30):
        super().__init__()
        self.url = url
        self.interval = interval
        self._is_running = True
        self.healthy = True

    def get_health(self):
        return self.healthy

    def run(self):
        while self._is_running:
            try:
                resp = requests.get(self.url, timeout=3)
                status_code = resp.status_code
            except:
                status_code = 400
            self.healthy = (
                "healthy" if (status_code >= 200 and status_code < 300) else "unhealthy"
            )
            time.sleep(self.interval)

    def stop(self):
        self._is_running = False