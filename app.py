from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)
app.secret_key = "development-key"


def valid_email(email):
    return email.lower().endswith("@charlotte.edu")


def valid_password(password):
    return (
        len(password) >= 8
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"[0-9]", password)
        and re.search(r"[^A-Za-z0-9]", password)
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login/<role>", methods=["GET", "POST"])
def login(role):

    if role not in ["student", "faculty"]:
        return "Invalid role", 404

    error = None

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not valid_email(email):
            error = "Email must end with @charlotte.edu."

        elif not valid_password(password):
            error = (
                "Password must contain at least 8 characters, "
                "one uppercase letter, one lowercase letter, "
                "one number, and one special character."
            )

        else:
            session["email"] = email
            session["role"] = role

            if role == "student":
                return redirect(url_for("student_dashboard"))

            return redirect(url_for("faculty_dashboard"))

    return render_template(
        "login.html",
        role=role,
        error=error
    )


@app.route("/student/dashboard")
def student_dashboard():

    if session.get("role") != "student":
        return redirect(url_for("home"))

    return render_template(
        "student_dashboard.html",
        email=session.get("email")
    )


@app.route("/faculty/dashboard")
def faculty_dashboard():

    if session.get("role") != "faculty":
        return redirect(url_for("home"))

    return render_template(
        "faculty_dashboard.html",
        email=session.get("email")
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)