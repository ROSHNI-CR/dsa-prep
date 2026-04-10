<!-- # Adaptive Learning System MVP
# v1 by Jhanvi

A research prototype for an adaptive learning system that diagnoses student understanding and updates a learning roadmap.

## Features
- Knowledge graph with 5 DSA concepts
- Question bank with 2 questions per concept
- LLM evaluation module with rubric scoring
- Mastery evaluation (Strong/Partial/Weak)
- Prerequisite checking
- Simple CLI demonstration

## Installation
```bash
pip install openai python-dotenv
```

## Setup
1. Get an OpenAI API key from https://platform.openai.com/api-keys
2. Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage
```bash
python test_pipeline.py
```

## Project Structure
```
adaptive_learning_mvp/
├── README.md
├── requirements.txt
├── .env.example
├── knowledge_graph.json
├── question_bank.json
├── llm_evaluator.py
├── mastery_evaluator.py
├── prerequisite_checker.py
└── test_pipeline.py
```
 -->

# Adaptive Learning System MVP
# v2 - updated by Soumashree
A research prototype for an adaptive learning system that diagnoses student understanding and updates a learning roadmap.

---

## Features

- Static knowledge graph (DSA concepts)
- Dynamic learner state tracking
- Mastery evaluation (Strong / Partial / Weak)
- Prerequisite checking
- Adaptive roadmap generation
- Simple CLI demonstration

---

## Installation

```bash
pip install -r requirements.txt