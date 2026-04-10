def normalize(text):
    return text.lower().replace("-", " ").replace("(", "").replace(")", "")


def evaluate_answer(answer, keywords):
    answer = normalize(answer)
    score = 0

    for word, weight in keywords.items():
        if word in answer:
            score += weight

    # 🔹 fallback: give partial credit if answer is meaningful
    if score == 0 and len(answer.split()) > 3:
        score = 0.4

    return min(score, 1.0)


def ask_questions(concept):
    print(f"\n--- Questions for {concept} ---")

    questions = {
        "arrays": [
            {
                "q": "What is an array?",
                "keywords": {
                    "collection": 0.3,
                    "list": 0.3,
                    "elements": 0.4,
                    "values": 0.4,
                    "index": 0.3,
                    "position": 0.3
                }
            },
            {
                "q": "What is time complexity of accessing an element?",
                "keywords": {
                    "o1": 1.0,
                    "constant": 1.0
                }
            }
        ],

        "sorting": [
            {
                "q": "What is sorting?",
                "keywords": {
                    "arrange": 0.5,
                    "order": 0.5,
                    "organize": 0.5
                }
            },
            {
                "q": "Name any sorting algorithms",
                "keywords": {
                    "bubble": 0.3,
                    "merge": 0.3,
                    "quick": 0.3,
                    "heap": 0.3,
                    "insertion": 0.3,
                    "selection": 0.3
                }
            },
            {
                "q": "What is time complexity of merge sort?",
                "keywords": {
                    "n log n": 1.0,
                    "nlogn": 1.0
                }
            }
        ],

        "binary_search": [
            {
                "q": "What is binary search?",
                "keywords": {
                    "sorted": 0.3,
                    "divide": 0.3,
                    "half": 0.4
                }
            },
            {
                "q": "What is its time complexity?",
                "keywords": {
                    "log n": 1.0,
                    "logn": 1.0
                }
            },
            {
                "q": "When can binary search be applied?",
                "keywords": {
                    "sorted": 1.0
                }
            }
        ],

        "recursion": [
            {
                "q": "What is recursion?",
                "keywords": {
                    "function": 0.3,
                    "itself": 0.4,
                    "call": 0.3
                }
            },
            {
                "q": "What is a base case?",
                "keywords": {
                    "stop": 0.5,
                    "condition": 0.5,
                    "termination": 0.5
                }
            },
            {
                "q": "Why is base case important?",
                "keywords": {
                    "infinite": 0.5,
                    "termination": 0.5,
                    "stop": 0.5
                }
            }
        ],

        "backtracking": [
            {
                "q": "What is backtracking?",
                "keywords": {
                    "recursion": 0.3,
                    "choice": 0.3,
                    "backtrack": 0.4,
                    "undo": 0.4
                }
            },
            {
                "q": "Give an example of backtracking problem",
                "keywords": {
                    "n queen": 0.5,
                    "sudoku": 0.5,
                    "maze": 0.5
                }
            }
        ]
    }

    concept_questions = questions.get(concept, [])

    if not concept_questions:
        print("No questions available. Default score 0.5")
        return 0.5

    total_score = 0

    for i, item in enumerate(concept_questions, 1):
        answer = input(f"Q{i}. {item['q']} → ")

        score = evaluate_answer(answer, item["keywords"])
        print(f"Score: {score:.2f}")

        total_score += score

    final_score = total_score / len(concept_questions)

    print(f"\nFinal score for {concept}: {final_score:.2f}")

    return final_score