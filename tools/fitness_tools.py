"""
FitnessTools: Utility functions for fitness calculations and formatting.
"""
"""
FitnessTools: Utility functions for formatting and progress.
"""
from typing import Dict, Any, List


class FitnessTools:
    @staticmethod
    def format_plan_display(plan: Dict[str, Any]) -> str:
        if not plan:
            return "No plan available"

        goal = plan.get("goal", {})
        schedule = plan.get("weekly_schedule", [])
        output = "\n=== PLAN ===\n"
        output += f"Goal: {goal.get('description', 'N/A')}\n"
        output += f"Week: {plan.get('week_number', 1)}\n\nSchedule:\n"

        for task in schedule:
            status_icon = "✓" if task.get("status") == "completed" else "○" if task.get("status") == "skipped" else "□"
            label = task.get("type", "task")
            detail = task.get("practice") or task.get("task") or ", ".join(task.get("items", [])) or ""
            duration = ""
            if "duration_minutes" in task:
                duration = f" ({task.get('duration_minutes', 0)} min, {task.get('intensity', 'N/A')})"
            output += f"  {status_icon} {task.get('day', 'N/A')}: {label} {detail}{duration}\n"
        return output

    @staticmethod
    def calculate_progress(user_data: Dict[str, Any]) -> Dict[str, Any]:
        plan = user_data.get("current_plan")
        if not plan:
            return {"progress_percent": 0, "completed": 0, "total": 0, "message": "No active plan"}

        schedule = plan.get("weekly_schedule", [])
        total_expected = len(schedule)
        completed = len([w for w in schedule if w.get("status") == "completed"])
        progress = (completed / total_expected * 100) if total_expected else 0

        return {
            "progress_percent": progress,
            "completed": completed,
            "total": total_expected,
            "message": f"{completed}/{total_expected} tasks completed",
        }

    @staticmethod
    def create_workout_entry(day: str, workout_type: str, status: str = "completed") -> Dict[str, Any]:
        from datetime import datetime

        return {"day": day, "type": workout_type, "status": status, "date": datetime.now().isoformat()}