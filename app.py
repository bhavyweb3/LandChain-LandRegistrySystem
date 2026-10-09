from flask import Flask, render_template, request, redirect, url_for, session
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = "landchain_demo_key"

blockchain = Blockchain()

USERNAME = "admin"
PASSWORD = "admin123"


def logged_in():
    return session.get("logged_in") == True


def current_land_records():
    lands = {}

    for block in blockchain.chain:
        data = block.land_data
        if not isinstance(data, dict) or "land_id" not in data:
            continue

        land_id = data["land_id"]

        if data.get("transaction_type") == "LAND_REGISTRATION":
            lands[land_id] = {
                "land_id": land_id,
                "owner": data.get("owner", ""),
                "location": data.get("location", ""),
                "area": data.get("area", ""),
                "survey_number": data.get("survey_number", ""),
                "status": "Registered",
                "block": block.index
            }

        elif data.get("transaction_type") == "OWNERSHIP_TRANSFER":
            if land_id in lands:
                lands[land_id]["owner"] = data.get("owner", lands[land_id]["owner"])
                lands[land_id]["status"] = "Transferred"
                lands[land_id]["block"] = block.index

    return list(lands.values())


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))

        error = "Invalid username or password."

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard():
    if not logged_in():
        return redirect(url_for("login"))

    lands = current_land_records()
    search = request.args.get("search", "").strip().lower()

    if search:
        lands = [
            land for land in lands
            if search in land["land_id"].lower()
            or search in land["owner"].lower()
            or search in land["location"].lower()
            or search in land["survey_number"].lower()
        ]

    registrations = sum(
        1 for block in blockchain.chain
        if isinstance(block.land_data, dict)
        and block.land_data.get("transaction_type") == "LAND_REGISTRATION"
    )

    transfers = sum(
        1 for block in blockchain.chain
        if isinstance(block.land_data, dict)
        and block.land_data.get("transaction_type") == "OWNERSHIP_TRANSFER"
    )

    return render_template(
        "dashboard.html",
        lands=lands,
        search=search,
        registrations=registrations,
        transfers=transfers,
        blocks=len(blockchain.chain),
        valid=blockchain.verify_chain()
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if not logged_in():
        return redirect(url_for("login"))

    error = ""

    if request.method == "POST":
        land_id = request.form.get("land_id", "").strip()
        owner = request.form.get("owner", "").strip()
        location = request.form.get("location", "").strip()
        area = request.form.get("area", "").strip()
        survey = request.form.get("survey_number", "").strip()

        if not all([land_id, owner, location, area, survey]):
            error = "Please fill all fields."
        elif blockchain.find_land(land_id):
            error = "Land ID already exists."
        else:
            try:
                if float(area) <= 0:
                    error = "Area must be greater than 0."
            except ValueError:
                error = "Area must be a number."

        if not error:
            blockchain.add_block({
                "transaction_type": "LAND_REGISTRATION",
                "land_id": land_id,
                "owner": owner,
                "location": location,
                "area": area,
                "survey_number": survey
            })
            return redirect(url_for("dashboard"))

    return render_template("register_land.html", error=error)


@app.route("/verify", methods=["GET", "POST"])
def verify():
    records = []
    land_id = ""

    if request.method == "POST":
        land_id = request.form.get("land_id", "").strip()
        records = blockchain.find_land(land_id)

    return render_template(
        "verify_land.html",
        records=records,
        land_id=land_id,
        valid=blockchain.verify_chain()
    )


@app.route("/land/<land_id>")
def land_details(land_id):
    records = blockchain.find_land(land_id)

    if not records:
        return "Land record not found.", 404

    latest = records[-1]
    data = latest.land_data

    land = {
        "land_id": land_id,
        "owner": data.get("owner", ""),
        "location": data.get("location", ""),
        "area": data.get("area", ""),
        "survey_number": data.get("survey_number", ""),
        "status": "Transferred" if data.get("transaction_type") == "OWNERSHIP_TRANSFER" else "Registered"
    }

    return render_template(
        "land_details.html",
        land=land,
        records=records,
        valid=blockchain.verify_chain()
    )


@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if not logged_in():
        return redirect(url_for("login"))

    message = ""
    success = False

    if request.method == "POST":
        land_id = request.form.get("land_id", "").strip()
        new_owner = request.form.get("new_owner", "").strip()
        records = blockchain.find_land(land_id)

        if not land_id or not new_owner:
            message = "Please enter Land ID and new owner."
        elif not records:
            message = "Land ID not found."
        else:
            old_owner = records[-1].land_data.get("owner", "")
            if old_owner.lower() == new_owner.lower():
                message = "New owner must be different from current owner."
            else:
                last = records[-1].land_data
                blockchain.add_block({
                    "transaction_type": "OWNERSHIP_TRANSFER",
                    "land_id": land_id,
                    "previous_owner": old_owner,
                    "owner": new_owner,
                    "location": last.get("location", ""),
                    "area": last.get("area", ""),
                    "survey_number": last.get("survey_number", "")
                })
                message = "Ownership transferred successfully."
                success = True

    return render_template(
        "transfer_land.html",
        message=message,
        success=success
    )


@app.route("/certificate/<land_id>")
def certificate(land_id):
    records = blockchain.find_land(land_id)

    if not records:
        return "Land record not found.", 404

    data = records[-1].land_data

    certificate = {
        "land_id": land_id,
        "owner": data.get("owner", ""),
        "location": data.get("location", ""),
        "area": data.get("area", ""),
        "survey_number": data.get("survey_number", ""),
        "reference": records[-1].hash[:12].upper(),
        "valid": blockchain.verify_chain()
    }

    return render_template("certificate.html", certificate=certificate)


@app.route("/blockchain")
def view_blockchain():
    return render_template(
        "blockchain.html",
        blockchain=blockchain,
        valid=blockchain.verify_chain()
    )


if __name__ == "__main__":
    app.run(debug=True)
