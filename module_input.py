def input_non_empty(prompt):
    """Ask until user enters non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def input_int_in_range(prompt, min_value, max_value):
    """Ask until user enters int within range."""
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            number = int(value)
            if min_value <= number <= max_value:
                return number
        print(f"Please enter a number between {min_value} and {max_value}.")


def input_positive_float(prompt):
    """Ask until user enters positive float."""
    while True:
        value = input(prompt).strip()
        try:
            num = float(value)
            if num > 0:
                return num
        except ValueError:
            pass
        print("Please enter a positive number.")


def input_date(prompt):
    """
    Ask for a date in format YYYY-MM-DD.
    (We won't parse it as datetime to keep things simple.)
    """
    while True:
        date_str = input(prompt).strip()
        parts = date_str.split("-")
        if len(parts) == 3 and all(p.isdigit() for p in parts):
            year, month, day = parts
            if len(year) == 4 and len(month) == 2 and len(day) == 2:
                return date_str
        print("Invalid date format. Please use YYYY-MM-DD (e.g. 2025-10-17).")


def input_menu_choice(prompt, options):
    """
    Ask for menu choice. options is a list of valid strings like ["1","2","3"].
    """
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print("Invalid choice. Please try again.")


# ---------- SPECIFIC INPUT HELPERS ----------

def input_member_details(membership_types):
    """Collect details for a new member."""
    print("\n--- New Member Registration ---")
    name = input_non_empty("Name: ")
    age = input_int_in_range("Age: ", 10, 100)
    phone = input_non_empty("Phone number: ")

    # Choose membership type
    print("Membership Types:")
    for idx, mtype in enumerate(membership_types, start=1):
        print(f"{idx}. {mtype}")
    choice = input_menu_choice(
        "Choose membership type: ",
        [str(i) for i in range(1, len(membership_types) + 1)]
    )
    membership_type = membership_types[int(choice) - 1]

    start_date = input_date("Start date (YYYY-MM-DD): ")
    end_date = input_date("End date (YYYY-MM-DD): ")

    trainer = input_non_empty("Assigned Trainer: ")
    schedule = input_non_empty(
        "Work schedule / preferred session (e.g. Mon/Wed/Fri 6–8pm): "
    )

    return {
        "name": name,
        "age": age,
        "phone": phone,
        "membership_type": membership_type,
        "start_date": start_date,
        "end_date": end_date,
        "trainer": trainer,
        "schedule": schedule,
    }


def input_payment_details():
    """Collect details for a new payment."""
    print("\n--- Record Payment ---")
    date_paid = input_date("Date paid (YYYY-MM-DD): ")
    amount = input_positive_float("Amount: ")
    method = input_non_empty("Payment method (Cash/Card/Online): ")
    membership_type = input_non_empty("Membership type paid for: ")
    return {
        "date_paid": date_paid,
        "amount": amount,
        "method": method,
        "membership_type": membership_type,
    }


def input_attendance_details():
    """Collect details for attendance record."""
    print("\n--- Record Attendance ---")
    date = input_date("Date (YYYY-MM-DD): ")
    checkin = input_non_empty("Check-in time (e.g. 18:30): ")
    checkout = input_non_empty("Check-out time (e.g. 19:30): ")
    return {
        "date": date,
        "checkin": checkin,
        "checkout": checkout,
    }
