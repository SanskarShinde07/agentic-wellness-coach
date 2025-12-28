"""
FeedbackAgent: Observes user behavior and collects feedback for the agent loop.
"""
from datetime import datetime
from typing import Dict, Any, List


class FeedbackAgent:
    def __init__(self):
        self.observation_log = []

    def observe_task_completion(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        print("\n[FeedbackAgent] Reasoning: Observing task completion (domain-agnostic)...")
        plan = user_data.get("current_plan", {}).get("weekly_schedule", [])
        completed = [w for w in plan if w.get("status") == "completed"]
        skipped = [w for w in plan if w.get("status") == "skipped"]
        pending = [w for w in plan if w.get("status") == "pending"]

        total_expected = len(plan)
        total_completed = len(completed)
        consistency_rate = (total_completed / total_expected) if total_expected else 0

        observation = {
            "completed_workouts": total_completed,  # keep key name for compatibility
            "skipped_workouts": len(skipped),
            "pending_workouts": len(pending),
            "consistency_rate": consistency_rate,
            "current_streak": self._calculate_streak(user_data.get("workouts", [])),
            "total_workouts": total_expected,
            "observation_timestamp": datetime.now().isoformat(),
            "domain": user_data.get("profile", {}).get("domain", "fitness"),
        }

        reasoning = f"Observed {total_completed} completed, {len(skipped)} skipped, {len(pending)} pending"
        self.observation_log.append(
            {
                "step": "task_observation",
                "observation": observation,
                "reasoning": reasoning,
                "timestamp": datetime.now().isoformat(),
            }
        )
        print(f"[FeedbackAgent] Observation: {reasoning}")
        print(f"[FeedbackAgent] Observation: Consistency rate = {consistency_rate:.2%}")
        return observation

    def collect_difficulty_feedback(self, user_data: Dict[str, Any]) -> str:
        print("\n[FeedbackAgent] Reasoning: Collecting difficulty feedback (simulated)...")
        # Simulation based on completion; in real app, collect user input
        workouts = user_data.get("workouts", [])
        recent = workouts[-5:] if len(workouts) >= 5 else workouts
        if not recent:
            difficulty = "moderate"
            reasoning = "No recent tasks - default moderate"
        else:
            completed_recent = [w for w in recent if w.get("status") == "completed"]
            rate = len(completed_recent) / len(recent) if recent else 0
            if rate < 0.4:
                difficulty = "hard"
                reasoning = "Low completion suggests tasks too hard"
            elif rate > 0.8:
                difficulty = "easy"
                reasoning = "High completion suggests tasks easy"
            else:
                difficulty = "moderate"
                reasoning = "Completion suggests appropriate difficulty"

        self.observation_log.append(
            {
                "step": "difficulty_feedback",
                "difficulty": difficulty,
                "reasoning": reasoning,
                "timestamp": datetime.now().isoformat(),
            }
        )
        print(f"[FeedbackAgent] Observation: Difficulty level = {difficulty}")
        print(f"[FeedbackAgent] Reasoning: {reasoning}")
        return difficulty

    def aggregate_feedback(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        print("\n[FeedbackAgent] Reasoning: Aggregating all feedback data...")
        observation = self.observe_task_completion(user_data)
        difficulty = self.collect_difficulty_feedback(user_data)
        feedback = {
            **observation,
            "difficulty": difficulty,
            "aggregated_at": datetime.now().isoformat(),
        }
        reasoning = f"Aggregated feedback: {observation['completed_workouts']} completed, difficulty={difficulty}"
        self.observation_log.append(
            {
                "step": "feedback_aggregation",
                "feedback": feedback,
                "reasoning": reasoning,
                "timestamp": datetime.now().isoformat(),
            }
        )
        print("[FeedbackAgent] Observation: Feedback aggregated")
        print(f"[FeedbackAgent] Reasoning: {reasoning}")
        return feedback

    def _calculate_streak(self, workouts: List[Dict[str, Any]]) -> int:
        if not workouts:
            return 0
        completed = sorted(
            [w for w in workouts if w.get("status") == "completed"],
            key=lambda x: x.get("date", ""),
            reverse=True,
        )
        if not completed:
            return 0
        streak = 0
        today = datetime.now().date()
        for w in completed:
            date_str = w.get("date", "")
            try:
                d = datetime.fromisoformat(date_str).date()
            except Exception:
                continue
            diff = (today - d).days
            if diff == streak:
                streak += 1
            elif diff > streak:
                break
        return streak

    def get_observation_log(self) -> List[Dict[str, Any]]:
        return self.observation_log