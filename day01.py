# Day 1 - Data structures warmup
skills = ["sql", "python", "linux", "git"]
print(skills)
print(skills[0])
print(len(skills))

record = {"id": 1, "name": "Arjun", "city": "Chennai"}
print(record["name"])
print(record.get("age", "not found"))

upper_skills = [skill.upper() for skill in skills]
print(upper_skills)

scores = {"python": 60, "sql": 95, "linux": 40}
passed = {k: v for k, v in scores.items() if v >= 50}
print(passed)
