camera_data = [
        [1764547200, 1, 1],
        [1774547200, 1, 1],
        [1784547200, 1, 1],
        [1794547200, 1, 1],
        [1804547200, 1, 1],
        [1814547200, 0, 0],
        [1824547200, 1, 1]
]

# "start": 1764547200,
# "end": 1795996800

# Normalized version: each row as a dict with field names
normalized_camera_data = [
    {"timestamp": ts, "cam1": c1, "cam2": c2}
    for ts, c1, c2 in camera_data
]