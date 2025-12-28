"""
DataManager: Handles user data persistence.
"""
import json
from pathlib import Path
from typing import Dict, Any


class DataManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.data_file = self.data_dir / "user_data.json"

    def load_user_data(self, user_id: str = "default") -> Dict[str, Any]:
        if not self.data_file.exists():
            return self._create_default_user(user_id)
        try:
            with open(self.data_file, "r") as f:
                all_data = json.load(f)
                return all_data.get(user_id, self._create_default_user(user_id))
        except Exception:
            return self._create_default_user(user_id)

    def save_user_data(self, user_data: Dict[str, Any], user_id: str = "default") -> bool:
        try:
            all_data = {}
            if self.data_file.exists():
                with open(self.data_file, "r") as f:
                    all_data = json.load(f)
            all_data[user_id] = user_data
            with open(self.data_file, "w") as f:
                json.dump(all_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def _create_default_user(self, user_id: str) -> Dict[str, Any]:
        return {
            "user_id": user_id,
            "profile": {
                "domain": "fitness",
                "fitness_level": "beginner",
                "time_per_week": 3,
                "preferences": ["general_fitness"],
                "nutrition_goal": "balanced",
                "mental_focus": "stress_management",
                "preventive_focus": "activity",
            },
            "current_plan": None,
            "workouts": [],
            "goal_history": [],
            "created_at": None,
        }

    def add_workout(self, user_data: Dict[str, Any], workout: Dict[str, Any]) -> Dict[str, Any]:
        user_data.setdefault("workouts", [])
        user_data["workouts"].append(workout)
        return user_data

    def update_plan(self, user_data: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
        user_data["current_plan"] = plan
        return user_data