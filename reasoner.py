class PrerequisiteReasoner:
    def __init__(self, static_kg, learner_graph):
        self.kg = static_kg
        self.lsg = learner_graph

    def check_prerequisites(self, concept_id):
        prerequisites = self.kg.get_prerequisites(concept_id)

        missing = []

        for p in prerequisites:
            state = self.lsg.get_mastery(p)
            if state["level"] != "Strong":
                missing.append(p)

        return missing

    def detect_root_cause(self, concept_id):
        """
        If concept is weak, check if prerequisites are weak
        """
        state = self.lsg.get_mastery(concept_id)

        if state["level"] != "Weak":
            return None

        prereqs = self.kg.get_prerequisites(concept_id)

        weak_prereqs = [
            p for p in prereqs
            if self.lsg.get_mastery(p)["level"] != "Strong"
        ]

        return weak_prereqs