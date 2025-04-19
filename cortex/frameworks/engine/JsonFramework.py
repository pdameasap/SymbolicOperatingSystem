import json
from ReflectiveFrameworkBase import ReflectiveFrameworkBase

class JsonFramework(ReflectiveFrameworkBase):
    def __init__(self, json_path):
        super().__init__()
        with open(json_path, 'r') as f:
            self.data = json.load(f)

        self.framework_name = self.data.get("framework", "UnnamedJsonFramework")
        self.version = self.data.get("version", "0.0.1")
        self.description = self.data.get("description", "No description provided.")
        self.questions = self.data.get("questions", {})
        self.meta_heuristics = self.data.get("meta_heuristics", {})
        self.graded_levels = self.data.get("graded_levels", {})
        self.output_format = self.data.get("output_format", {})

    def query(self, question, unit=None, metadata=None, flags=None):
        return super().query(question, unit, metadata, flags)

    def evaluate(self, evaluand):
        results = {}
        z_total = 0.0
        count = 0

        for z_key, q in self.questions.items():
            label = q.get("label", z_key)
            question = q.get("question", f"What is the {label.lower()} of this?")
            score = self.query(question, evaluand)
            results[z_key] = {
                "label": label,
                "score": score,
                "question": question
            }
            z_total += score
            count += 1

        average = z_total / max(count, 1)
        results["scalar_average"] = average

        if self.graded_levels:
            graded_result = self.assign_grade(average, results)
            if graded_result:
                results["grade"] = graded_result

        return results

    def assign_grade(self, average, results):
        # grades should be in increasing order, sorted numerically
        sorted_grades = sorted(self.graded_levels.items(), key=lambda x: int(x[0]))
        highest_met = None

        for grade_value, grade_info in sorted_grades:
            try:
                label = grade_info.get("label", f"{grade_value}%")
                criteria = grade_info.get("criteria", "")

                # Heuristic: interpret '≥ X' in criteria if it's a scalar clause
                if f">= {int(grade_value) / 100:.2f}" in criteria or average >= int(grade_value) / 100.0:
                    highest_met = f"{label} ({grade_value}%)"
            except Exception:
                continue

        return highest_met
