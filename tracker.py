import datetime

def calorie():
    print("\n============================================")
    print("     Welcome to the Daily Calorie Tracker!  ")
    print("============================================")
    print("This tool helps you record your meals, calculate total calories,")
    print("compare with your daily calorie limit, and optionally save a report.\n")

    meal_names = []
    meal_calories = []

    try:
        num_meals = int(input("How many meals did you have today? "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for i in range(num_meals):
        print(f"\n--- Meal {i+1} ---")
        meal = input("Enter meal name: ").strip().title()
        try:
            calories = float(input(f"Enter calories for {meal}: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            calories = 0
        meal_names.append(meal)
        meal_calories.append(calories)

    total_calories = sum(meal_calories)
    avg_calories = total_calories / num_meals if num_meals > 0 else 0

    try:
        daily_limit = float(input("\nEnter your daily calorie limit: "))
    except ValueError:
        print("Invalid input. Setting daily limit to 0.")
        daily_limit = 0

    print("\n--------------------------------------------")
    if total_calories > daily_limit:
        print(f"  Warning: You have exceeded your daily calorie limit by {total_calories - daily_limit:.2f} calories!")
    else:
        print(f" Great job! You are within your daily limit with {daily_limit - total_calories:.2f} calories remaining.")

    print("\n========= DAILY CALORIE SUMMARY =========")
    print(f"{'Meal Name':<15}{'Calories':>10}")
    print("-----------------------------------------")
    for meal, cal in zip(meal_names, meal_calories):
        print(f"{meal:<15}{cal:>10.2f}")
    print("-----------------------------------------")
    print(f"{'Total':<15}{total_calories:>10.2f}")
    print(f"{'Average':<15}{avg_calories:>10.2f}")
    print("=========================================\n")

    save_choice = input("Would you like to save this session to a file? (yes/no): ").strip().lower()
    if save_choice == "yes":
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"calorie_log_{timestamp}.txt"
        with open(filename, "w") as file:
            file.write("========== DAILY CALORIE TRACKER LOG ==========\n")
            file.write(f"Date & Time: {datetime.datetime.now()}\n\n")
            file.write(f"{'Meal Name':<15}{'Calories':>10}\n")
            file.write("---------------------------------------------\n")
            for meal, cal in zip(meal_names, meal_calories):
                file.write(f"{meal:<15}{cal:>10.2f}\n")
            file.write("---------------------------------------------\n")
            file.write(f"{'Total':<15}{total_calories:>10.2f}\n")
            file.write(f"{'Average':<15}{avg_calories:>10.2f}\n\n")
            if total_calories > daily_limit:
                file.write(f"  Exceeded daily limit by {total_calories - daily_limit:.2f} calories.\n")
            else:
                file.write(f" Within limit by {daily_limit - total_calories:.2f} calories.\n")
        print(f"\nSession saved successfully to {filename}")

    print("\nThank you for using the Daily Calorie Tracker! Stay healthy 😊")

if __name__ == "__main__":
    calorie()
