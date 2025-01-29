import requests
from typing import Dict, Any

def get_operator(operator_name: str) -> Dict[str, Any]:
    url = f"https://api.rhodesapi.com/api/operator/{operator_name}" 
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        op = response.json()

        lore = op.get("lore", {})
        base = op.get("base", [])
        module = op.get("module", [])
        voicelines = op.get("voicelines", {})

        talks = [
            talk if (talk := voicelines.get(f"talk_{i}")) and operator_name not in talk else "Operator name in talk or no quote"
            for i in range(1, 4)
        ]

        return {
            "rarity": op.get("rarity", "Unknown"),
            "alter": op.get("alter", "Unknown"),
            "availability": op.get("availability", "Unknown"),
            "gender": lore.get("gender", "Unknown"),
            "race": lore.get("race", "Unknown"),
            "recruitable": op.get("recruitable", "Unknown"),
            "headhunting": op.get("headhunting", "Unknown"),
            "infection_status": lore.get("infection_status", "Unknown"),
            "tags": op.get("tags", ["No tags"]),
            "module_availability": module[1].get("availability", "No module") if len(module) > 1 else "No module",
            "base": base[-1].get("effects", "No base effects") if base else "No base effects",
            "talks": talks
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching operator data: {e}")
        return {"error": "Failed to fetch operator data"}

