import csv
from code_feed.models import ProblemModel

csv_file_path = "problem_list.csv"

with open(csv_file_path, "r", encoding="utf-8") as file:
    csv_rows = csv.reader(file)
    next(csv_rows)
    for number, title, link, level in csv_rows:
        ProblemModel.objects.create(
            number=int(number),
            title=title,
            link=link,
            level=int(level),
        )

print("complete!")
