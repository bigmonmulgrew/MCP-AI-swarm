from typing import List, Dict, Any, Callable

# Type alias for a row: dict with field names like {"timestamp": ..., "cam1": ..., "cam2": ...}
Row = Dict[str, Any]


def apply_plan(rows: List[Row], plan: Dict[str, Any]) -> List[Row]:
    """
    Execute a declarative filter plan against a list of data rows.
    
    Args:
        rows: List of dictionaries representing data records
        plan: Dictionary describing filters to apply, e.g.:
            {
                "rule": "red",
                "description": "...",
                "filters": [
                    {"type": "all", "conditions": [...]},
                    {"type": "exclude_window", "field": "timestamp", "start": ..., "end": ...}
                ]
            }
    
    Returns:
        Filtered list of rows matching the plan criteria
    """
    # Define comparison operators
    def op_eq(val, target): 
        return val == target
    
    def op_ne(val, target): 
        return val != target
    
    def op_gt(val, target): 
        return val > target
    
    def op_gte(val, target): 
        return val >= target
    
    def op_lt(val, target): 
        return val < target
    
    def op_lte(val, target): 
        return val <= target

    # Map operator names to functions
    op_map: Dict[str, Callable[[Any, Any], bool]] = {
        "eq": op_eq, 
        "ne": op_ne, 
        "gt": op_gt, 
        "gte": op_gte, 
        "lt": op_lt, 
        "lte": op_lte
    }

    def match_all(row: Row, conditions: List[Dict[str, Any]]) -> bool:
        """Check if a row matches all conditions."""
        return all(
            op_map[c["op"]](row.get(c["field"]), c["value"]) 
            for c in conditions
        )

    # Start with all rows
    filtered = rows
    
    # Apply each filter in sequence
    for f in plan.get("filters", []):
        ftype = f.get("type")
        
        if ftype == "exclude_window":
            # Exclude rows whose field value falls within [start, end]
            start = f["start"]
            end = f["end"]
            field = f["field"]
            filtered = [
                r for r in filtered 
                if not (start <= r.get(field, 0) <= end)
            ]
        
        elif ftype == "all":
            # Keep only rows where all conditions are true
            conditions = f.get("conditions", [])
            filtered = [
                r for r in filtered 
                if match_all(r, conditions)
            ]
        
        elif ftype == "any":
            # Keep rows where at least one condition is true
            conditions = f.get("conditions", [])
            filtered = [
                r for r in filtered 
                if any(match_all(r, [c]) for c in conditions)
            ]
        
        else:
            raise ValueError(f"Unknown filter type: {ftype}")
    
    return filtered
