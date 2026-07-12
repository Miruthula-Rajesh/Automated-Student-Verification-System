from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

database.create_tables()
database.insert_sample_students()


@app.route("/")
def home():
    students = database.get_all_students()
    logs = database.get_logs()

    total = len(students)
    verified = len([s for s in students if s["status"] == "Verified"])
    pending = total - verified

    return render_template(
        "index.html",
        students=students,
        logs=logs,
        total=total,
        verified=verified,
        pending=pending,
    )


@app.route("/students")
def students():
    students = database.get_all_students()
    return render_template("students.html", students=students)


@app.route("/add", methods=["POST"])
def add():

    reg = request.form["reg_no"]
    name = request.form["name"]
    dept = request.form["department"]
    year = request.form["year"]
    email = request.form["email"]

    database.add_student(reg, name, dept, year, email)

    return redirect(url_for("students"))


@app.route("/delete/<reg>")
def delete(reg):

    database.delete_student(reg)

    return redirect(url_for("students"))


@app.route("/verify/<reg>")
def verify(reg):

    student = database.get_student(reg)

    if student:
        database.update_status(reg, "Verified")
        database.log_verification(reg, student["email"], "Verified")

    return redirect(url_for("home"))


@app.route("/logs")
def logs():

    log = database.get_logs()

    return render_template("logs.html", logs=log)


@app.route("/search", methods=["POST"])
def search():

    keyword = request.form["keyword"]

    students = database.search_student(keyword)

    return render_template("students.html", students=students)


if __name__ == "__main__":
    app.run(debug=True)