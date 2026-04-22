import os
import csv
import json

# ======================
# CLASS 1 — FILE MANAGER
# ======================
class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"Error: {self.filename} not found.")
            return False

    def create_output_folder(self, folder='output'):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print("Output folder created: output/")
        else:
            print("Output folder already exists: output/")


# ======================
# CLASS 2 — DATA LOADER
# ======================
class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.students.append(row)

            print(f"Data loaded successfully: {len(self.students)} students")
            return self.students

        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            return []

        except Exception as e:
            print("Unexpected error:", e)
            return []

    def preview(self, n=5):
        print("First", n, "rows:")
        print("-" * 30)

        for s in self.students[:n]:
            print(f"{s['student_id']} | {s['age']} | {s['gender']} | {s['country']} | GPA: {s['GPA']}")

        print("-" * 30)


# ======================
# CLASS 3 — DATA ANALYSER
# ======================
class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        country_counts = {}

        for s in self.students:
            try:
                country = s["country"]

                if country in country_counts:
                    country_counts[country] += 1
                else:
                    country_counts[country] = 1

            except Exception:
                print(f"Warning: skipping row {s.get('student_id', 'unknown')}")
                continue

        top_3 = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:3]

        # lambda / filter / map
        high_gpa = list(filter(lambda s: float(s['GPA']) > 3.5, self.students))
        gpa_values = list(map(lambda s: float(s['GPA']), self.students))

        good_attendance = list(filter(
            lambda s: float(s['class_attendance_percent']) > 90,
            self.students
        ))

        self.result = {
            "analysis": "Country Analysis",
            "total_students": len(self.students),
            "total_countries": len(country_counts),
            "top_3_countries": [
                {"country": c, "count": count} for c, count in top_3
            ],
            "all_countries": country_counts,
            "high_gpa_count": len(high_gpa),
            "attendance_above_90": len(good_attendance),
            "gpa_sample": gpa_values[:5]
        }

        return self.result

    def print_results(self):
        print("------------------------------")
        print("Country Analysis")
        print("------------------------------")

        print("Total students :", self.result["total_students"])
        print("Total countries :", self.result["total_countries"])

        print("------------------------------")
        print("Top 3 Countries:")

        for i, item in enumerate(self.result["top_3_countries"], 1):
            print(f"{i}. {item['country']} : {item['count']}")

        print("------------------------------")
        print("Lambda / Map / Filter")

        print("Students with GPA > 3.5 :", self.result["high_gpa_count"])
        print("GPA values (first 5) :", self.result["gpa_sample"])
        print("Students attendance > 90% :", self.result["attendance_above_90"])

        print("------------------------------")


# ======================
# CLASS 4 — RESULT SAVER
# ======================
class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(self.result, f, indent=4)

            print(f"Result saved to {self.output_path}")

        except Exception as e:
            print("Error saving file:", e)


# ======================
# MAIN
# ======================
if __name__ == "__main__":
    fm = FileManager('students.csv')

    if not fm.check_file():
        print("Stopping program.")
        exit()

    fm.create_output_folder()

    dl = DataLoader('students.csv')
    dl.load()
    dl.preview()

    analyser = DataAnalyser(dl.students)
    analyser.analyse()
    analyser.print_results()

    saver = ResultSaver(analyser.result, 'output/result.json')
    saver.save_json()
