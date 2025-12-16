camera_data = [
        [1760650094000, 1, 1],
        [1760650214000, 1, 1],
        [1760650223000, 1, 1],
        [1760650236000, 1, 1],
        [1760650248000, 1, 1],
        [1760650259000, 0, 0],
        [1760650268000, 1, 1]
]

#"start": 1760650220000, "end": 1760650240000

# Normalized version: each row as a dict with field names
normalized_camera_data = [
    {"timestamp": ts, "cam1": c1, "cam2": c2}
    for ts, c1, c2 in camera_data
]