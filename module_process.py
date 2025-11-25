# process functions
from datetime import datetime, timedelta
from collections import Counter


def generate_new_id(prefix, existing_items, key_name):
    # make new ID like M001 / P001
    max_num = 0
    for item in existing_items:
        item_id = item.get(key_name, "")
        if item_id.startswith(prefix):
            try:
                num = int(item_id[len(prefix):])
                if num > max_num:
                    max_num = num
            except ValueError:
                continue
    new_num = max_num + 1
    return f"{prefix}{new_num:03d}"


# MEMBER FUNCTIONS 

def add_member(members, member_data):
    # add new member (starts as pending)
    member_id = generate_new_id("M", members, "member_id")
    member = {
        "member_id": member_id,
        "name": member_data["name"],
        "age": member_data["age"],
        "phone": member_data["phone"],
        "membership_type": member_data["membership_type"],
        "start_date": member_data["start_date"],
        "end_date": member_data["end_date"],
        "status": "pending",
        "trainer": member_data["trainer"],
        "schedule": member_data["schedule"],
    }
    members.append(member)
    return member


def find_member(members, member_id):
    # find member by ID
    for m in members:
        if m["member_id"] == member_id:
            return m
    return None


def update_member(members, member_id, updated_fields):
    # update selected fields of a member
    member = find_member(members, member_id)
    if not member:
        return None
    for key, value in updated_fields.items():
        if key in member and value is not None:
            member[key] = value
    return member


def get_active_members(members):
    # filter active members
    return [m for m in members if m["status"].lower() == "active"]


def get_expired_members(members):
    # filter expired members
    return [m for m in members if m["status"].lower() == "expired"]


def get_pending_members(members):
    # members without payment yet
    return [m for m in members if m["status"].lower() == "pending"]


def get_members_expiring_within_days(members, days_from_today):
    # check who is expiring soon (using datetime)
    result = []
    today = datetime.today().date()
    cutoff = today + timedelta(days=days_from_today)

    for m in members:
        try:
            end_date = datetime.strptime(m["end_date"], "%Y-%m-%d").date()
        except ValueError:
            continue

        if today <= end_date <= cutoff:
            result.append(m)

    return result


def cancel_membership(members, member_id):
    # set member status to expired
    member = find_member(members, member_id)
    if not member:
        return None

    member["status"] = "expired"
    return member


# PAYMENT FUNCTIONS 

def record_payment(members, payments, member_id, payment_data):
    # record new payment for member
    member = find_member(members, member_id)
    if not member:
        return None, None

    payment_id = generate_new_id("P", payments, "payment_id")
    payment = {
        "payment_id": payment_id,
        "member_id": member_id,
        "date_paid": payment_data["date_paid"],
        "amount": payment_data["amount"],
        "method": payment_data["method"],
        "membership_type": payment_data["membership_type"],
    }
    payments.append(payment)

    # update member status after payment
    member["status"] = "active"
    member["membership_type"] = payment_data["membership_type"]

    return payment, member


def get_member_payments(payments, member_id):
    # list payments belonging to one member
    return [p for p in payments if p["member_id"] == member_id]


def get_payments_in_month(payments, year, month):
    # filter payments by month (YYYY-MM)
    filtered = []
    for p in payments:
        parts = p["date_paid"].split("-")
        if len(parts) == 3:
            y, m, _ = parts
            if y == year and m == month:
                filtered.append(p)
    return filtered


def get_revenue_per_membership_type(payments):
    # sum revenue grouped by membership type
    totals = {}
    for p in payments:
        mtype = p["membership_type"]
        totals[mtype] = totals.get(mtype, 0.0) + p["amount"]
    return totals


# ATTENDANCE FUNCTIONS 

def record_attendance(attendance_list, member_id, attendance_data):
    # add attendance record
    attendance_id = generate_new_id("A", attendance_list, "attendance_id")
    record = {
        "attendance_id": attendance_id,
        "member_id": member_id,
        "date": attendance_data["date"],
        "checkin": attendance_data["checkin"],
        "checkout": attendance_data["checkout"],
    }
    attendance_list.append(record)
    return record


def get_member_attendance(attendance_list, member_id):
    # all attendance for one member
    return [a for a in attendance_list if a["member_id"] == member_id]


def get_attendance_on_date(attendance_list, date_str):
    # attendance for specific day
    return [a for a in attendance_list if a["date"] == date_str]


def get_attendance_in_range(attendance_list, start_date, end_date):
    # attendance in date range
    result = []
    for a in attendance_list:
        if start_date <= a["date"] <= end_date:
            result.append(a)
    return result


def get_busiest_day_of_week(attendance_list):
    # find busiest weekday using Counter
    if not attendance_list:
        return None, {}

    weekday_counter = Counter()
    weekday_names = ["Monday", "Tuesday", "Wednesday",
                     "Thursday", "Friday", "Saturday", "Sunday"]

    for a in attendance_list:
        try:
            date_obj = datetime.strptime(a["date"], "%Y-%m-%d").date()
        except ValueError:
            continue
        weekday_index = date_obj.weekday()
        weekday_counter[weekday_names[weekday_index]] += 1

    if not weekday_counter:
        return None, {}

    busiest_day, _ = weekday_counter.most_common(1)[0]
    return busiest_day, dict(weekday_counter)


# TRAINER SUMMARY 

def group_members_by_trainer(members):
    # group members by trainer (exclude expired)
    trainers = {}

    for m in members:
        if m["status"].lower() == "expired":
            continue

        trainer = m["trainer"]
        trainers.setdefault(trainer, []).append(m)

    return trainers
