import socket
import requests
import threading

class NetworkInfo:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NetworkInfo, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.internet_status = None
        self.private_ip = None

    def check_network_info(self):
        self.internet_status = self._check_internet()
        self.private_ip = self._get_private_ip()

    def _check_internet(self):
        try:
            requests.get('http://www.google.com', timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def _get_private_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0)
            s.connect(('192.168.0.1', 1))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return None

# Usage
# print(f"Internet startig")
# network_info = NetworkInfo()
# # Wait for the thread to complete (for demonstration purposes)
# # threading.Event().wait(1)
# network_info.check_network_info()
# print(f"Internet Status: {network_info.internet_status}")
# print(f"Private IP: {network_info.private_ip}")