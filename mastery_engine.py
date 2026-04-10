class MasteryEngine:
    def __init__(self, alpha=0.3):  # 🔥 reduced weight of old knowledge
        self.alpha = alpha

    def update(self, old_score, new_score):
        # 🔥 if first attempt, trust new score fully
        if old_score == 0:
            return new_score

        # exponential smoothing
        return self.alpha * old_score + (1 - self.alpha) * new_score

    def score_to_level(self, score):
        if score >= 0.8:
            return "Strong"
        elif score >= 0.5:
            return "Partial"
        else:
            return "Weak"