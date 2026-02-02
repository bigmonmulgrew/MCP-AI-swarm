from drone import DomainDrone

drone = DomainDrone(
    name="MCP Domain XL server",
    category="Unstructured",
    env_host_key="MCP_DOMAIN_XL_HOST",
    env_port_key="MCP_DOMAIN_XL_PORT_E",
)

app = drone.app
