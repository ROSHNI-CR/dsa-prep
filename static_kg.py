class CurriculumKnowledgeGraph:
    def __init__(self):
        # concept_id → metadata
        self.concepts = {
            "arrays": {
                "name": "Arrays",
                "difficulty": "easy",
                "prerequisites": []
            },
            "sorting": {
                "name": "Sorting",
                "difficulty": "easy",
                "prerequisites": ["arrays"]
            },
            "binary_search": {
                "name": "Binary Search",
                "difficulty": "medium",
                "prerequisites": ["arrays", "sorting"]
            },
            "recursion": {
                "name": "Recursion",
                "difficulty": "medium",
                "prerequisites": []
            },
            "backtracking": {
                "name": "Backtracking",
                "difficulty": "hard",
                "prerequisites": ["recursion"]
            }
        }

    def get_prerequisites(self, concept_id):
        return self.concepts[concept_id]["prerequisites"]

    def get_all_concepts(self):
        return list(self.concepts.keys())