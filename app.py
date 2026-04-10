import streamlit as st
from graphviz import Digraph

from static_kg import CurriculumKnowledgeGraph
from dynamic_kg import LearnerStateGraph
from mastery_engine import MasteryEngine
from reasoner import PrerequisiteReasoner
from planner import LearningPlanner
from questionnaire import evaluate_answer


# 🔹 INIT SESSION
if "initialized" not in st.session_state:
    st.session_state.kg = CurriculumKnowledgeGraph()
    st.session_state.lsg = LearnerStateGraph(
        "student_1",
        st.session_state.kg.get_all_concepts()
    )
    st.session_state.engine = MasteryEngine()
    st.session_state.reasoner = PrerequisiteReasoner(
        st.session_state.kg,
        st.session_state.lsg
    )
    st.session_state.planner = LearningPlanner(
        st.session_state.kg,
        st.session_state.lsg,
        st.session_state.reasoner
    )
    st.session_state.show_results = False
    st.session_state.last_result = None
    st.session_state.initialized = True


kg = st.session_state.kg
lsg = st.session_state.lsg
engine = st.session_state.engine
planner = st.session_state.planner


# 🎯 HEADER
st.title("🎯 Your Personalized Learning Plan")
st.markdown("Improve step-by-step based on your current knowledge.")


# 🧭 STATIC GUIDE
st.subheader("🧭 How Your Learning Plan Works")

st.markdown("""
1. 📌 Select a topic you want to improve  
2. ✍️ Answer a few conceptual questions  
3. 📊 Get evaluated based on your understanding  
4. 🚀 Receive a personalized learning plan  
""")


# 🔹 SELECT CONCEPT
st.markdown("👉 Select a topic to begin:")

concept = st.selectbox(
    "📌 Select Topic to Improve",
    ["-- Select a concept --"] + kg.get_all_concepts()
)


answers = []

# 🔥 QUESTIONS (STABLE INPUT — NO AUTOFILL ISSUE)
if concept != "-- Select a concept --":

    st.subheader("✍️ Answer Questions")

    questions_map = {
        "arrays": [
            "What is an array?",
            "How are elements accessed in an array?"
        ],
        "sorting": [
            "What is sorting?",
            "Name any sorting algorithms",
            "Why do we use sorting?"
        ],
        "binary_search": [
            "What is binary search?",
            "When can binary search be applied?",
            "How does binary search work?"
        ],
        "recursion": [
            "What is recursion?",
            "What is a base case?",
            "Why is base case important?"
        ],
        "backtracking": [
            "What is backtracking?",
            "How does backtracking work?",
            "Give an example"
        ]
    }

    keywords_map = {
        "arrays": {
            "collection": 0.3,
            "elements": 0.4,
            "index": 0.3,
            "position": 0.3
        },
        "sorting": {
            "arrange": 0.4,
            "order": 0.4,
            "organize": 0.4
        },
        "binary_search": {
            "sorted": 0.3,
            "divide": 0.3,
            "half": 0.4
        },
        "recursion": {
            "function": 0.3,
            "itself": 0.4,
            "call": 0.3
        },
        "backtracking": {
            "recursion": 0.3,
            "undo": 0.4,
            "choice": 0.3
        }
    }

    for i, q in enumerate(questions_map.get(concept, [])):
        ans = st.text_area(
            f"Q{i+1}. {q}",
            key=f"{concept}_{i}",
            placeholder="Type your answer...",
            height=80
        )
        answers.append(ans)

    if st.button("✅ Submit Answer"):

        keywords = keywords_map.get(concept, {})

        total_score = 0
        individual_scores = []

        for ans in answers:
            score = evaluate_answer(ans, keywords)
            individual_scores.append(score)
            total_score += score

        final_score = total_score / len(answers) if answers else 0

        old_score = lsg.get_mastery(concept)["score"]
        updated_score = engine.update(old_score, final_score)
        level = engine.score_to_level(updated_score)

        lsg.update_mastery(concept, updated_score, level)

        st.session_state.last_result = {
            "concept": concept,
            "individual_scores": individual_scores,
            "final_score": final_score,
            "level": level,
            "updated_score": updated_score
        }

        st.session_state.show_results = True


# 🔥 RESULTS + FLOWCHART
if st.session_state.show_results and st.session_state.last_result:

    result = st.session_state.last_result

    st.subheader("📊 Evaluation Result")

    for i, s in enumerate(result["individual_scores"]):
        st.write(f"Q{i+1} Score: {s:.2f}")

    st.write(f"**Final Score: {result['final_score']:.2f}**")

    st.success(
        f"{result['concept']} → {result['level']} ({result['updated_score']:.2f})"
    )

    roadmap, reasons = planner.generate_next_steps()

    # 🔥 FLOWCHART UI
    st.subheader("📌 Your Learning Path")

    dot = Digraph()

    for i, step in enumerate(roadmap):

        if "Revise" in step:
            color = "lightcoral"
        elif "Practice" in step:
            color = "khaki"
        else:
            color = "lightgreen"

        dot.node(str(i), step, style="filled", fillcolor=color)

    for i in range(len(roadmap) - 1):
        dot.edge(str(i), str(i + 1))

    st.graphviz_chart(dot)

    # 🔹 WHY SECTION
    st.subheader("🧠 Why this plan?")

    for r in reasons:
        st.write("•", r)