from drone import DataDrone

drone = DataDrone(
    name="MCP Data server",
    category="Unstructured",
    env_host_key="MCP_DATA_HOST",
    env_port_key="MCP_DATA_PORT_E",
)

app = drone.app