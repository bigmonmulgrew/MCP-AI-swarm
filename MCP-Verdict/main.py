from drone import DataDrone

drone = DataDrone(
    name="MCP Verdict server",
    category="Unstructured",
    env_host_key="MCP_VERDICT_HOST",
    env_port_key="MCP_VERDICT_PORT_E",
)

app = drone.app