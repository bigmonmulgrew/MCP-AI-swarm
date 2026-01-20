from typing import List, Dict, Any
import json

def analyse_camera_data(camera_data: List[List[int]]) -> str:
    if not camera_data:
        return {
            "start_time": None,
            "end_time": None,
            "total_count": 0,
            "all_on_count": 0,
            "one_off_count": 0,
            "two_off_count": 0,
            "summary": []
        }

    timestamps = [row[0] for row in camera_data]

    all_on_count = 0
    one_off_count = 0
    two_off_count = 0
    summary = []

    for ts, cam1, cam2 in camera_data:
        if cam1 == 1 and cam2 == 1:
            all_on_count += 1
        else:
            summary.append([ts, cam1, cam2])
            if cam1 == 0 and cam2 == 0:
                two_off_count += 1
            else:
                one_off_count += 1

    return_dict = {
        "start_time": min(timestamps),
        "end_time": max(timestamps),
        "total_count": len(camera_data),
        "all_on_count": all_on_count,
        "one_off_count": one_off_count,
        "two_off_count": two_off_count,
        "summary": summary
    }

    return json.dumps(return_dict, indent=2)