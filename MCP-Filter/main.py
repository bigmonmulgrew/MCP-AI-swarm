from drone import FilterDrone

drone = FilterDrone(
    name="MCP Filter server",
    category="Unstructured",
    env_host_key="MCP_FILTER_HOST",
    env_port_key="MCP_FILTER_PORT_E",
)

app = drone.app
