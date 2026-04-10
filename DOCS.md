# Adaptive Learning System – Final Approach

## Overview

This project builds an adaptive learning system that:

- Tracks student understanding
- Uses a knowledge graph for concept dependencies
- Updates a learning roadmap based on mastery

---

## Core Idea

The system uses **two knowledge graphs**:

### 1. Static Knowledge Graph
- Fixed structure of concepts (DSA)
- Defines prerequisites
- Same for all students

### 2. Dynamic Knowledge Graph
- Stores student mastery per concept
- Updates after each interaction

---

## Flow

1. Student answers a question
2. Answer is evaluated (LLM or mock)
3. Scores are converted to mastery level
4. Mastery is updated
5. Prerequisites are checked
6. Roadmap is updated

---

## Mastery Levels

- Strong (≥ 0.8)
- Partial (≥ 0.5)
- Weak (< 0.5)

---

## Planner Logic

- If prerequisite is **Weak** → revise it
- If prerequisite is **Partial** → practice + continue
- If prerequisite is **Strong** → move forward

---

## Features

- Knowledge graph-based learning
- Mastery tracking
- Prerequisite checking
- Roadmap adaptation
- Simple CLI interaction

---

## Notes

- Prototype uses small DSA graph
- Uses rule-based logic (no training)
- Designed for experimentation and research