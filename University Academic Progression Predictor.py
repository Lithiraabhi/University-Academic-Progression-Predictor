import graphics

def validate_input(credit_type):
    """Validate user input for credit values to ensure they're valid integers within allowed range."""
    while True:
        value = input(f"Enter your total {credit_type} credits: ").strip().lower()
        if value == 'q':
            return value
        try:
            value = int(value)
            if value not in [0, 20, 40, 60, 80, 100, 120]:
                print("Out of range.")
                continue
            return value
        except ValueError:
            print("Integer required")

def get_student_data():
    """Collect and validate all credit inputs for a single student."""
    while True:
        pass_credits = validate_input("PASS")
        if pass_credits == 'q':
            return 'q', None, None

        defer_credits = validate_input("DEFER")
        if defer_credits == 'q':
            return 'q', None, None

        fail_credits = validate_input("FAIL")
        if fail_credits == 'q':
            return 'q', None, None

        total = pass_credits + defer_credits + fail_credits
        if total != 120:
            print("Total incorrect.")
            continue

        return pass_credits, defer_credits, fail_credits

def determine_outcome(pass_credits, defer_credits, fail_credits):
    """Determine the student's progression outcome based on their credit distribution."""
    if pass_credits == 120:
        return "Progress"
    elif pass_credits == 100:
        return "Progress (module trailer)"
    elif fail_credits >= 80:
        return "Exclude"
    else:
        return "Module retriever"

def display_histogram(outcomes):
    """Create and display a visual histogram of all student outcomes using graphics library."""
    categories = ["Progress", "Trailer", "Retriever", "Excluded"]
    counts = [
        outcomes.count("Progress"),
        outcomes.count("Progress (module trailer)"),
        outcomes.count("Module retriever"),
        outcomes.count("Exclude")
    ]
    total = sum(counts)
    
    win = graphics.GraphWin("Histogram Results", 800, 600)
    win.setBackground("white")
    
    title = graphics.Text(graphics.Point(400, 30), "Histogram Results")
    title.setSize(24)
    title.setStyle("bold")
    title.draw(win)
    
    max_height = 350
    bar_width = 100
    spacing = 50
    base_y = 450
    max_count = max(counts) if counts else 1
    
    colors = ["#4CAF50", "#2196F3", "#FFC107", "#F44336"]
    
    for i, (category, count, color) in enumerate(zip(categories, counts, colors)):
        x = 200 + i * (bar_width + spacing)
        bar_height = (count / max_count) * max_height if max_count > 0 else 20
        
        bar = graphics.Rectangle(
            graphics.Point(x - bar_width/2, base_y),
            graphics.Point(x + bar_width/2, base_y - bar_height)
        )
        bar.setFill(color)
        bar.setOutline("black")
        bar.setWidth(1)
        bar.draw(win)
        
        if count > 0:
            count_text = graphics.Text(graphics.Point(x, base_y - bar_height - 15), str(count))
            count_text.setSize(14)
            count_text.setStyle("bold")
            count_text.draw(win)
        
        cat_text = graphics.Text(graphics.Point(x, base_y + 30), category)
        cat_text.setSize(12)
        cat_text.draw(win)
    
    total_text = graphics.Text(graphics.Point(400, base_y + 80), f"{total} outcomes in total.")
    total_text.setSize(14)
    total_text.draw(win)
    
    win.getMouse()
    win.close()

def save_to_file(data, filename="progression_data.txt"):
    """Save all progression data to a text file, preserving any existing data."""
    try:
        with open(filename, 'w') as file:
            for item in data:
                file.write(f"{item['outcome']} - {item['pass']}, {item['defer']}, {item['fail']}\n")
    except Exception as e:
        print(f"Error saving to file: {e}")

def display_stored_data(data_list):
    """Display all stored progression data in the required format."""
    print("\nPart 2: List Extension")
    for item in data_list:
        print(f"{item['outcome']} - {item['pass']}, {item['defer']}, {item['fail']}")

def display_file_data(filename="progression_data.txt"):
    """Display data from the text file in the required format."""
    try:
        print("\nPart 3: Text File Extension")
        with open(filename, 'r') as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("No progression data found in file.")

def main():
    """Main function that runs the progression outcome predictor program."""
    print("University Progression Outcome Predictor")
    print("Enter 'q' at any time to quit and view results\n")

    outcomes = []
    data_list = []

    while True:
        result = get_student_data()
        if result[0] == 'q':
            break

        pass_credits, defer_credits, fail_credits = result
        outcome = determine_outcome(pass_credits, defer_credits, fail_credits)
        print(outcome)

        outcomes.append(outcome)
        data_list.append({
            'outcome': outcome,
            'pass': pass_credits,
            'defer': defer_credits,
            'fail': fail_credits
        })

        choice = input("\nWould you like to enter another set of data?\n"
                      "Enter 'y' for yes or 'q' to quit and view results: ").lower()
        if choice == 'q':
            break

    if outcomes:
        display_histogram(outcomes)
        display_stored_data(data_list)
        save_to_file(data_list)
        display_file_data()

if __name__ == "__main__":
    main()
