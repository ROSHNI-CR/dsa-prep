import json

class PrerequisiteChecker:
    def __init__(self, knowledge_graph_path="knowledge_graph.json"):
        """
        Initialize the prerequisite checker with knowledge graph.
        
        Args:
            knowledge_graph_path (str): Path to knowledge graph JSON file
        """
        with open(knowledge_graph_path, 'r') as f:
            self.knowledge_graph = json.load(f)
        
        # Build concept lookup and prerequisite maps
        self.concepts = self.knowledge_graph["concepts"]
        self.prerequisite_map = self._build_prerequisite_map()
    
    def _build_prerequisite_map(self):
        """Build a map of concept -> list of prerequisite concept IDs."""
        prerequisite_map = {}
        
        for concept_id, concept_data in self.concepts.items():
            prerequisite_map[concept_id] = concept_data.get("prerequisites", [])
        
        return prerequisite_map
    
    def check_prerequisites(self, target_concept_id, mastery_states):
        """
        Check if student has sufficient mastery of prerequisites for a concept.
        
        Args:
            target_concept_id (str): ID of the concept to check prerequisites for
            mastery_states (dict): Dictionary mapping concept IDs to mastery levels
            
        Returns:
            dict: Result with missing prerequisites and recommendations
        """
        if target_concept_id not in self.prerequisite_map:
            return {
                "target_concept": target_concept_id,
                "prerequisites_met": True,
                "missing_prerequisites": [],
                "recommendation": "Proceed with learning"
            }
        
        prerequisites = self.prerequisite_map[target_concept_id]
        missing_prerequisites = []
        
        for prereq_id in prerequisites:
            # Check if prerequisite is in mastery states
            if prereq_id not in mastery_states:
                missing_prerequisites.append({
                    "concept_id": prereq_id,
                    "concept_name": self.concepts.get(prereq_id, {}).get("name", prereq_id),
                    "reason": "Not evaluated yet",
                    "mastery": "Unknown"
                })
            else:
                prereq_mastery = mastery_states[prereq_id]
                # Consider "Weak" mastery as insufficient
                if prereq_mastery.get("mastery") == "Weak":
                    missing_prerequisites.append({
                        "concept_id": prereq_id,
                        "concept_name": self.concepts.get(prereq_id, {}).get("name", prereq_id),
                        "reason": "Insufficient mastery",
                        "mastery": prereq_mastery.get("mastery"),
                        "score": prereq_mastery.get("average_score")
                    })
        
        if missing_prerequisites:
            # Generate learning path recommendation
            recommendation = f"Review {len(missing_prerequisites)} prerequisite concept(s): "
            recommendation += ", ".join([p["concept_name"] for p in missing_prerequisites])
            
            return {
                "target_concept": target_concept_id,
                "concept_name": self.concepts.get(target_concept_id, {}).get("name", target_concept_id),
                "prerequisites_met": False,
                "missing_prerequisites": missing_prerequisites,
                "recommendation": recommendation
            }
        else:
            return {
                "target_concept": target_concept_id,
                "concept_name": self.concepts.get(target_concept_id, {}).get("name", target_concept_id),
                "prerequisites_met": True,
                "missing_prerequisites": [],
                "recommendation": "Ready to learn this concept"
            }
    
    def get_learning_path(self, current_mastery_states, target_concept_id):
        """
        Generate a learning path to reach target concept.
        
        Args:
            current_mastery_states (dict): Current mastery states
            target_concept_id (str): Target concept to learn
            
        Returns:
            dict: Learning path with steps and prerequisites
        """
        if target_concept_id not in self.concepts:
            return {"error": f"Concept '{target_concept_id}' not found"}
        
        # Perform BFS to find all prerequisites
        visited = set()
        queue = [target_concept_id]
        prerequisite_tree = {}
        
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            
            visited.add(current)
            prerequisites = self.prerequisite_map.get(current, [])
            prerequisite_tree[current] = prerequisites
            
            for prereq in prerequisites:
                if prereq not in visited:
                    queue.append(prereq)
        
        # Build learning path in topological order (prerequisites first)
        learning_path = []
        concepts_to_learn = list(visited)
        
        # Sort by difficulty and prerequisites
        def get_concept_depth(concept_id):
            depth = 0
            current = concept_id
            while self.prerequisite_map.get(current):
                if self.prerequisite_map[current]:
                    depth += 1
                    current = self.prerequisite_map[current][0]  # Follow first prerequisite
                else:
                    break
            return depth
        
        concepts_to_learn.sort(key=lambda x: (get_concept_depth(x), x))
        
        # Create path steps
        for concept_id in concepts_to_learn:
            concept_data = self.concepts.get(concept_id, {})
            current_mastery = current_mastery_states.get(concept_id, {})
            
            step = {
                "concept_id": concept_id,
                "concept_name": concept_data.get("name", concept_id),
                "description": concept_data.get("description", ""),
                "difficulty": concept_data.get("difficulty", "unknown"),
                "current_mastery": current_mastery.get("mastery", "Unknown"),
                "prerequisites": self.prerequisite_map.get(concept_id, []),
                "status": "completed" if current_mastery.get("mastery") in ["Strong", "Partial"] else "pending"
            }
            
            learning_path.append(step)
        
        return {
            "target_concept": target_concept_id,
            "target_concept_name": self.concepts.get(target_concept_id, {}).get("name", target_concept_id),
            "total_steps": len(learning_path),
            "completed_steps": sum(1 for step in learning_path if step["status"] == "completed"),
            "learning_path": learning_path
        }