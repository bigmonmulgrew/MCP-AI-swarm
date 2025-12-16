# Filter plans for traffic light rules
# These plans are applied to camera data to determine system status

# Red rule: "At any time, both cameras are off."
# This checks if both cam1 and cam2 equal 0
red_plan = {
    "rule": "red",
    "description": "At any time, both cameras are off.",
    "filters": [
        {
            "type": "all",
            "conditions": [
                {"field": "cam1", "op": "eq", "value": 0},
                {"field": "cam2", "op": "eq", "value": 0}
            ]
        }
    ]
}

# Amber rule: "Cameras are not in the maintenance period."
# This excludes rows where timestamp falls within a maintenance window
# For demo purposes, using a sample maintenance window
amber_plan = {
    "rule": "amber",
    "description": "Cameras are not in the maintenance period.",
    "filters": [
        {
            "type": "exclude_window",
            "field": "timestamp",
            "start": 1760650220000,
            "end": 1760650240000
        }
    ]
}
