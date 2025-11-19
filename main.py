from module_file import (
    load_members_from_file,
    save_members_to_file,
    load_payments_from_file,
    save_payments_to_file,
    load_attendance_from_file,
    save_attendance_to_file,
)
from module_input import (
    input_menu_choice,
    input_member_details,
    input_payment_details,
    input_attendance_details,
    input_non_empty,
    input_date,
)
from module_output import (
    print_main_menu,
    print_member,
    print_member_list,
    print_payment_list,
    print_attendance_list,
    print_trainer_summary,
    print_financial_summary,
    print_title,
    print_busiest_day_report,
    print_revenue_by_membership_type,
    print_expiry_alert,
)
from module_process import (
    add_member,
    update_member,
    find_member,
    get_active_members,
    get_expired_members,
    get_pending_members,
    get_members_expiring_within_days,
    cancel_membership,
    record_payment,
    get_member_payments,
    get_payments_in_month,
    record_attendance,
    get_member_attendance,
    get_attendance_on_date,
    get_attendance_in_range,
    get_members_expiring_within_days,
    get_busiest_day_of_week,
    get_revenue_per_membership_type,
)


MEMBERSHIP_TYPES = ["Monthly", "Quarterly", "Yearly"]


def member_management_menu(members, payments, attendance):
    while True:
        print_title("Member Management")
        print("1. Register new member")
        print("2. View member by ID")
        print("3. Update member details")
        print("4. List all members")
        print("5. Cancel membership")
        print("6. Back to main menu")

        choice = input_menu_choice("Enter choice: ", ["1", "2", "3", "4", "5", "6"])

        if choice == "1":
            data = input_member_details(MEMBERSHIP_TYPES)
            member = add_member(members, data)
            save_members_to_file(members)
            print_title("Membership Confirmation (Status: PENDING)")
            print_member(member)

        elif choice == "2":
            member_id = input_non_empty("Enter Member ID: ").upper()
            member = find_member(members, member_id)
            if member:
                print_member(member)
            else:
                print("Member not found.")

        elif choice == "3":
            member_id = input_non_empty("Enter Member ID to update: ").upper()
            member = find_member(members, member_id)
            if not member:
                print("Member not found.")
            else:
                print("Leave field empty to keep current value.")
                new_phone = input(
                    "New phone (current: "
                    f"{member['phone']}): "
                ).strip()
                new_trainer = input(
                    "New trainer (current: "
                    f"{member['trainer']}): "
                ).strip()
                new_status = input(
                    "New status (pending/active/expired, current: "
                    f"{member['status']}): "
                ).strip()
                new_schedule = input(
                    "New schedule (current: "
                    f"{member['schedule']}): "
                ).strip()

                updated_fields = {
                    "phone": new_phone or None,
                    "trainer": new_trainer or None,
                    "status": new_status or None,
                    "schedule": new_schedule or None,
                }
                updated_member = update_member(members, member_id, updated_fields)
                save_members_to_file(members)
                print("Member updated:")
                print_member(updated_member)

        elif choice == "4":
            print_member_list(members, "All Members")
        
        elif choice == "5":
            member_id = input_non_empty("Enter Member ID to cancel: ").upper()
            cancelled = cancel_membership(members, member_id)
            if cancelled:
                save_members_to_file(members)
                print_title("Membership Cancelled")
                print_member(cancelled)
            else:
                print("Member not found.")

        elif choice == "6":
            break


def payment_management_menu(members, payments):
    while True:
        print_title("Payment Management")
        print("1. Record payment")
        print("2. View member payment history")
        print("3. Back to main menu")
        choice = input_menu_choice("Enter choice: ", ["1", "2", "3"])

        if choice == "1":
            member_id = input_non_empty("Enter Member ID: ").upper()
            payment_data = input_payment_details()
            payment, member = record_payment(members, payments, member_id, payment_data)
            if payment is None:
                print("Member not found. Payment cancelled.")
            else:
                save_payments_to_file(payments)
                save_members_to_file(members)
                print_title("Payment Receipt (Status: ACTIVE)")
                print_member(member)
                print_payment_list([payment], "Payment Recorded")

        elif choice == "2":
            member_id = input_non_empty("Enter Member ID: ").upper()
            member_payments = get_member_payments(payments, member_id)
            print_payment_list(member_payments, f"Payment History for {member_id}")

        elif choice == "3":
            break


def attendance_management_menu(members, attendance):
    while True:
        print_title("Attendance Management")
        print("1. Record attendance (check-in & check-out)")
        print("2. View member attendance")
        print("3. View attendance by date")
        print("4. Back to main menu")
        choice = input_menu_choice("Enter choice: ", ["1", "2", "3", "4"])

        if choice == "1":
            member_id = input_non_empty("Enter Member ID: ").upper()
            member = find_member(members, member_id)
            if not member:
                print("Member not found.")
            else:
                att_data = input_attendance_details()
                record = record_attendance(attendance, member_id, att_data)
                save_attendance_to_file(attendance)
                print_title("Attendance Recorded")
                print_attendance_list([record], "New Attendance")

        elif choice == "2":
            member_id = input_non_empty("Enter Member ID: ").upper()
            records = get_member_attendance(attendance, member_id)
            print_attendance_list(records, f"Attendance for member {member_id}")

        elif choice == "3":
            date_str = input_date("Enter date (YYYY-MM-DD): ")
            records = get_attendance_on_date(attendance, date_str)
            print_attendance_list(records, f"Attendance on {date_str}")

        elif choice == "4":
            break

def advanced_analytics_menu(members, payments, attendance):
    while True:
        print_title("Advanced Analytics")
        print("1. Members expiring within N days from today")
        print("2. Busiest day of the week (attendance)")
        print("3. Revenue by membership type")
        print("4. Back to Reports menu")
        choice = input_menu_choice("Enter choice: ", ["1", "2", "3", "4"])

        if choice == "1":
            days_str = input_non_empty("Enter number of days from today: ")
            if not days_str.isdigit():
                print("Please enter a valid positive number.")
                continue
            days = int(days_str)
            expiring_soon = get_members_expiring_within_days(members, days)
            print_member_list(
                expiring_soon,
                f"Memberships expiring within {days} day(s) from today"
            )

        elif choice == "2":
            busiest_day, stats = get_busiest_day_of_week(attendance)
            print_busiest_day_report(busiest_day, stats)

        elif choice == "3":
            revenue = get_revenue_per_membership_type(payments)
            print_revenue_by_membership_type(revenue)

        elif choice == "4":
            break


def reports_menu(members, payments, attendance):
    while True:
        print_title("Reports")
        print("1. List active members")
        print("2. List expired members")
        print("3. List pending members (unpaid)")
        print("4. Monthly financial summary")
        print("5. Daily attendance report")
        print("6. Weekly attendance report (date range)")
        print("7. Trainer assignment summary")
        print("8. Advanced analytics")
        print("9. Back to main menu")
        choice = input_menu_choice("Enter choice: ",
                                   ["1", "2", "3", "4", "5",
                                    "6", "7", "8", "9"])

        if choice == "1":
            active = get_active_members(members)
            print_member_list(active, "Active Members")

        elif choice == "2":
            expired = get_expired_members(members)
            print_member_list(expired, "Expired Members")

        elif choice == "3":
            pending = get_pending_members(members)
            print_member_list(pending, "Pending Members (Need Payment)")

        elif choice == "4":
            year = input_non_empty("Year (YYYY): ")
            month = input_non_empty("Month (MM): ")
            month_payments = get_payments_in_month(payments, year, month)
            total = sum(p["amount"] for p in month_payments)
            print_payment_list(month_payments, f"Payments for {year}-{month}")
            print_financial_summary(total, len(month_payments))

        elif choice == "5":
            date_str = input_date("Enter date (YYYY-MM-DD): ")
            records = get_attendance_on_date(attendance, date_str)
            print_attendance_list(records, f"Daily Attendance on {date_str}")

        elif choice == "6":
            print("Enter week range (e.g. Monday–Sunday).")
            start_date = input_date("Start date (YYYY-MM-DD): ")
            end_date = input_date("End date   (YYYY-MM-DD): ")
            records = get_attendance_in_range(attendance, start_date, end_date)
            print_attendance_list(
                records,
                f"Weekly Attendance from {start_date} to {end_date}"
            )

        elif choice == "7":
            print_trainer_summary(members)

        elif choice == "8":
            advanced_analytics_menu(members, payments, attendance)

        elif choice == "9":
            break


def main():
    # Load existing data 
    members = load_members_from_file()
    payments = load_payments_from_file()
    attendance = load_attendance_from_file()

    # Expiry alert (if have)
    DAYS_AHEAD = 7 
    expiring_soon = get_members_expiring_within_days(members, DAYS_AHEAD)
    if expiring_soon:  
        print_expiry_alert(expiring_soon, DAYS_AHEAD)

    while True:
        print_main_menu()
        choice = input_menu_choice("Enter choice: ", ["1", "2", "3", "4", "5"])

        if choice == "1":
            member_management_menu(members, payments, attendance)
        elif choice == "2":
            payment_management_menu(members, payments)
        elif choice == "3":
            attendance_management_menu(members, attendance)
        elif choice == "4":
            reports_menu(members, payments, attendance)
        elif choice == "5":
            print("Exiting program. Goodbye!")
            save_members_to_file(members)
            save_payments_to_file(payments)
            save_attendance_to_file(attendance)
            break


if __name__ == "__main__":
    main()
