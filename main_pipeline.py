from static_kg import CurriculumKnowledgeGraph
from dynamic_kg import LearnerStateGraph
from mastery_engine import MasteryEngine
from reasoner import PrerequisiteReasoner
from planner import LearningPlanner
from questionnaire import ask_questions


def compare_roadmaps(old, new):
    added = [x for x in new if x not in old]
    removed = [x for x in old if x not in new]
    return added, removed


# 1. Initialize KG
kg = CurriculumKnowledgeGraph()

# 2. Create learner state
lsg = LearnerStateGraph("student_1", kg.get_all_concepts())

# 3. Initialize components
engine = MasteryEngine()
reasoner = PrerequisiteReasoner(kg, lsg)
planner = LearningPlanner(kg, lsg, reasoner)

previous_roadmap = []

while True:
    print("\n==============================")
    print("📌 CURRENT ROADMAP")
    print("==============================")

    # 🔥 FIX: unpack roadmap and reasons
    roadmap, reasons = planner.generate_next_steps()

    # 🔹 Print roadmap
    for i, step in enumerate(roadmap):
        print(f"{i+1}. {step}")

    # 🔹 Print reasons
    print("\n🧠 Why this roadmap?")
    for r in reasons:
        print("-", r)

    # 🔹 Show changes
    if previous_roadmap:
        added, removed = compare_roadmaps(previous_roadmap, roadmap)

        print("\n🔄 Changes:")
        print("Added:", added)
        print("Removed:", removed)

    # 🔹 Save current roadmap
    previous_roadmap = roadmap.copy()

    # 🔹 Input
    concept = input("\nEnter concept to evaluate (or q): ").lower()

    if concept == 'q':
        print("Exiting...")
        break

    # 🔥 Use questionnaire instead of manual score
    score = ask_questions(concept)

    # 🔹 Update mastery
    old_score = lsg.get_mastery(concept)["score"]
    updated_score = engine.update(old_score, score)
    level = engine.score_to_level(updated_score)

    lsg.update_mastery(concept, updated_score, level)

    print(f"\nUpdated {concept}: {level} ({updated_score:.2f})")