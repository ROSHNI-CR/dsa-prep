import json

class MasteryEvaluator:
    def __init__(self, thresholds=None):
        """
        Initialize the mastery evaluator with scoring thresholds.
        
        Args:
            thresholds (dict): Custom thresholds for mastery levels
        """
        self.thresholds = thresholds or {
            "strong": 0.8,
            "partial": 0.5,
            "weak": 0.0
        }
    
    def evaluate_mastery(self, rubric_scores):
        """
        Convert rubric scores into mastery levels.
        
        Args:
            rubric_scores (dict): Scores for definition, reasoning, application
            
        Returns:
            dict: Mastery level for each dimension and overall
        """
        mastery_levels = {}
        
        for dimension, score in rubric_scores.items():
            if score >= self.thresholds["strong"]:
                mastery_levels[dimension] = "Strong"
            elif score >= self.thresholds["partial"]:
                mastery_levels[dimension] = "Partial"
            else:
                mastery_levels[dimension] = "Weak"
        
        # Calculate overall mastery (average of all dimensions)
        avg_score = sum(rubric_scores.values()) / len(rubric_scores)
        
        if avg_score >= self.thresholds["strong"]:
            mastery_levels["overall"] = "Strong"
        elif avg_score >= self.thresholds["partial"]:
            mastery_levels["overall"] = "Partial"
        else:
            mastery_levels["overall"] = "Weak"
        
        mastery_levels["average_score"] = round(avg_score, 2)
        
        return mastery_levels
    
    def get_concept_mastery_state(self, concept_id, evaluation_history):
        """
        Determine mastery state for a concept based on evaluation history.
        
        Args:
            concept_id (str): ID of the concept
            evaluation_history (list): List of evaluation results for this concept
            
        Returns:
            dict: Mastery state including level and confidence
        """
        if not evaluation_history:
            return {
                "concept": concept_id,
                "mastery": "Unknown",
                "confidence": 0.0,
                "last_evaluated": None
            }
        
        # Calculate average scores across all evaluations
        total_scores = {"definition": 0, "reasoning": 0, "application": 0}
        count = 0
        
        for eval_result in evaluation_history:
            if "rubric_scores" in eval_result:
                for dimension, score in eval_result["rubric_scores"].items():
                    total_scores[dimension] += score
                count += 1
        
        if count == 0:
            return {
                "concept": concept_id,
                "mastery": "Unknown",
                "confidence": 0.0,
                "last_evaluated": None
            }
        
        # Calculate averages
        avg_scores = {
            dimension: total_scores[dimension] / count
            for dimension in total_scores
        }
        
        # Determine mastery level
        mastery_result = self.evaluate_mastery(avg_scores)
        
        # Calculate confidence based on number of evaluations
        confidence = min(1.0, count / 3.0)  # Max confidence after 3 evaluations
        
        return {
            "concept": concept_id,
            "mastery": mastery_result["overall"],
            "average_score": mastery_result["average_score"],
            "dimension_scores": avg_scores,
            "confidence": round(confidence, 2),
            "evaluation_count": count,
            "last_evaluated": evaluation_history[-1].get("timestamp") if evaluation_history else None
        }