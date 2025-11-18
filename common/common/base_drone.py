from abc import ABC, abstractmethod
from fastapi import FastAPI
from time import time, sleep
import threading
import requests
import os
from common import DroneOnlineObject

class BaseDroneServer(ABC):
    def __init__(self, name, category, env_host_key, env_port_key):
        self.name = name
        self.category = category
        self.env_host_key = env_host_key
        self.env_port_key = env_port_key
        self.start_time = time()
        self.app = FastAPI(title=f"{self.name} API")
        
        # Register required endpoints
        self._register_status_endpoint()

        # Force subclass to register its /query endpoint
        self._register_subclass_endpoints()

        # Start MCPS registration thread
        self._register_startup_event()

    def _register_status_endpoint(self):
        @self.app.get("/status")
        async def status():
            return {"status": "ok", "uptime_seconds": time() - self.start_time}

    def _register_startup_event(self):
        @self.app.on_event("startup")
        def startup_event():
            print(f"[MCO] Starting {self.name}...")
            threading.Thread(target=self._announce_to_mcps, daemon=True).start()

    def _announce_to_mcps(self):
        sleep(10)
        MCPS_HOST = os.getenv("MCPS_HOST", "localhost")
        MCPS_PORT = os.getenv("MCPS_PORT_I", 8080)
        MCPS_ONLINE_URL = f"http://{MCPS_HOST}:{MCPS_PORT}/online"

        drone_info = DroneOnlineObject(
            ToolServerName=self.name,
            ToolServerAddress=os.getenv(self.env_host_key, "localhost"),
            ToolServerPort=os.getenv(self.env_port_key, "8000"),
            ToolServerCategory=self.category,
            Timeout=300,
        )

        print(f"[MCO] Registering {self.name} with MCPS at {MCPS_ONLINE_URL}...")
        try:
            res = requests.post(MCPS_ONLINE_URL, json=drone_info.model_dump(mode = "json"))
            res.raise_for_status()
            print(f"[MCO] {self.name} registered successfully: {res.json()}")
        except requests.exceptions.RequestException as e:
            print(f"[MCO] {self.name} failed to register: {e}")
    
    @abstractmethod
    def _register_subclass_endpoints(self):
        """Subclasses must define their own /query endpoint."""
        pass