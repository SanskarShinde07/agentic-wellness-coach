"""
Agentic Wellness System - Streamlit Interface
Domains: fitness, nutrition, mental_health, preventive
"""
import streamlit as st
from agents import PlannerAgent, DecisionAgent, FeedbackAgent
from tools import DataManager, FitnessTools

st.set_page_config(page_title="Agentic Wellness Coach", page_icon="🤖", layout="wide")

# Initialize session state
if "planner" not in st.session_state:
    st.session_state.planner = PlannerAgent()
    st.session_state.decision_agent = DecisionAgent()
    st.session_state.feedback_agent = FeedbackAgent()
    st.session_state.data_manager = DataManager()
    st.session_state.fitness_tools = FitnessTools()
    st.session_state.user_data = st.session_state.data_manager.load_user_data("default")
    st.session_state.iteration_count = 0

st.title("🤖 Agentic Wellness Coaching System")
st.markdown("---")
st.warning("⚠️ Wellness guidance only. No medical diagnosis or treatment. Consult professionals for medical concerns.")

# Sidebar: profile
with st.sidebar:
    st.header("User Profile")
    domain = st.selectbox("Domain", ["fitness", "nutrition", "mental_health", "preventive"])
    fitness_level = st.selectbox("Fitness Level", ["beginner", "intermediate", "advanced"])
    time_per_week = st.slider("Days per Week (fitness)", 2, 7, 3)
    preferences = st.multiselect(
        "Fitness Goals", ["weight_loss", "muscle_gain", "endurance", "general_fitness"], default=["general_fitness"]
    )
    nutrition_goal = st.selectbox("Nutrition goal", ["balanced", "high_protein", "calorie_deficit"])
    mental_focus = st.selectbox("Mental focus", ["stress_management", "mindfulness", "sleep_support"])
    preventive_focus = st.selectbox("Preventive focus", ["activity", "posture", "breaks"])

    if st.button("Initialize Profile"):
        st.session_state.user_data = st.session_state.data_manager.load_user_data("default")
        st.session_state.user_data["profile"] = {
            "domain": domain,
            "fitness_level": fitness_level,
            "time_per_week": time_per_week,
            "preferences": preferences,
            "nutrition_goal": nutrition_goal,
            "mental_focus": mental_focus,
            "preventive_focus": preventive_focus,
        }
        st.session_state.data_manager.save_user_data(st.session_state.user_data, "default")
        st.success("Profile initialized!")

# Ensure user_data loaded
if st.session_state.user_data is None:
    st.session_state.user_data = st.session_state.data_manager.load_user_data("default")

st.header("🤖 Agent Loop Execution")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Run Agent Loop Iteration"):
        st.session_state.iteration_count += 1

        # PLAN
        with st.expander("📋 PHASE 1: PLAN", expanded=True):
            current_plan = st.session_state.user_data.get("current_plan")
            if not current_plan:
                st.write("**Agent reasoning: Identifying user goal...**")
                goal = st.session_state.planner.identify_goal(st.session_state.user_data.get("profile", {}))
                st.write("**Agent planning: Creating plan...**")
                current_plan = st.session_state.planner.create_plan(goal, st.session_state.user_data.get("profile", {}))
                st.session_state.user_data = st.session_state.data_manager.update_plan(
                    st.session_state.user_data, current_plan
                )
            st.code(st.session_state.fitness_tools.format_plan_display(current_plan))

        # ACT
        with st.expander("⚡ PHASE 2: ACT"):
            st.write("**Simulate user action...**")
            schedule = current_plan.get("weekly_schedule", [])
            pending = [w for w in schedule if w.get("status") == "pending"]
            if pending:
                task = pending[0]
                action = st.radio(
                    f"Action for {task.get('day')} - {task.get('type')}",
                    ["Completed", "Skipped"],
                    key=f"action_{st.session_state.iteration_count}",
                )
                if st.button("Record Action"):
                    status = "completed" if action == "Completed" else "skipped"
                    entry = st.session_state.fitness_tools.create_workout_entry(task.get("day"), task.get("type"), status)
                    st.session_state.user_data = st.session_state.data_manager.add_workout(
                        st.session_state.user_data, entry
                    )
                    for w in schedule:
                        if w.get("day") == task.get("day"):
                            w["status"] = status
                    st.session_state.user_data = st.session_state.data_manager.update_plan(
                        st.session_state.user_data, current_plan
                    )
                    st.success("Action recorded!")

        # OBSERVE
        with st.expander("👁️ PHASE 3: OBSERVE"):
            st.write("**Agent observation: Analyzing feedback...**")
            feedback = st.session_state.feedback_agent.aggregate_feedback(st.session_state.user_data)
            st.json(feedback)

        # ADAPT
        with st.expander("🔄 PHASE 4: ADAPT"):
            st.write("**Agent decision: Evaluating plan adaptation...**")
            should_adapt = st.session_state.decision_agent.should_adapt_plan(feedback, current_plan)
            if should_adapt:
                st.write("**Agent adaptation: Modifying plan...**")
                adapted_plan = st.session_state.planner.adapt_plan(current_plan, feedback)
                st.session_state.user_data = st.session_state.data_manager.update_plan(
                    st.session_state.user_data, adapted_plan
                )
                st.code(st.session_state.fitness_tools.format_plan_display(adapted_plan))
                st.success("Plan adapted!")
            else:
                st.info("Plan maintained - no adaptation needed")

            intervention = st.session_state.decision_agent.decide_intervention(feedback)
            st.info(f"💬 {intervention['message']}")

        st.session_state.data_manager.save_user_data(st.session_state.user_data, "default")
        st.rerun()

with col2:
    st.subheader("📊 Current Status")
    if st.session_state.user_data.get("current_plan"):
        progress = st.session_state.fitness_tools.calculate_progress(st.session_state.user_data)
        st.metric("Progress", f"{progress['progress_percent']:.1f}%")
        st.metric("Completed", f"{progress['completed']}/{progress['total']}")
        st.subheader("Current Plan")
        st.code(st.session_state.fitness_tools.format_plan_display(st.session_state.user_data.get("current_plan")))
    else:
        st.info("No active plan. Initialize profile and run agent loop.")

# Reasoning logs
st.markdown("---")
st.header("🧠 Agent Reasoning Logs")
tab1, tab2, tab3 = st.tabs(["Planner", "Decision", "Feedback"])

with tab1:
    st.subheader("PlannerAgent Reasoning (last 5)")
    for log in st.session_state.planner.get_reasoning_log()[-5:]:
        st.json(log)

with tab2:
    st.subheader("DecisionAgent Reasoning (last 5)")
    for log in st.session_state.decision_agent.get_decision_log()[-5:]:
        st.json(log)

with tab3:
    st.subheader("FeedbackAgent Reasoning (last 5)")
    for log in st.session_state.feedback_agent.get_observation_log()[-5:]:
        st.json(log)