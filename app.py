from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3307,
    user="root",
    password="",
    database="social_welfare"
)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/beneficiaries")
def beneficiaries():
    search = request.args.get("search", "")

    cursor = db.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM beneficiaries WHERE name LIKE %s",
            ("%" + search + "%",)
        )
    else:
        cursor.execute("SELECT * FROM beneficiaries")

    data = cursor.fetchall()
    cursor.close()

    return render_template("beneficiaries.html", beneficiaries=data)

@app.route("/delete_beneficiary/<int:id>")
def delete_beneficiary(id):
    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM beneficiaries WHERE id = %s",
        (id,)
    )

    db.commit()
    cursor.close()

    return redirect("/beneficiaries")

 
@app.route("/schemes")
def schemes():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM schemes")
    data = cursor.fetchall()
    cursor.close()

    return render_template("schemes.html", schemes=data)

@app.route("/applications")
def applications():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM applications")
    data = cursor.fetchall()
    cursor.close()

    return render_template("applications.html", applications=data)

@app.route("/dashboard")
def dashboard():
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM beneficiaries")
    beneficiaries_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM schemes")
    schemes_count = cursor.fetchone()[0]

    registrations_count = beneficiaries_count

    cursor.close()

    return render_template(
        "dashboard.html",
        beneficiaries_count=beneficiaries_count,
        schemes_count=schemes_count,
        registrations_count=registrations_count
    )

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    recommendation = None

    if request.method == "POST":
        age = int(request.form["age"])
        gender = request.form["gender"]

        income_text = request.form.get("income", "").strip()

        if income_text:
            income = int(income_text)
        else:
            income = None

        if age >= 60:
            recommendation = "Senior Citizen Scheme"

        elif income is not None and income < 100000:
            recommendation = "Low Income Welfare Scheme"

        elif gender == "Female":
            recommendation = "Women Welfare Scheme"

        else:
            recommendation = "Family Welfare Scheme"

    return render_template(
        "recommend.html",
        recommendation=recommendation
    )


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        phone = request.form.get("phone")
        address = request.form.get("address")
        scheme = request.form.get("scheme")

        cursor = db.cursor()

        sql = """
        INSERT INTO beneficiaries
        (name, age, gender, phone, address, scheme)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (name, age, gender, phone, address, scheme)

        cursor.execute(sql, values)
        db.commit()

        cursor.close()

        return redirect("/beneficiaries")

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)