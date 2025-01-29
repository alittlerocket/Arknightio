import requests
from typing import Dict, Any
from fastapi import APIRouter

router = APIRouter()

@router.get("/operator/{name}", tags=["operator"])
def get_clues(name: str) -> Dict[str, Any]:
    url = f"https://api.rhodesapi.com/api/operator/{name}" 
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        op = response.json()

        lore = op.get("lore", {})
        base = op.get("base", [])
        module = op.get("module", [])
        voicelines = op.get("voicelines", {})

        # Clues from the top level of the JSON
        clues = {key : op[key] for key in op.keys() & {"rarity", "availability", "recruitable", "headhunting", "tags", "class"}}
        
        # Information from the lore section
        lore_clues = {key : lore[key] for key in lore.keys() & {"gender", "race", "infection_status"}}

        # Highest level base effect
        base_clues = { "highest base effect" : base[-1].get("effects") if base else "No base effects" }

        # Module available?
        module_clues = { "module_availability" : module[0].get("availability", "No Module") }

        # Voiceline quotes
        voicelines_clues = { 
            key : (voicelines[key] if not name in voicelines[key] else "Operator Name in Quote")
            for key in voicelines.keys() & {"talk_1", "talk_2", "talk_3"}
        }

        return {**clues, **lore_clues, **base_clues, **module_clues, **voicelines_clues}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching operator data: {e}")
        return {"error": "Failed to fetch operator data"}
