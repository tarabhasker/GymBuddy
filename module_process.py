# BUSINESS LOGIC FUNCTIONS

def generate_new_id(prefix, existing_items, key_name):
    """Generate new ID like M001, P002 based on existing list."""
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


# ---------- MEMBER FUNCTIONS ----------

def add_member(members, member_data):
    """Create new member dict and add to list.

    New members start with status 'pending' (no payment yet).
    """
    member_id = generate_new_id("M", members, "member_id")
    member = {
        "member_id": member_id,
        "name": member_data["name"],
        "age": member_data["age"],
        "phone": member_data["phone"],
        "membership_type": member_data["membership_type"],
        "start_date": member_data["start_date"],
        "end_date": member_data["end_date"],
        "status": "pending",  # pending payment
        "trainer": member_data["trainer"],
        "schedule": member_data["schedule"],
    }
    members.append(member)
    return member


def find_member(members, member_id):
    for m in members:
        if m["member_id"] == member_id:
            return m
    return None


def update_member(members, member_id, updated_fields):
    member = find_member(members, member_id)
    if not member:
        return None
    for key, value in updated_fields.items():
        if key in member and value is not None:
            member[key] = value
    return member


def get_active_members(members):
    return [m for m in members if m["status"].lower() == "active"]


def get_expired_members(members):
    return [m for m in members if m["status"].lower() == "expired"]


def get_pending_members(members):
    """Members who have registered but not yet paid."""
    return [m for m in members if m["status"].lower() == "pending"]


def get_members_expiring_before_date(members, cutoff_date):
    """
    Return members whose membership end_date is <= cutoff_date.

    Dates are in YYYY-MM-DD so string comparison works.
    """
    result = []
    for m in members:
        if m["end_date"] <= cutoff_date:
            result.append(m)
    return result


# ---------- PAYMENT FUNCTIONS ----------

def record_payment(members, payments, member_id, payment_data):
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

    # Update member status to active (paid)
    member["status"] = "active"
    # Optionally update membership_type based on payment
    member["membership_type"] = payment_data["membership_type"]

    return payment, member


def get_member_payments(payments, member_id):
    return [p for p in payments if p["member_id"] == member_id]


def get_payments_in_month(payments, year, month):
    """Return payments in a given YYYY and MM (strings)."""
    filtered = []
    for p in payments:
        # date_paid format: YYYY-MM-DD
        parts = p["date_paid"].split("-")
        if len(parts) == 3:
            y, m, _ = parts
            if y == year and m == month:
                filtered.append(p)
    return filtered


# ---------- ATTENDANCE FUNCTIONS ----------

def record_attendance(attendance_list, member_id, attendance_data):
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
    return [a for a in attendance_list if a["member_id"] == member_id]


def get_attendance_on_date(attendance_list, date_str):
    return [a for a in attendance_list if a["date"] == date_str]


def get_attendance_in_range(attendance_list, start_date, end_date):
    """
    Return attendance records between start_date and end_date (inclusive).
    Dates in YYYY-MM-DD allow string comparison.
    """
    result = []
    for a in attendance_list:
        if start_date <= a["date"] <= end_date:
            result.append(a)
    return result


# ---------- TRAINER SUMMARY ----------

def group_members_by_trainer(members):
    trainers = {}
    for m in members:
        t = m["trainer"]
        trainers.setdefault(t, []).append(m)
    return trainers
