import os
import json
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMEvaluator:
    """Evaluates student answers using Google's Gemini models."""
    
    def __init__(self, use_mock=False):
        """
        Initialize the LLM evaluator.
        
        Args:
            use_mock: If True, use mock evaluator instead of real API calls
        """
        self.use_mock = use_mock
        
        if not use_mock:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            
            # Configure Gemini
            genai.configure(api_key=api_key)
            self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
            self.temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
            
            # Initialize the model
            generation_config = {
                "temperature": self.temperature,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 200,
            }
            
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=generation_config
            )
    
    def evaluate_answer(self, question: Dict[str, Any], student_answer: str) -> Dict[str, float]:
        """
        Evaluate a student's answer using LLM.
        
        Args:
            question: Question dictionary from question bank
            student_answer: Student's answer text
            
        Returns:
            Dictionary with scores for each rubric dimension (0-1)
        """
        if self.use_mock:
            return self._mock_evaluate(question, student_answer)
        
        return self._real_evaluate(question, student_answer)
    
    def _real_evaluate(self, question: Dict[str, Any], student_answer: str) -> Dict[str, float]:
        """Evaluate using Gemini API."""
        rubric = question.get("rubric", {})
        question_text = question.get("text") or question.get("question", "")
        expected_answer = question.get("expected_answer", "N/A")
        
        prompt = f"""
        You are an expert computer science educator evaluating a student's answer to a Data Structures and Algorithms question.
        
        QUESTION: {question_text}
        
        EXPECTED ANSWER KEY POINTS: {expected_answer}
        
        RUBRIC DIMENSIONS:
        1. Definition (0-1): {rubric.get('definition', 'N/A')}
        2. Reasoning (0-1): {rubric.get('reasoning', 'N/A')}
        3. Application (0-1): {rubric.get('application', 'N/A')}
        
        STUDENT'S ANSWER: {student_answer}
        
        Please evaluate the student's answer and provide scores for each rubric dimension.
        Return ONLY a JSON object with exactly this structure:
        {{
            "definition": <score between 0 and 1>,
            "reasoning": <score between 0 and 1>,
            "application": <score between 0 and 1>
        }}
        
        Be fair and consistent in your evaluation. Consider partial credit where appropriate.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from response
            try:
                # Try to parse the entire response as JSON
                scores = json.loads(result_text)
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from the text
                import re
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    scores = json.loads(json_match.group())
                else:
                    # Fallback to mock evaluation
                    print(f"Warning: Could not parse Gemini response as JSON. Using mock evaluation.\nResponse: {result_text}")
                    return self._mock_evaluate(question, student_answer)
            
            # Validate scores
            for dimension in ["definition", "reasoning", "application"]:
                if dimension not in scores:
                    scores[dimension] = 0.5
                else:
                    scores[dimension] = max(0, min(1, float(scores[dimension])))
            
            return scores
            
        except Exception as e:
            print(f"Error in Gemini evaluation: {e}")
            # Fallback to mock evaluation
            return self._mock_evaluate(question, student_answer)
    
    def _mock_evaluate(self, question: Dict[str, Any], student_answer: str) -> Dict[str, float]:
        """
        Mock evaluator for testing without API calls.
        Simulates evaluation based on answer length and content.
        """
        # Simple mock evaluation logic
        answer_length = len(student_answer)
        
        # Base scores
        definition_score = min(1.0, answer_length / 100) * 0.8
        reasoning_score = min(1.0, answer_length / 150) * 0.7
        application_score = min(1.0, answer_length / 200) * 0.6
        
        # Add some randomness
        import random
        definition_score += random.uniform(-0.1, 0.2)
        reasoning_score += random.uniform(-0.1, 0.2)
        application_score += random.uniform(-0.1, 0.2)
        
        # Clamp to 0-1 range
        definition_score = max(0, min(1, definition_score))
        reasoning_score = max(0, min(1, reasoning_score))
        application_score = max(0, min(1, application_score))
        
        return {
            "definition": round(definition_score, 2),
            "reasoning": round(reasoning_score, 2),
            "application": round(application_score, 2)
        }