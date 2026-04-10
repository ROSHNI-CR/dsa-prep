class LearningPlanner:
    def __init__(self, kg, lsg, reasoner):
        self.kg = kg
        self.lsg = lsg
        self.reasoner = reasoner

    def generate_next_steps(self):
        roadmap = []
        reasons = []
        visited = set()

        # 🔹 Get concepts (NO change to KG)
        concepts = self.kg.get_all_concepts()

        # 🔥 PRIORITY: Weak → Partial → Strong
        def priority(concept):
            level = self.lsg.get_mastery(concept)["level"]

            if level == "Weak":
                return 0
            elif level == "Partial":
                return 1
            else:
                return 2

        # sort concepts based on priority
        concepts = sorted(concepts, key=priority)

        # 🔹 Build roadmap
        for concept in concepts:
            state = self.lsg.get_mastery(concept)
            level = state["level"]

            # 🔹 Check prerequisites (existing logic)
            missing = self.reasoner.check_prerequisites(concept)

            if missing:
                for m in missing:
                    if m not in visited:
                        roadmap.append(f"{m} (Revise)")
                        reasons.append(f"{m} is prerequisite for {concept}")
                        visited.add(m)
                continue

            # 🔹 Weak → Revise + Practice
            if level == "Weak":
                if concept not in visited:
                    roadmap.append(f"{concept} (Revise)")
                    roadmap.append(f"{concept} (Practice)")
                    reasons.append(f"{concept} is Weak → added revision")
                    visited.add(concept)

            # 🔹 Partial → Practice
            elif level == "Partial":
                if concept not in visited:
                    roadmap.append(f"{concept} (Practice)")
                    reasons.append(f"{concept} is Partial → needs practice")
                    visited.add(concept)

            # 🔹 Strong → Skip
            elif level == "Strong":
                continue

        return roadmap, reasons