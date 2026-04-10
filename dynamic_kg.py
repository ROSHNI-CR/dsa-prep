from datetime import datetime

class LearnerStateGraph:
    def __init__(self, student_id, concepts):
        self.student_id = student_id

        # concept_id → mastery state
        self.mastery = {
            concept: {
                "score": 0.0,
                "level": "Unknown",
                "confidence": 0.0,
                "attempts": 0,
                "last_updated": None
            }
            for concept in concepts
        }

    def update_mastery(self, concept_id, score, level):
        node = self.mastery[concept_id]

        node["score"] = score
        node["level"] = level
        node["attempts"] += 1
        node["last_updated"] = datetime.now().isoformat()

    def get_mastery(self, concept_id):
        return self.mastery[concept_id]

    def get_all_states(self):
        return self.mastery