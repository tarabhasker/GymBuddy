# output functions

def print_title(text):
    # title box
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50)


def print_main_menu():
    # main menu
    print_title("Gym Membership Management System")
    print("1. Member Management")
    print("2. Payment Management")
    print("3. Attendance Management")
    print("4. Reports")
    print("5. Exit")


def print_member(member):
    # show individual member details
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
    # list all members
    print_title(title)
    if not members:
        print("No members found.")
        return
    for m in members:
        print_member(m)


def print_payment(payment):
    # show one payment
    print("-" * 50)
    print(f"Payment ID  : {payment['payment_id']}")
    print(f"Member ID   : {payment['member_id']}")
    print(f"Date Paid   : {payment['date_paid']}")
    print(f"Amount      : {payment['amount']:.2f}")
    print(f"Method      : {payment['method']}")
    print(f"Membership  : {payment['membership_type']}")
    print("-" * 50)


def print_payment_list(payments, title="Payments"):
    # list of payments
    print_title(title)
    if not payments:
        print("No payments found.")
        return
    for p in payments:
        print_payment(p)


def print_attendance(record):
    # show one attendance record
    print("-" * 50)
    print(f"Attendance ID: {record['attendance_id']}")
    print(f"Member ID    : {record['member_id']}")
    print(f"Date         : {record['date']}")
    print(f"Check-in     : {record['checkin']}")
    print(f"Check-out    : {record['checkout']}")
    print("-" * 50)


def print_attendance_list(attendance_list, title="Attendance Records"):
    # list attendance
    print_title(title)
    if not attendance_list:
        print("No attendance records found.")
        return
    for r in attendance_list:
        print_attendance(r)


def print_trainer_summary(members):
    # show members assigned to trainers (only if not expired)
    print_title("Trainer Assignment Summary")

    trainers = {}
    for m in members:
        if m["status"].lower() == "expired":
            continue
        trainer = m["trainer"]
        trainers.setdefault(trainer, []).append(m)

    if not trainers:
        print("No active or pending members assigned.")
        return

    for trainer, t_members in trainers.items():
        print(f"\nTrainer: {trainer}")
        for m in t_members:
            print(
                f"  - {m['member_id']} | {m['name']} "
                f"({m['membership_type']}, {m['schedule']}, Status: {m['status']})"
            )


def print_financial_summary(total_amount, count):
    # simple financial summary
    print_title("Financial Summary")
    print(f"Number of payments: {count}")
    print(f"Total amount      : {total_amount:.2f}")


def print_busiest_day_report(busiest_day, stats_dict):
    # busiest day report
    print_title("Busiest Day of the Week (Attendance)")
    if not stats_dict:
        print("No attendance data available.")
        return

    print("Visits per day:")
    for day, count in stats_dict.items():
        print(f"  {day}: {count} visit(s)")

    if busiest_day:
        print("\nOverall busiest day:", busiest_day)


def print_revenue_by_membership_type(revenue_dict):
    # revenue by membership type
    print_title("Revenue by Membership Type")
    if not revenue_dict:
        print("No payment data available.")
        return

    for mtype, total in revenue_dict.items():
        print(f"{mtype:10} : {total:.2f}")


def print_expiry_alert(expiring_members, days):
    # alert for upcoming expirations
    print_title(f"Automatic Alert: Memberships expiring within {days} day(s)")
    if not expiring_members:
        print("No memberships are expiring in this period.")
        return

    print(f"{len(expiring_members)} member(s) found:")
    for m in expiring_members:
        print(f"- {m['member_id']} | {m['name']} | End Date: {m['end_date']}")
