"""
DecisionAgent: Makes autonomous decisions about plan execution and interventions.
"""
from datetime import datetime
from typing import Dict, Any, List


class DecisionAgent:
    def __init__(self):
        self.decision_log = []

    def should_adapt_plan(self, feedback: Dict[str, Any], plan: Dict[str, Any]) -> bool:
        print("\n[DecisionAgent] Reasoning: Evaluating if plan adaptation is needed...")
        consistency_rate = feedback.get("consistency_rate", 0)
        difficulty = feedback.get("difficulty", "moderate")
        total = feedback.get("total_workouts", 0)
        adaptation_count = plan.get("adaptation_count", 0)

        if total == 0:
            print("[DecisionAgent] Decision: No data yet - continue with current plan")
            return False

        if adaptation_count >= 5:
            reasoning = "Maximum adaptations reached - maintain"
            decision = False
        elif consistency_rate < 0.5 and total >= 3:
            reasoning = "Low consistency below 50%"
            decision = True
        elif consistency_rate > 0.8 and difficulty == "easy" and total >= 5:
            reasoning = "High consistency + easy difficulty"
            decision = True
        elif difficulty == "hard" and total >= 3:
            reasoning = "User reports difficulty hard"
            decision = True
        else:
            reasoning = "Plan appropriate - maintain"
            decision = False

        self.decision_log.append(
            {
                "step": "adaptation_decision",
                "decision": decision,
                "reasoning": reasoning,
                "feedback": feedback,
                "timestamp": datetime.now().isoformat(),
            }
        )
        print(f"[DecisionAgent] Decision: {'ADAPT PLAN' if decision else 'MAINTAIN PLAN'}")
        print(f"[DecisionAgent] Reasoning: {reasoning}")
        return decision

    def decide_intervention(self, feedback: Dict[str, Any]) -> Dict[str, Any]:
        print("\n[DecisionAgent] Reasoning: Deciding on user intervention...")
        skipped = feedback.get("skipped_workouts", 0)
        completed = feedback.get("completed_workouts", 0)
        streak = feedback.get("current_streak", 0)

        intervention = {
            "type": "encouragement",
            "message": "Keep up the great work!",
            "action": None,
        }

        if skipped > completed:
            intervention = {
                "type": "motivation",
                "message": "Consistency matters. Try a smaller task today.",
                "action": "reduce_intensity",
            }
            reasoning = "Struggling with consistency"
        elif streak >= 7:
            intervention = {
                "type": "celebration",
                "message": f"Amazing streak of {streak} days! You're building strong habits!",
                "action": "maintain",
            }
            reasoning = "Celebrate streak"
        elif completed > 0:
            intervention = {
                "type": "positive_reinforcement",
                "message": f"Great job completing {completed} task(s)!",
                "action": "maintain",
            }
            reasoning = "Reinforce success"
        else:
            reasoning = "Standard encouragement"

        self.decision_log.append(
            {
                "step": "intervention_decision",
                "intervention": intervention,
                "reasoning": reasoning,
                "timestamp": datetime.now().isoformat(),
            }
        )
        print(f"[DecisionAgent] Decision: {intervention['type'].upper()} intervention")
        print(f"[DecisionAgent] Reasoning: {reasoning}")
        print(f"[DecisionAgent] Message: {intervention['message']}")
        return intervention

    def should_escalate_goal(self, plan: Dict[str, Any], feedback: Dict[str, Any]) -> bool:
        print("\n[DecisionAgent] Reasoning: Evaluating goal escalation...")
        week_number = plan.get("week_number", 1)
        consistency_rate = feedback.get("consistency_rate", 0)
        goal_weeks = plan.get("goal", {}).get("target_weeks", 8)

        if week_number >= goal_weeks and consistency_rate > 0.75:
            reasoning = f"Goal period complete with high consistency ({consistency_rate:.2%})"
            print("[DecisionAgent] Decision: Goal achieved - ready for new goal")
            print(f"[DecisionAgent] Reasoning: {reasoning}")
            return True

        reasoning = f"Goal in progress ({week_number}/{goal_weeks}) - continue"
        print("[DecisionAgent] Decision: Continue current goal")
        print(f"[DecisionAgent] Reasoning: {reasoning}")
        return False

    def get_decision_log(self) -> List[Dict[str, Any]]:
        return self.decision_log