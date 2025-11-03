import csv
import statistics

def average(marks):
    return sum(marks.values()) / len(marks) if marks else 0

def median(marks):
    return statistics.median(marks.values()) if marks else 0

def maximum(marks):
    return max(marks.values()) if marks else 0

def minimum(marks):
    return min(marks.values()) if marks else 0

def assign_grade(marks):
    grades = {}
    for name, score in marks.items():
        if score >= 90:
            grades[name] = "A"
        elif score >= 80:
            grades[name] = "B"
        elif score >= 70:
            grades[name] = "C"
        elif score >= 60:
            grades[name] = "D"
        else:
            grades[name] = "F"
    return grades

def show_table(marks, grades):
    print("\nName\t\tMarks\tGrade")
    print("--------------------------------")
    for name in marks:
        print(f"{name}\t\t{marks[name]}\t{grades[name]}")
    print("--------------------------------")
    print(f"Average Marks: {average(marks):.2f}")
    print(f"Median Marks : {median(marks):.2f}")
    print(f"Highest Marks: {maximum(marks):.2f}")
    print(f"Lowest Marks : {minimum(marks):.2f}")

def grade_summary(grades):
    print("\nGrade Summary:")
    for g in sorted(set(grades.values())):
        count = list(grades.values()).count(g)
        print(f"Grade {g}: {count} student(s)")

def pass_fail(marks):
    passed = [n for n, m in marks.items() if m >= 40]
    failed = [n for n, m in marks.items() if m < 40]
    print(f"\nPassed Students ({len(passed)}): {', '.join(passed) if passed else 'None'}")
    print(f"Failed Students ({len(failed)}): {', '.join(failed) if failed else 'None'}")

def manual_input():
    data = {}
    n = int(input("Enter number of students: "))
    for i in range(n):
        name = input(f"Enter name of student {i+1}: ").strip().title()
        score = float(input(f"Enter marks for {name}: "))
        data[name] = score
    return data

def csv_input():
    path = input("Enter CSV file path: ").strip()
    data = {}
    try:
        with open(path, newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip().title()
                    try:
                        data[name] = float(row[1])
                    except ValueError:
                        pass
    except FileNotFoundError:
        print("File not found.")
    return data

def gradebook():
    print("\n===================================")
    print("     Welcome to GradeBook Analyzer ")
    print("===================================")
    while True:
        print("\n1. Enter Marks Manually")
        print("2. Import Marks from CSV File")
        print("3. Exit")
        ch = input("Enter your choice: ").strip()
        if ch == "3":
            print("\nThank you for using GradeBook Analyzer!")
            break
        elif ch == "1":
            marks = manual_input()
        elif ch == "2":
            marks = csv_input()
        else:
            print("Invalid choice. Try again.")
            continue
        if not marks:
            print("No data found.")
            continue
        grades = assign_grade(marks)
        show_table(marks, grades)
        grade_summary(grades)
        pass_fail(marks)

if __name__ == "__main__":
    gradebook()
