from drone import VisualiserDrone

drone = VisualiserDrone(
    name="MCP visualisation server",
    category="Visualisation",
    env_host_key="MCP_VISUALISER_HOST",
    env_port_key="MCP_VISUALISER_PORT_E",
)

app = drone.app