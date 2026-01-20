from drone import DomainDrone

drone = DomainDrone(
    name="MCP Domain server",
    category="Unstructured",
    env_host_key="MCP_DOMAIN_HOST",
    env_port_key="MCP_DOMAIN_PORT_E",
)

app = drone.app
