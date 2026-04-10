#!/usr/bin/env python3
"""
Test script for the adaptive learning system pipeline.
Demonstrates: Question → Student Answer → LLM Evaluation → Mastery State → Prerequisite Check
"""

import json
import random
from datetime import datetime
from llm_evaluator import LLMEvaluator
from mastery_evaluator import MasteryEvaluator
from prerequisite_checker import PrerequisiteChecker

def load_question_bank():
    """Load questions from the question bank."""
    with open("question_bank.json", "r") as f:
        return json.load(f)

def simulate_student_answer(question_text, concept):
    """
    Simulate a student answer based on the question and concept.
    In a real system, this would come from actual student input.
    """
    # Simple simulation: generate answers of varying quality
    answer_templates = {
        "arrays": [
            "An array is a data structure that stores elements in contiguous memory locations. It allows O(1) access but O(n) insertion/deletion in the middle.",
            "Arrays are collections of items. You can access them with indexes.",
            "I'm not sure about arrays. They seem like lists?"
        ],
        "sorting": [
            "Bubble sort repeatedly compares adjacent elements and swaps them if they're in the wrong order. It has O(n²) time complexity.",
            "Sorting arranges data. Bubble sort is slow.",
            "What's sorting?"
        ],
        "binary_search": [
            "Binary search requires a sorted array. It works by repeatedly dividing the search interval in half. Time complexity is O(log n).",
            "You search in half of the array each time. Needs sorted data.",
            "Binary what?"
        ],
        "recursion": [
            "Recursion is when a function calls itself. It needs a base case to stop. Examples include factorial and Fibonacci.",
            "Functions calling themselves. Can cause stack overflow.",
            "Recursion is confusing."
        ],
        "backtracking": [
            "Backtracking builds solutions incrementally and abandons partial solutions that can't be completed. Used in N-Queens and Sudoku.",
            "It's like trying different paths and going back if they don't work.",
            "Backtracking sounds complicated."
        ]
    }
    
    # Return a random answer for the concept
    templates = answer_templates.get(concept, ["I don't know the answer."])
    return random.choice(templates)

def run_pipeline_demo():
    """Run the complete pipeline demonstration."""
    print("=" * 60)
    print("ADAPTIVE LEARNING SYSTEM MVP - PIPELINE DEMONSTRATION")
    print("=" * 60)
    
    # Initialize components
    print("\n1. Initializing components...")
    
    # Check if we have Gemini API key
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key and gemini_api_key != "your_gemini_api_key_here":
        print("   Using Gemini API for evaluation...")
        llm_evaluator = LLMEvaluator(use_mock=False)
    else:
        print("   Using mock evaluator (no API key found)...")
        llm_evaluator = LLMEvaluator(use_mock=True)
    
    mastery_evaluator = MasteryEvaluator()
    prerequisite_checker = PrerequisiteChecker()
    
    # Load questions
    question_bank = load_question_bank()
    questions = question_bank["questions"]
    
    # Track mastery states across concepts
    mastery_states = {}
    evaluation_history = {}
    
    print(f"Loaded {len(questions)} questions across 5 concepts")
    
    # Test with a few sample questions
    test_concepts = ["arrays", "sorting", "binary_search", "recursion", "backtracking"]
    
    for concept_id in test_concepts:
        print(f"\n{'='*60}")
        print(f"TESTING CONCEPT: {concept_id.upper()}")
        print(f"{'='*60}")
        
        # Get questions for this concept
        concept_questions = [q for q in questions if q["concept"] == concept_id]
        
        if not concept_questions:
            print(f"No questions found for concept: {concept_id}")
            continue
        
        # Test with first question for this concept
        question = concept_questions[0]
        
        print(f"\n2. Question: {question['text']}")
        print(f"   Concept: {question['concept']}")
        
        # Simulate student answer
        student_answer = simulate_student_answer(question["text"], question["concept"])
        print(f"\n3. Simulated Student Answer:\n   {student_answer}")
        
        # LLM Evaluation
        print(f"\n4. LLM Evaluation (using rubric):")

        # Use evaluate_answer (mock or real depending on configuration)
        rubric_scores = llm_evaluator.evaluate_answer(question, student_answer)

        print(f"   Rubric Scores: {json.dumps(rubric_scores, indent=6)}")
        
        # Mastery Evaluation
        print(f"\n5. Mastery Evaluation:")
        mastery_result = mastery_evaluator.evaluate_mastery(rubric_scores)
        print(f"   Mastery Levels: {json.dumps(mastery_result, indent=6)}")
        
        # Store evaluation in history
        eval_record = {
            "question_id": question["id"],
            "question_text": question["text"],
            "student_answer": student_answer,
            "rubric_scores": rubric_scores,
            "mastery_levels": mastery_result,
            "timestamp": datetime.now().isoformat()
        }
        
        if concept_id not in evaluation_history:
            evaluation_history[concept_id] = []
        evaluation_history[concept_id].append(eval_record)
        
        # Update mastery state for this concept
        mastery_states[concept_id] = mastery_evaluator.get_concept_mastery_state(
            concept_id, 
            evaluation_history[concept_id]
        )
        
        print(f"\n6. Current Mastery State for '{concept_id}':")
        print(f"   {json.dumps(mastery_states[concept_id], indent=6)}")
        
        # Prerequisite Check
        print(f"\n7. Prerequisite Check for '{concept_id}':")
        prereq_check = prerequisite_checker.check_prerequisites(concept_id, mastery_states)
        print(f"   Prerequisites Met: {prereq_check['prerequisites_met']}")
        
        if not prereq_check["prerequisites_met"]:
            print(f"   Missing Prerequisites: {len(prereq_check['missing_prerequisites'])}")
            for missing in prereq_check["missing_prerequisites"]:
                print(f"     - {missing['concept_name']}: {missing['reason']}")
        
        print(f"   Recommendation: {prereq_check['recommendation']}")
    
    # Demonstrate learning path generation
    print(f"\n{'='*60}")
    print("LEARNING PATH DEMONSTRATION")
    print(f"{'='*60}")
    
    # Show learning path for backtracking (most complex concept)
    target_concept = "backtracking"
    print(f"\nGenerating learning path for: {target_concept}")
    
    learning_path = prerequisite_checker.get_learning_path(mastery_states, target_concept)
    
    if "error" not in learning_path:
        print(f"\nLearning Path to master '{learning_path['target_concept_name']}':")
        print(f"Total steps: {learning_path['total_steps']}")
        print(f"Completed: {learning_path['completed_steps']}")
        
        print("\nStep-by-step path:")
        for i, step in enumerate(learning_path["learning_path"], 1):
            status_icon = "✓" if step["status"] == "completed" else "○"
            print(f"{i:2d}. {status_icon} {step['concept_name']} "
                  f"({step['difficulty']}) - Current: {step['current_mastery']}")
            if step["prerequisites"]:
                prereq_names = [prerequisite_checker.concepts.get(p, {}).get("name", p) 
                              for p in step["prerequisites"]]
                print(f"    Requires: {', '.join(prereq_names)}")
    
    # Summary
    print(f"\n{'='*60}")
    print("SYSTEM SUMMARY")
    print(f"{'='*60}")
    
    print("\nMastery States Across All Concepts:")
    for concept_id, state in mastery_states.items():
        concept_name = prerequisite_checker.concepts.get(concept_id, {}).get("name", concept_id)
        print(f"  {concept_name:15} : {state['mastery']:8} "
              f"(Score: {state.get('average_score', 0):.2f}, "
              f"Confidence: {state.get('confidence', 0):.2f})")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)

def run_single_question_test():
    """Run a single question through the complete pipeline."""
    print("\n" + "=" * 60)
    print("SINGLE QUESTION PIPELINE TEST")
    print("=" * 60)
    
    # Initialize components
    # Check if we have Gemini API key
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key and gemini_api_key != "your_gemini_api_key_here":
        print("Using Gemini API for evaluation...")
        llm_evaluator = LLMEvaluator(use_mock=False)
    else:
        print("Using mock evaluator (no API key found)...")
        llm_evaluator = LLMEvaluator(use_mock=True)
    
    mastery_evaluator = MasteryEvaluator()
    prerequisite_checker = PrerequisiteChecker()
    
    # Load questions
    question_bank = load_question_bank()
    
    # Pick a specific question (binary search)
    question = next(q for q in question_bank["questions"] if q["id"] == "q5")
    
    print(f"\n1. Question: {question['text']}")
    print(f"   Concept: {question['concept']}")
    
    # Simulate a detailed student answer
    student_answer = """
    Binary search is an efficient algorithm for finding an item in a sorted array. 
    It works by repeatedly dividing the search interval in half. 
    
    Prerequisites:
    1. The array must be sorted
    2. Random access to elements (like arrays provide)
    
    Algorithm:
    1. Set left = 0, right = n-1
    2. While left <= right:
        a. mid = (left + right) // 2
        b. If array[mid] == target, return mid
        c. If array[mid] < target, left = mid + 1
        d. If array[mid] > target, right = mid - 1
    3. Return -1 (not found)
    
    Time complexity: O(log n) because we halve the search space each iteration.
    Space complexity: O(1) for iterative version.
    
    Example: Finding a word in a dictionary or a name in a phone book.
    """
    
    print(f"\n2. Student Answer:\n{student_answer}")
    
    # LLM Evaluation
    print(f"\n3. LLM Evaluation:")
    rubric_scores = llm_evaluator.evaluate_answer(question, student_answer)
    print(f"   Rubric Scores: {json.dumps(rubric_scores, indent=6)}")
    
    # Mastery Evaluation
    print(f"\n4. Mastery Evaluation:")
    mastery_result = mastery_evaluator.evaluate_mastery(rubric_scores)
    print(f"   Mastery Levels: {json.dumps(mastery_result, indent=6)}")
    
    # Simulate some existing mastery states
    mastery_states = {
        "arrays": {"mastery": "Strong", "average_score": 0.9},
        "sorting": {"mastery": "Partial", "average_score": 0.7},
        "binary_search": mastery_result  # Current evaluation
    }
    
    # Prerequisite Check
    print(f"\n5. Prerequisite Check for 'binary_search':")
    prereq_check = prerequisite_checker.check_prerequisites("binary_search", mastery_states)
    print(f"   Prerequisites Met: {prereq_check['prerequisites_met']}")
    print(f"   Recommendation: {prereq_check['recommendation']}")
    
    # Learning Path
    print(f"\n6. Learning Path to master 'Backtracking':")
    learning_path = prerequisite_checker.get_learning_path(mastery_states, "backtracking")
    
    if "error" not in learning_path:
        print(f"   Target: {learning_path['target_concept_name']}")
        print(f"   Steps needed: {learning_path['total_steps']}")
        print(f"   Next step: {learning_path['learning_path'][0]['concept_name']}")

if __name__ == "__main__":
    print("Adaptive Learning System MVP")
    print("Choose demonstration mode:")
    print("1. Full pipeline demo (all concepts)")
    print("2. Single question test")
    
    try:
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            run_pipeline_demo()
        elif choice == "2":
            run_single_question_test()
        else:
            print("Invalid choice. Running full pipeline demo.")
            run_pipeline_demo()
            
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\nError during demo: {e}")
        print("Falling back to simple test...")
        run_single_question_test()