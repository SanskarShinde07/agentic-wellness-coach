"""
PlannerAgent: Creates and adapts plans based on goals and feedback.
Domains: fitness, nutrition, mental_health, preventive
"""
from datetime import datetime
from typing import Dict, List, Any


class PlannerAgent:
    def __init__(self):
        self.reasoning_log = []

    def identify_goal(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        print("\n[PlannerAgent] Reasoning: Identifying user's long-term goal by domain...")
        domain = user_profile.get("domain", "fitness")

        if domain == "nutrition":
            goal = {
                "type": "nutrition_balance",
                "description": "Build consistent healthy eating habits and meal balance",
                "target_weeks": 8,
                "metrics": ["meals_logged", "adherence_rate", "hydration"],
            }
        elif domain == "mental_health":
            goal = {
                "type": "stress_management",
                "description": "Reduce stress via daily micro-practices and reflection",
                "target_weeks": 6,
                "metrics": ["practices_completed", "streak", "self_reported_stress"],
            }
        elif domain == "preventive":
            goal = {
                "type": "preventive_activity",
                "description": "Maintain daily movement and recovery-focused habits",
                "target_weeks": 8,
                "metrics": ["movement_breaks", "steps_proxy", "sleep_hygiene_checks"],
            }
        else:  # fitness default
            goal = {
                "type": "general_fitness",
                "description": "Build consistent exercise habits and improve overall fitness",
                "target_weeks": 8,
                "metrics": ["workouts_completed", "consistency_rate"],
            }

        reasoning = f"Identified goal '{goal['type']}' for domain={domain}"
        self.reasoning_log.append(
            {
                "step": "goal_identification",
                "reasoning": reasoning,
                "goal": goal,
                "timestamp": datetime.now().isoformat(),
            }
        )
        print(f"[PlannerAgent] Decision: Long-term goal set - {goal['description']}")
        print(f"[PlannerAgent] Reasoning: {reasoning}")
        return goal

    def create_plan(self, goal: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        print("\n[PlannerAgent] Reasoning: Creating multi-step plan by domain...")
        domain = user_profile.get("domain", "fitness")

        if domain == "nutrition":
            plan = self._create_nutrition_plan(goal, user_profile)
        elif domain == "mental_health":
            plan = self._create_mental_health_plan(goal, user_profile)
        elif domain == "preventive":
            plan = self._create_preventive_plan(goal, user_profile)
        else:
            plan = self._create_fitness_plan(goal, user_profile)

        reasoning = f"Plan created for domain={domain} with {len(plan.get('weekly_schedule', []))} tasks"
        self.reasoning_log.append(
            {
                "step": "plan_creation",
                "reasoning": reasoning,
                "plan": plan,
                "timestamp": datetime.now().isoformat(),
            }
        )
        print(f"[PlannerAgent] Decision: {reasoning}")
        return plan

    def adapt_plan(self, current_plan: Dict[str, Any], feedback: Dict[str, Any]) -> Dict[str, Any]:
        print("\n[PlannerAgent] Reasoning: Analyzing feedback to adapt plan...")
        skipped = feedback.get("skipped_workouts", 0)
        completed = feedback.get("completed_workouts", 0)
        difficulty = feedback.get("difficulty", "moderate")
        total = completed + skipped
        consistency_rate = completed / total if total else 0

        print(f"[PlannerAgent] Observation: {skipped} skipped, {completed} completed")
        print(f"[PlannerAgent] Observation: Consistency rate = {consistency_rate:.2%}")

        adapted_plan = current_plan.copy()
        adapted_plan["adaptation_count"] = adapted_plan.get("adaptation_count", 0) + 1

        if consistency_rate < 0.5:
            print("[PlannerAgent] Decision: Consistency low - reducing frequency/intensity")
            adapted_plan["weekly_schedule"] = self._reduce_frequency(adapted_plan["weekly_schedule"])
            reasoning = "Reduced frequency due to low consistency"
        elif consistency_rate > 0.8 and difficulty == "easy":
            print("[PlannerAgent] Decision: High consistency + easy - increasing challenge")
            adapted_plan["weekly_schedule"] = self._increase_intensity(adapted_plan["weekly_schedule"])
            reasoning = "Increased intensity due to high consistency and easy feedback"
        elif difficulty == "hard":
            print("[PlannerAgent] Decision: Difficulty high - easing tasks")
            adapted_plan["weekly_schedule"] = self._reduce_intensity(adapted_plan["weekly_schedule"])
            reasoning = "Reduced intensity due to difficulty feedback"
        else:
            print("[PlannerAgent] Decision: Plan appropriate - minor/no adjustments")
            reasoning = "Maintained plan with minor/no adjustments"

        adapted_plan["last_adapted"] = datetime.now().isoformat()
        self.reasoning_log.append(
            {
                "step": "plan_adaptation",
                "reasoning": reasoning,
                "feedback": feedback,
                "adaptation": adapted_plan,
                "timestamp": datetime.now().isoformat(),
            }
        )
        print(f"[PlannerAgent] Reasoning: {reasoning}")
        return adapted_plan

    # Domain-specific plan builders
    def _create_fitness_plan(self, goal, user_profile):
        fitness_level = user_profile.get("fitness_level", "beginner")
        time_per_week = user_profile.get("time_per_week", 3)
        goal_type = goal.get("type", "general_fitness")
        templates = {
            "weight_loss": ["Cardio", "HIIT", "Strength", "Cardio", "Active Recovery"],
            "muscle_gain": ["Strength", "Strength", "Hypertrophy", "Strength", "Active Recovery"],
            "endurance": ["Cardio", "Long Run", "Interval", "Cardio", "Recovery"],
            "general_fitness": ["Full Body", "Cardio", "Strength", "Flexibility", "Active Recovery"],
        }
        workouts = templates.get(goal_type, templates["general_fitness"])[:time_per_week]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        schedule = []
        for i, w in enumerate(workouts):
            schedule.append(
                {
                    "day": days[i],
                    "type": w,
                    "duration_minutes": 30 if fitness_level == "beginner" else 45,
                    "intensity": "moderate" if fitness_level == "beginner" else "high",
                    "status": "pending",
                }
            )
        return {
            "goal": goal,
            "weekly_schedule": schedule,
            "created_at": datetime.now().isoformat(),
            "week_number": 1,
            "adaptation_count": 0,
        }

    def _create_nutrition_plan(self, goal, user_profile):
        prefs = user_profile.get("nutrition_goal", "balanced")
        schedule = []
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        for d in days:
            schedule.append(
                {
                    "day": d,
                    "type": f"{prefs}_meal_plan",
                    "items": ["3 meals", "2L water"],
                    "status": "pending",
                }
            )
        return {
            "goal": goal,
            "weekly_schedule": schedule,
            "created_at": datetime.now().isoformat(),
            "week_number": 1,
            "adaptation_count": 0,
        }

    def _create_mental_health_plan(self, goal, user_profile):
        focus = user_profile.get("mental_focus", "stress_management")
        practices = ["breathing (5 min)", "gratitude (3 items)", "walk (10 min)", "mindfulness (5 min)"]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        schedule = []
        for i, d in enumerate(days):
            practice = practices[i % len(practices)]
            schedule.append({"day": d, "type": focus, "practice": practice, "status": "pending"})
        return {
            "goal": goal,
            "weekly_schedule": schedule,
            "created_at": datetime.now().isoformat(),
            "week_number": 1,
            "adaptation_count": 0,
        }

    def _create_preventive_plan(self, goal, user_profile):
        focus = user_profile.get("preventive_focus", "activity")
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        tasks = [
            "5 movement breaks",
            "posture check x3",
            "5 movement breaks",
            "hydration focus 2L",
            "sleep hygiene: wind-down 30m",
        ]
        schedule = []
        for d, task in zip(days, tasks):
            schedule.append({"day": d, "type": focus, "task": task, "status": "pending"})
        return {
            "goal": goal,
            "weekly_schedule": schedule,
            "created_at": datetime.now().isoformat(),
            "week_number": 1,
            "adaptation_count": 0,
        }

    # Adaptation helpers (generic)
    def _reduce_frequency(self, schedule: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return schedule[:-1] if len(schedule) > 2 else schedule

    def _increase_intensity(self, schedule: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for task in schedule:
            if "duration_minutes" in task:
                task["duration_minutes"] += 5
            if task.get("intensity") == "moderate":
                task["intensity"] = "high"
        return schedule

    def _reduce_intensity(self, schedule: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for task in schedule:
            if "duration_minutes" in task:
                task["duration_minutes"] = max(20, task["duration_minutes"] - 5)
            if task.get("intensity") == "high":
                task["intensity"] = "moderate"
        return schedule

    def get_reasoning_log(self):
        return self.reasoning_log