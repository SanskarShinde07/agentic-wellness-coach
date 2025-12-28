"""
Agentic Wellness System - Main Application (CLI)
Domains: fitness, nutrition, mental_health, preventive
Agent Loop: Plan -> Act -> Observe -> Adapt
"""
from datetime import datetime
import random
from agents import PlannerAgent, DecisionAgent, FeedbackAgent
from tools import DataManager, FitnessTools


class AgenticWellnessCoach:
    def __init__(self):
        self.planner = PlannerAgent()
        self.decision_agent = DecisionAgent()
        self.feedback_agent = FeedbackAgent()
        self.data_manager = DataManager()
        self.fitness_tools = FitnessTools()

        print("=" * 60)
        print("AGENTIC WELLNESS COACHING SYSTEM")
        print("=" * 60)
        print("\n⚠️  DISCLAIMER: Wellness guidance only. No medical diagnosis or treatment.")
        print("   Consult healthcare professionals for medical concerns.\n")
        print("=" * 60)

    def run_agent_loop(self, user_id: str = "default", max_iterations: int = 5):
        print("\n" + "=" * 60)
        print("STARTING AGENT LOOP")
        print("=" * 60)

        user_data = self.data_manager.load_user_data(user_id)

        if not user_data.get("current_plan"):
            print("\n[SYSTEM] Initializing new user profile...")
            user_data = self._initialize_user(user_data)

        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            print(f"\n{'=' * 60}")
            print(f"AGENT LOOP ITERATION {iteration}")
            print(f"{'=' * 60}")

            # PLAN
            print("\n>>> PHASE 1: PLAN <<<")
            current_plan = user_data.get("current_plan")
            if not current_plan:
                goal = self.planner.identify_goal(user_data.get("profile", {}))
                current_plan = self.planner.create_plan(goal, user_data.get("profile", {}))
                user_data = self.data_manager.update_plan(user_data, current_plan)
            print(self.fitness_tools.format_plan_display(current_plan))

            # ACT (simulate)
            print("\n>>> PHASE 2: ACT <<<")
            print("[SYSTEM] Simulating user interaction...")
            user_action = self._simulate_user_action(user_data)
            if user_action:
                workout_entry = self.fitness_tools.create_workout_entry(
                    user_action["day"], user_action["type"], user_action["status"]
                )
                user_data = self.data_manager.add_workout(user_data, workout_entry)
                print(f"[SYSTEM] User action recorded: {user_action['status']} - {user_action['type']}")

            # OBSERVE
            print("\n>>> PHASE 3: OBSERVE <<<")
            feedback = self.feedback_agent.aggregate_feedback(user_data)

            # ADAPT
            print("\n>>> PHASE 4: ADAPT <<<")
            should_adapt = self.decision_agent.should_adapt_plan(feedback, current_plan)
            if should_adapt:
                print("\n[SYSTEM] Adapting plan based on feedback...")
                adapted_plan = self.planner.adapt_plan(current_plan, feedback)
                user_data = self.data_manager.update_plan(user_data, adapted_plan)
                current_plan = adapted_plan
            else:
                print("\n[SYSTEM] Maintaining current plan - no adaptation needed")

            intervention = self.decision_agent.decide_intervention(feedback)
            print(f"\n[SYSTEM] Intervention: {intervention['message']}")

            if self.decision_agent.should_escalate_goal(current_plan, feedback):
                print("\n[SYSTEM] Long-term goal achieved! Ready for new goal.")
                user_data["current_plan"] = None
                user_data["goal_history"].append(current_plan)

            self.data_manager.save_user_data(user_data, user_id)

            progress = self.fitness_tools.calculate_progress(user_data)
            print(f"\n[PROGRESS] {progress['message']} ({progress['progress_percent']:.1f}%)")

            if iteration < max_iterations:
                print("\n[SYSTEM] Press Enter to continue (or 'q' to quit)...")
                user_input = input().strip().lower()
                if user_input == "q":
                    break

        print("\n" + "=" * 60)
        print("AGENT LOOP COMPLETE")
        print("=" * 60)
        self._print_reasoning_summary()

    def _initialize_user(self, user_data: dict) -> dict:
        if not user_data.get("profile"):
            domain_input = input("Choose domain (fitness/nutrition/mental_health/preventive) [fitness]: ").strip().lower()
            domain = domain_input if domain_input in ["fitness", "nutrition", "mental_health", "preventive"] else "fitness"
            user_data["profile"] = {
                "domain": domain,
                "fitness_level": "beginner",
                "time_per_week": 3,
                "preferences": ["general_fitness"],
                "nutrition_goal": "balanced",
                "mental_focus": "stress_management",
                "preventive_focus": "activity",
            }

        goal = self.planner.identify_goal(user_data["profile"])
        plan = self.planner.create_plan(goal, user_data["profile"])
        user_data = self.data_manager.update_plan(user_data, plan)
        user_data["created_at"] = datetime.now().isoformat()
        return user_data

    def _simulate_user_action(self, user_data: dict) -> dict:
        plan = user_data.get("current_plan")
        if not plan:
            return None
        schedule = plan.get("weekly_schedule", [])
        pending = [w for w in schedule if w.get("status") == "pending"]
        if not pending:
            return None
        workout = pending[0]
        status = "completed" if random.random() < 0.7 else "skipped"
        for w in schedule:
            if w.get("day") == workout.get("day"):
                w["status"] = status
        return {"day": workout.get("day"), "type": workout.get("type"), "status": status}

    def _print_reasoning_summary(self):
        print("\n=== AGENT REASONING SUMMARY ===")
        print(f"\nPlannerAgent reasoning steps: {len(self.planner.get_reasoning_log())}")
        print(f"DecisionAgent decision steps: {len(self.decision_agent.get_decision_log())}")
        print(f"FeedbackAgent observation steps: {len(self.feedback_agent.get_observation_log())}")
        print("\nAll reasoning logs are printed above during execution.")


if __name__ == "__main__":
    coach = AgenticWellnessCoach()
    try:
        coach.run_agent_loop(user_id="default", max_iterations=5)
    except KeyboardInterrupt:
        print("\n\nSystem interrupted by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback

        traceback.print_exc()