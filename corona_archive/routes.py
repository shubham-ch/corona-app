from pickle import FALSE, TRUE
from flask import render_template, url_for, redirect, flash, session, request, Response
from flask_login import login_user
from corona_archive import app, get_cursor, mysql
from corona_archive.helper import random_id, decode_qr_code, allowedFile
from corona_archive.forms import (
    AgentLoginForm,
    HospitalLoginForm,
    HospitalRequestForm,
    PlaceRegisterForm,
    QRCodeUploadForm,
    VisitorRegisterForm,
    AgentHospitalForm,
    HospitalInfectCitizen, VisitorRegisterForm
)
from uuid import uuid4
import datetime
from datetime import timedelta
import pip._vendor.requests as requests
import smtplib
from smtplib import SMTP

"""
The file is used for routing.
This file contains the functions which are run depending on the route called
"""

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
global COOKIE_TIME_OUT
COOKIE_TIME_OUT = 60*5


@app.route("/index")
@app.route("/")
def index():
    """
    Landing page for the website
    If there is an already logged in user, it redirects them to their own homepage.
    If no user is found, shows the landing page with links towards login and registration pages.
    """
    if "logged_in" in session and "user_type" in session and "id" in session:
        if session["user_type"] == "visitor":
            return redirect(url_for("visitorHome"))
        if session["user_type"] == "place":
            return redirect(url_for("placeHome"))
        if session["user_type"] == "hospital":
            return redirect(url_for("hospitalHome"))
        if session["user_type"] == "agent":
            return redirect(url_for("agentHome"))

    return render_template("index.html")


@app.route("/register_visitor", methods=["GET", "POST"])
def registerVisitor():
    """
    First time registration page for the visitor.
    Form data:
        full_name: Full name of the Visitor
        visitor_email: Email of the Visitor
        address: Address of the Visitor
        phone_number: Phone number of the Visitor
    Saves the Visitor to the database by generating a unique random id and redirects the new Visitor to their home page.
    If invalid data is provided sets the session variable to error and prompts the Visitor to retry.
    """

    if request.method == "POST":
        data = request.form
        full_name = data["full_name"]
        visitor_email = data["visitor_email"]
        address = data["address"]
        phone_number = data["phone_number"]
        device_id = str(uuid4())[:20]

        cursor = get_cursor()
        cursor.execute(
            "Select * from Visitor where email = %s", (visitor_email,)
        )
        data1 = cursor.fetchone()
        cursor.close()

        citizen_id = random_id()
        while True:
            cursor = get_cursor()
            cursor.execute(
                "SELECT * FROM Visitor WHERE citizen_id = %s", (citizen_id,))
            data = cursor.fetchone()
            if data == None:
                cursor.close()
                break
            citizen_id = random_id()

        if data1 == None:
            try:
                cursor = get_cursor()
                cursor.execute(
                    "INSERT INTO Visitor(citizen_id, visitor_name, address, phone_number, email, device_id, infected) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        citizen_id,
                        full_name,
                        address,
                        phone_number,
                        visitor_email,
                        device_id,
                        False,
                    ),
                )
                mysql.connection.commit()
                cursor.close()
                session["logged_in"] = True
                session["user_type"] = "visitor"
                session["id"] = citizen_id
                session["device_id"] = device_id
                return redirect(url_for("visitorHome"))
            except Exception as e:
                session["error"] = True
                return redirect(url_for("registerVisitor"))
        else:
            flash("Email already exists")

    else:
        form = VisitorRegisterForm()
        if "error" in session:
            session.pop("error")
            return render_template("visitor/register_visitor.html", form=form, error=True)
        return render_template("visitor/register_visitor.html", form=form)


@app.route("/register_place", methods=["GET", "POST"])
def registerPlace():
    """
    First time registration page for the place.
    Form data:
        place_name: Name of the Place
        address: Address of the Place
    Saves the place to the database by generating a unique random id and redirects the place owner to their home page
    If invalid data is provided sets the session variable to error and prompts the place owner to retry.
    """
    if request.method == "POST":
        data = request.form
        place_name = data["place_name"]
        address = data["address"]
        qr_code = str(uuid4())[:20]

        cursor = get_cursor()
        cursor.execute(
            "Select * from Places where place_name = %s", (place_name,)
        )
        data1 = cursor.fetchone()
        cursor.close()

        place_id = random_id()
        while True:
            cursor = get_cursor()
            cursor.execute(
                "SELECT * FROM Places WHERE place_id = %s", (place_id,))
            data = cursor.fetchone()
            if data == None:
                cursor.close()
                break
            place_id = random_id()
        if data1 == None:
            try:
                cursor = get_cursor()
                cursor.execute(
                    "INSERT INTO Places(place_id, place_name, address, QRcode) VALUES (%s, %s, %s, %s)",
                    (place_id, place_name, address, qr_code),
                )
                mysql.connection.commit()
                cursor.close()
                session["logged_in"] = True
                session["user_type"] = "place"
                session["id"] = place_id
                session["place_name"] = place_name
                session["qr_code"] = qr_code
                return redirect(url_for("placeHome"))
            except:
                session["error"] = True
                return redirect(url_for("registerPlace"))
        else:
            flash("Place already exists")

    else:
        form = PlaceRegisterForm()
        if "error" in session:
            session.pop("error")
            return render_template("place/register_place.html", form=form, error=True)
        return render_template("place/register_place.html", form=form)


@app.route("/hospitals", methods=["GET", "POST"])
def HospitalLogin():
    """
    Login page for the hospital.
    Form data:
        hospital_email: Email of the hospital serves as a username
        password: Password of the hospital
    If correct credentials are passed, redirects the hospital to the homepage.
    If the data provided is incorrect, shows error message and prompts hospital to retry.
    """
    if request.method == "POST":
        data = request.form
        hospital_email = data["hospital_email"]
        password = data["password"]
        # remember = data.getlist('inputRemember')

        cursor = get_cursor()
        cursor.execute(
            "SELECT hospital_id FROM Hospital WHERE username = %s AND password = %s",
            (hospital_email, password),
        )

        # login_user(remember=True)
        account = cursor.fetchone()
        if account:
            session["logged_in"] = True
            session["user_type"] = "hospital"
            session["id"] = account[0]
            return redirect(url_for("hospitalHome"))
        else:
            session["error"] = True
            return redirect(url_for("HospitalLogin"))

    form = HospitalLoginForm()
    # if 'hospital_email' in session:
    #     username = session['hospital_email']

    if "error" in session:
        session.pop("error")
        return render_template("hospital/hospital_login.html", form=form, error=True)
    return render_template("hospital/hospital_login.html", form=form)


@app.route("/hospital_request", methods=["GET", "POST"])
def HospitalRequest():
    """
    Hospital registration request page.
    The page where hospitals provide their email to be approved by the agent.
    """
    if request.method == "POST":
        data = request.form
        hospital_email = data["hospital_email"]
        print(hospital_email)
        cursor = get_cursor()

        cursor = get_cursor()
        cursor.execute(
            "Select * from Hospital where username = %s", (hospital_email,)
        )
        data1 = cursor.fetchone()
        cursor.close()
        if data1 == None:
            try:
                cursor = get_cursor()
                cursor.execute(
                    "INSERT INTO Hospital_Requests(username) VALUES(%s)", (
                        hospital_email,)
                )
                mysql.connection.commit()
                cursor.close()
                return redirect("/")
            except:
                flash("Something went wrong trying to commit your entry")
        else:
            flash("Hospita already exists")

    form = HospitalRequestForm()
    return render_template("hospital/hospital_request.html", form=form)


@app.route("/agents", methods=["GET", "POST"])
def AgentLogin():
    """
    Login page for the agent.
    Form data:
        agent_email: Email of the agent serves as a username
        password: Password of the agent
    If correct credentials are passed, redirects the agent to the homepage.
    If the data provided is incorrect, shows error message and prompts agent to retry.
    """
    if request.method == "POST":
        data = request.form
        agent_email = data["agent_email"]
        password = data["password"]

        cursor = get_cursor()
        cursor.execute(
            "SELECT agent_id FROM Agent WHERE username = %s AND password = %s",
            (agent_email, password),
        )
        account = cursor.fetchone()
        cursor.close()
        if account:
            print(account)
            session["logged_in"] = True
            session["user_type"] = "agent"
            session["id"] = account[0]
            return redirect(url_for("agentHome"))
        else:
            session["error"] = True
            return redirect(url_for("AgentLogin"))

    form = AgentLoginForm()
    if "error" in session:
        session.pop("error")
        return render_template("agent/agent_login.html", form=form, error=True)
    return render_template("agent/agent_login.html", form=form)


@app.route("/agent_home", methods=["POST", "GET"])
def agentHome():
    """
    Homepage of the agent.
    """

    if request.method == "POST":
        data = request.form

        hospital_email = data["hospital_email"]
        hospital_pswrd = data["hospital_pswrd"]
        # approve = data["approved"]
        # if approve == "FALSE":
        #     cursor = get_cursor()
        #     cursor.execute(
        #         "INSERT INTO Hospital (approved) VALUES (?)", (TRUE)
        #     )

        hospital_ID = random_id()
        while True:
            cursor = get_cursor()
            cursor.execute(
                "SELECT * FROM Hospital WHERE hospital_id = %s", (hospital_ID,)
            )
            data = cursor.fetchone()
            if data == None:

                break
            hospital_ID = random_id()
            cursor.close()

        cursor = get_cursor()
        cursor.execute(
            "Select * from Hospital where username = %s", (hospital_email,)
        )

        data1 = cursor.fetchone()
        cursor.close()
        if data1 == None:
            try:
                cursor = get_cursor()
                cursor.execute(
                    "INSERT INTO Hospital(hospital_id, username, password) VALUES (%s, %s, %s)",
                    (hospital_ID, hospital_email, hospital_pswrd),
                )
                mysql.connection.commit()
                cursor.close()
                redirect(url_for("agentHome"))
            except:
                flash("Something went wrong trying to commit your entry")
        else:
            flash("Username already exists!!")

    hospital_params = ["ID", "Email", "approved"]
    hospital_data = []
    try:
        cursor = get_cursor()
        cursor.execute("SELECT hospital_id, username, approved FROM Hospital")
        hospital_data = cursor.fetchall()
        cursor.close()
    except:
        flash("Could not fetch hospital data")

    form = AgentHospitalForm()
    return render_template(
        "agent/agent_home.html", form=form, params=hospital_params, datas=hospital_data
    )


@app.route("/approved/<int:id>")
def approved(id):

    identification = id
    # if 'agent' in session:
    cursor = get_cursor()
    cursor.execute(
        "UPDATE Hospital SET approved=1 WHERE hospital_id = '{t}'".format(
            t=identification)
    )
    mysql.connection.commit()
    cursor.close()

    hospital_params = ["ID", "Email", "approved"]
    hospital_data = []
    cursor1 = get_cursor()
    cursor1.execute("SELECT hospital_id, username, approved FROM Hospital")
    hospital_data = cursor1.fetchall()
    cursor1.close()

    form = AgentHospitalForm()

    return render_template(
        "agent/agent_home.html", form=form, datas=hospital_data, params=hospital_params
    )


@app.route("/not_infected/<int:id>")
def not_infected(id):
    not_infectedid = id
    cursor = get_cursor()
    cursor.execute(
        "UPDATE Visitor SET infected=1 WHERE citizen_id = '{t}'".format(
            t=not_infectedid)
    )
    mysql.connection.commit()
    cursor.close()

    form = HospitalLoginForm()
    citizen_params = ["ID", "Name", "email",
                      "phone", "address", "device_id", "infected"]
    citizen_data = []
    cursor1 = get_cursor()
    cursor1.execute("SELECT * FROM Visitor")
    citizen_data = cursor1.fetchall()
    cursor1.close()

    task_email = cursor.execute(
        "SELECT email FROM Visitor WHERE citizen_ID = {f}'".format(f=not_infectedid)).fetchone()
    msg = "You are marked as not infected!"
    server = smtplib.SMTP("smtp.googlemail.com", 587)
    server.starttls()
    server.login("coronoarchive@gmail.com", "sprint4se8")
    server.sendmail("coronoarchive@gmail.com", task_email, msg)

    return render_template("agent/hospital_home.html", form=form, datas=citizen_data, params=citizen_params)


@app.route("/hospital_home", methods=["GET", "POST"])
def hospitalHome():
    """
    Homepage of the hospital.
    Provides method to set citizens as infected and uninfected
    Shows list of citizens that are infected
    """

    if request.method == "POST":
        data = request.form
        citizen_ID = data["citizen_ID"]
        cursor = get_cursor()
        cursor.execute(
            "SELECT * FROM Visitor WHERE citizen_id = %s", (citizen_ID,))
        data = cursor.fetchone()
        cursor.close()
        if data == None:
            flash("No matching ID in database")
        else:
            try:
                cursor = get_cursor()
                cursor.execute(
                    "UPDATE Visitor SET infected = 1 WHERE citizen_id = %s",
                    (citizen_ID,),
                )
                mysql.connection.commit()
                cursor.close()
                redirect(url_for("hospitalHome"))
            except:
                flash("Something went wrong trying to commit your entry")

    form = HospitalInfectCitizen()
    citizen_params = ["ID", "Name", "email",
                      "phone", "address", "device_id", "infected"]
    citizen_data = []
    try:
        cursor = get_cursor()
        cursor.execute(
            "SELECT citizen_id, visitor_name, email, phone_number, address, device_id, infected FROM Visitor"
        )
        citizen_data = cursor.fetchall()
        cursor.close()
    except:
        flash("Could not fetch hospital data")
    return render_template(
        "hospital/hospital_home.html", form=form, params=citizen_params, datas=citizen_data
    )


@app.route("/visitor_home", methods=["GET", "POST"])
def visitorHome():
    """
    Homepage of the visitor.
    Contains Form for scanning QR code.
    This functionn receives post request from frontend which is used to
    store data in mysql database
    """

    if request.method == "POST":
        entry_type = request.form["type"]
        qr_code_data = request.form["qr_data"]

        if entry_type != "check-in" and entry_type != "check-out":
            return "An error Occured in mentioning entry type"

        if entry_type == "check-in":
            device_id = request.form["device_id"]
            if qr_code_data is None:
                session["error"] = True
                redirect(url_for("visitorHome"))
            session["checked-in"] = True
            session["place"] = qr_code_data
            session["check-in_time"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            entry_date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            try:
                # print("the device id is ==", device_id, "-------")
                cursor = get_cursor()
                cursor.execute(
                    "INSERT INTO Visitor_to_places(QRcode, device_id, entry_date, entry_time) Values (%s,%s, %s, %s)",
                    (
                        qr_code_data,
                        device_id,
                        entry_date_time[0:10],
                        entry_date_time[11:],
                    ),
                )
                mysql.connection.commit()
                # print(
                #     "insertion successful ================== with device id ",
                #     "==",
                #     device_id,
                #     "==",
                # )
            except Exception as error:
                print("=====An error occured while writing to mysql database======= ")
                print("Error :", error)
            # print("implement sql command here to store check-in detail\n", qr_code_data)

        if entry_type == "check-out":
            session["checked-in"] = False
            exit_date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            try:
                cursor = get_cursor()
                cursor.execute(
                    "UPDATE Visitor_to_places SET exit_date = %s,exit_time = %s WHERE QRcode = %s",
                    (
                        exit_date_time[0:10],
                        exit_date_time[11:],
                        qr_code_data,
                    ),
                )
                mysql.connection.commit()
                # print(
                #     "sql commit succesful with check-out============",
                #     qr_code_data,
                #     "=============",
                # )
            except Exception as error:
                print("=====An error occured whiile writing to mysql database======= ")
                print("Error :", error)
            # print("Checkout checkout sql sql sql sql sql sql sql")

    if "error" in session:
        session.pop("error")
        return render_template("visitor/visitor_home.html", error=True)

    if "checked-in" in session:
        if session["checked-in"]:
            # print("from checked_in in session")
            return render_template(
                "visitor_home.html",
                checked_in=True,
            )
        else:
            # print("from else of checked_in in session")
            return render_template(
                "visitor/visitor_home.html",
                checked_in=False,
            )

    return render_template("visitor/visitor_home.html")


@app.route("/place_home")
def placeHome():
    """
    Homepage of the place.
    Shows the QR code of the place.
    """
    place_id = session["qr_code"]
    qr_code = f"https://chart.googleapis.com/chart?cht=qr&chl={place_id}&chs=400x400&choe=UTF-8&chld=L|2"
    return render_template("place/place_home.html", qr_code=qr_code)


@app.route("/place_home/qr_code")
def download_qr_code():
    """
    QR download page
    Download route for the QR code of the logged in user.
    """
    place_id = session["qr_code"]
    qr_code = f"https://chart.googleapis.com/chart?cht=qr&chl={place_id}&chs=400x400&choe=UTF-8&chld=L|2"
    pic = requests.get(qr_code)
    return Response(pic, mimetype="image/png")


@app.route("/logout")
def logout():
    """
    Log out.
    Logs out any user and redirects them to the landing page.
    """
    session.clear()
    return redirect(url_for("index"))
