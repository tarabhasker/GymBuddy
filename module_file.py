import os

DATA_FOLDER = "data"
MEMBERS_FILE = os.path.join(DATA_FOLDER, "members.txt")
PAYMENTS_FILE = os.path.join(DATA_FOLDER, "payments.txt")
ATTENDANCE_FILE = os.path.join(DATA_FOLDER, "attendance.txt")


def ensure_data_folder():
    """Create data folder if it does not exist."""
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)


# ---------- MEMBERS ----------

def load_members_from_file():
    """Read members from text file and return as list of dicts."""
    ensure_data_folder()
    members = []

    if not os.path.exists(MEMBERS_FILE):
        return members

    with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split(",")
            # member_id, name, age, phone, membership_type, start_date,
            # end_date, status, trainer, schedule
            if len(fields) < 10:
                continue  # skip invalid/old lines
            member = {
                "member_id": fields[0],
                "name": fields[1],
                "age": int(fields[2]),
                "phone": fields[3],
                "membership_type": fields[4],
                "start_date": fields[5],
                "end_date": fields[6],
                "status": fields[7],
                "trainer": fields[8],
                "schedule": fields[9],
            }
            members.append(member)
    return members


def save_members_to_file(members):
    """Write members list to text file."""
    ensure_data_folder()
    with open(MEMBERS_FILE, "w", encoding="utf-8") as f:
        for m in members:
            line = ",".join([
                m["member_id"],
                m["name"],
                str(m["age"]),
                m["phone"],
                m["membership_type"],
                m["start_date"],
                m["end_date"],
                m["status"],
                m["trainer"],
                m["schedule"],
            ])
            f.write(line + "\n")


# ---------- PAYMENTS ----------

def load_payments_from_file():
    """Read payments from text file and return as list of dicts."""
    ensure_data_folder()
    payments = []

    if not os.path.exists(PAYMENTS_FILE):
        return payments

    with open(PAYMENTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split(",")
            if len(fields) < 6:
                continue
            payment = {
                "payment_id": fields[0],
                "member_id": fields[1],
                "date_paid": fields[2],
                "amount": float(fields[3]),
                "method": fields[4],
                "membership_type": fields[5],
            }
            payments.append(payment)
    return payments


def save_payments_to_file(payments):
    """Write payments list to text file."""
    ensure_data_folder()
    with open(PAYMENTS_FILE, "w", encoding="utf-8") as f:
        for p in payments:
            line = ",".join([
                p["payment_id"],
                p["member_id"],
                p["date_paid"],
                f"{p['amount']:.2f}",
                p["method"],
                p["membership_type"],
            ])
            f.write(line + "\n")


# ---------- ATTENDANCE ----------

def load_attendance_from_file():
    """Read attendance records from text file and return list of dicts."""
    ensure_data_folder()
    attendance_list = []

    if not os.path.exists(ATTENDANCE_FILE):
        return attendance_list

    with open(ATTENDANCE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            fields = line.split(",")
            if len(fields) < 5:
                continue
            record = {
                "attendance_id": fields[0],
                "member_id": fields[1],
                "date": fields[2],
                "checkin": fields[3],
                "checkout": fields[4],
            }
            attendance_list.append(record)
    return attendance_list


def save_attendance_to_file(attendance_list):
    """Write attendance list to text file."""
    ensure_data_folder()
    with open(ATTENDANCE_FILE, "w", encoding="utf-8") as f:
        for a in attendance_list:
            line = ",".join([
                a["attendance_id"],
                a["member_id"],
                a["date"],
                a["checkin"],
                a["checkout"],
            ])
            f.write(line + "\n")
