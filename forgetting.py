class ForgettingDetector:
    def __init__(self, learner_graph, static_kg):
        self.lsg = learner_graph
        self.kg = static_kg

    def detect_decay(self, concept_id):
        """
        If prerequisite was strong but dependent concept fails,
        assume forgetting
        """
        weak_state = self.lsg.get_mastery(concept_id)

        if weak_state["level"] != "Weak":
            return []

        prereqs = self.kg.get_prerequisites(concept_id)

        decayed = []

        for p in prereqs:
            state = self.lsg.get_mastery(p)

            if state["level"] == "Strong":
                decayed.append(p)

        return decayed