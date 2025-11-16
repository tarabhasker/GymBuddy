def print_title(text):
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50)


def print_main_menu():
    print_title("Gym Membership Management System")
    print("1. Member Management")
    print("2. Payment Management")
    print("3. Attendance Management")
    print("4. Reports")
    print("5. Exit")


def print_member(member):
    """Print details of a single member."""
    print("-" * 50)
    print(f"Member ID   : {member['member_id']}")
    print(f"Name        : {member['name']}")
    print(f"Age         : {member['age']}")
    print(f"Phone       : {member['phone']}")
    print(f"Type        : {member['membership_type']}")
    print(f"Start Date  : {member['start_date']}")
    print(f"End Date    : {member['end_date']}")
    print(f"Status      : {member['status']}")
    print(f"Trainer     : {member['trainer']}")
    print(f"Schedule    : {member['schedule']}")
    print("-" * 50)


def print_member_list(members, title="Members"):
    print_title(title)
    if not members:
        print("No members found.")
        return
    for m in members:
        print_member(m)


def print_payment(payment):
    print("-" * 50)
    print(f"Payment ID  : {payment['payment_id']}")
    print(f"Member ID   : {payment['member_id']}")
    print(f"Date Paid   : {payment['date_paid']}")
    print(f"Amount      : {payment['amount']:.2f}")
    print(f"Method      : {payment['method']}")
    print(f"Membership  : {payment['membership_type']}")
    print("-" * 50)


def print_payment_list(payments, title="Payments"):
    print_title(title)
    if not payments:
        print("No payments found.")
        return
    for p in payments:
        print_payment(p)


def print_attendance(record):
    print("-" * 50)
    print(f"Attendance ID: {record['attendance_id']}")
    print(f"Member ID    : {record['member_id']}")
    print(f"Date         : {record['date']}")
    print(f"Check-in     : {record['checkin']}")
    print(f"Check-out    : {record['checkout']}")
    print("-" * 50)


def print_attendance_list(attendance_list, title="Attendance Records"):
    print_title(title)
    if not attendance_list:
        print("No attendance records found.")
        return
    for r in attendance_list:
        print_attendance(r)


def print_trainer_summary(members):
    """Show members grouped by trainer, including their schedule."""
    print_title("Trainer Assignment Summary")
    if not members:
        print("No members found.")
        return

    trainers = {}
    for m in members:
        t = m["trainer"]
        trainers.setdefault(t, []).append(m)

    for trainer, t_members in trainers.items():
        print(f"\nTrainer: {trainer}")
        for m in t_members:
            print(
                f"  - {m['member_id']} | {m['name']} "
                f"({m['membership_type']}, {m['schedule']})"
            )


def print_financial_summary(total_amount, count):
    print_title("Financial Summary")
    print(f"Number of payments: {count}")
    print(f"Total amount      : {total_amount:.2f}")
