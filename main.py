#!/usr/bin/env python3
"""
Main entry point for the Adaptive Learning System MVP.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from test_pipeline import run_pipeline_demo, run_single_question_test

def main():
    """Main function to run the adaptive learning system demo."""
    print("=" * 60)
    print("ADAPTIVE LEARNING SYSTEM MVP")
    print("=" * 60)
    print("\nThis prototype demonstrates:")
    print("1. Knowledge graph with 5 DSA concepts")
    print("2. Question bank with rubric-based evaluation")
    print("3. LLM-powered answer evaluation")
    print("4. Mastery assessment (Strong/Partial/Weak)")
    print("5. Prerequisite checking")
    print("6. Learning path generation")
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION OPTIONS")
    print("=" * 60)
    print("\n1. Full Pipeline Demo")
    print("   - Tests all 5 concepts")
    print("   - Shows complete evaluation pipeline")
    print("   - Generates learning paths")
    print("\n2. Single Question Test")
    print("   - Focuses on one detailed example")
    print("   - Shows step-by-step evaluation")
    
    while True:
        try:
            choice = input("\nEnter choice (1 or 2, or 'q' to quit): ").strip().lower()
            
            if choice == '1':
                run_pipeline_demo()
                break
            elif choice == '2':
                run_single_question_test()
                break
            elif choice == 'q':
                print("Exiting...")
                sys.exit(0)
            else:
                print("Invalid choice. Please enter 1, 2, or q.")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\nError: {e}")
            print("Running default demo...")
            run_pipeline_demo()
            break

if __name__ == "__main__":
    # Check if required files exist
    required_files = [
        "knowledge_graph.json",
        "question_bank.json",
        "llm_evaluator.py",
        "mastery_evaluator.py",
        "prerequisite_checker.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Error: Missing required files: {', '.join(missing_files)}")
        print("Please run from the adaptive_learning_mvp directory.")
        sys.exit(1)
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("Warning: .env file not found.")
        print("Creating .env.example for reference...")
        if os.path.exists(".env.example"):
            print("Please copy .env.example to .env and add your Gemini API key.")
        else:
            print("Please create a .env file with GEMINI_API_KEY=your_key_here")
        print("\nUsing mock evaluation mode (no API calls required).")
    
    main()