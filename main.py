import os
import csv
import json

# ======================
# B1 — FILE CHECK
# ======================
print("Checking file...")

csv_path = "students.csv"

if not os.path.exists(csv_path):
    print("Error: students.csv not found. Please download the file from LMS.")
    exit()
else:
    print("File found: students.csv")

print("Checking output folder...")

output_dir = "output"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print("Output folder created: output/")
else:
    print("Output folder exists: output/")

# ======================
# B2 — READ CSV
# ======================
students = []

with open(csv_path, encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        students.append(row)

print("Total students:", len(students))

print("First 5 rows:")
print("-" * 30)

for s in students[:5]:
    print(f"{s['student_id']} | {s['age']} | {s['gender']} | {s['country']} | GPA: {s['GPA']}")

print("-" * 30)

# ======================
# B3 — COUNTRY ANALYSIS
# ======================
country_counts = {}

for s in students:
    country = s["country"]
    if country in country_counts:
        country_counts[country] += 1
    else:
        country_counts[country] = 1

print("-" * 30)
print("Students by Country")
print("-" * 30)

for country, count in country_counts.items():
    print(country, ":", count)

top_3 = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:3]

print("-" * 30)
print("Top 3 Countries:")

for i, (country, count) in enumerate(top_3, 1):
    print(f"{i}. {country} : {count}")

print("-" * 30)

# ======================
# B4 — SAVE JSON
# ======================
result = {
    "analysis": "Country Analysis",
    "total_students": len(students),
    "total_countries": len(country_counts),
    "top_3_countries": [
        {"country": c, "count": count} for c, count in top_3
    ],
    "all_countries": country_counts
}

json_path = os.path.join(output_dir, "result.json")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

print("==============================")
print("ANALYSIS RESULT")
print("==============================")
print("Analysis : Country Analysis")
print("Total students :", len(students))
print("Total countries :", len(country_counts))
print("------------------------------")

for i, item in enumerate(result["top_3_countries"], 1):
    print(f"{i}. {item['country']} : {item['count']}")

print("==============================")
print("Result saved to output/result.json")
