from flask_mysqldb import MySQL
from corona_archive import app
import unittest
import os
import sys
from urllib import response

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


# test function


class FlaskTestCase(unittest.TestCase):

    # checks if landing page is accessible
    def test_landing_page(self):
        tester = app.test_client()
        response = tester.get("/index", content_type="html/text")
        self.assertIn(b"Let's put an end to corona", response.data)

    # checks if visitor is able to register with correct data
    def test_visitor_registration_correct(self):
        tester = app.test_client()
        data = {
            "full_name": "John Smith",
            "visitor_email": "johnsmith@example.com",
            "address": "Campus Ring 4",
            "phone_number": "+49123456789",
        }
        response = tester.post("/register_visitor",
                               data=data, follow_redirects=True)
        self.assertIn(b"qr-reader", response.data)

    # checks if visitor is not able to register with incorrect data
    def test_visitor_registration_incorrect(self):
        tester = app.test_client()
        data = {
            "full_name": "John Smith",
            "visitor_email": "johnsmith@example.com",
        }
        response = tester.post("/register_visitor",
                               data=data, follow_redirects=True)
        self.assertIn(b"Bad Request", response.data)

    # checks if place registration is possible with correct data
    def test_place_registration_correct(self):
        tester = app.test_client()
        data = {"place_name": "JUB", "address": "Campus Ring 4"}
        response = tester.post(
            "/register_place", data=data, follow_redirects=True)
        self.assertIn(b"Download your QR code", response.data)

    # checks if place registration is not possible with incorrect data
    def test_place_registration_incorrect(self):
        tester = app.test_client()
        data = {
            "place_name": "JUB",
        }
        response = tester.post(
            "/register_place", data=data, follow_redirects=True)
        self.assertIn(b"Bad Request", response.data)

    # checks if hospital is able to log in with correct data
    def test_hospital_login_correct(self):
        tester = app.test_client()
        data = {"hospital_email": "legithospital@gmail.com",
                "password": "hello@12"}
        response = tester.post("/hospitals", data=data, follow_redirects=True)
        self.assertIn(b"Hospital's homepage.", response.data)

    # checks if hospital is not able to log in with incorrect credentials
    def test_hospital_login_incorrect(self):
        tester = app.test_client()
        data = {
            "hospital_email": "legithospital@gmail.com",
            "password": "wrong_password",
        }
        response = tester.post("/hospitals", data=data, follow_redirects=True)
        self.assertIn(b"Login failed. Please try again!", response.data)

    # tests if an agent is able to login with correct credentials
    def test_agent_login_correct(self):
        tester = app.test_client()
        data = {"agent_email": "agent@gmail.com", "password": "hello@12"}
        response = tester.post("/agents", data=data, follow_redirects=True)
        self.assertIn(b"Agent's homepage.", response.data)

    # checks if a user is able to login with incorrect credentials
    def test_agent_login_incorrect(self):
        tester = app.test_client()
        data = {"agent_email": "legithospital@gmail.com",
                "password": "wrong_password"}
        response = tester.post("/agents", data=data, follow_redirects=True)
        self.assertIn(b"Login failed. Please try again!", response.data)

    # tests agent's homepage accessibility
    def test_agent_home_page(self):
        tester = app.test_client()
        response = tester.get("/agent_home", content_type="html/text")
        self.assertIn(b"Agent's homepage.", response.data)

    # checks if logout works
    def test_log_out(self):
        tester = app.test_client()
        response = tester.get(
            "/logout", content_type="html/text", follow_redirects=True
        )
        self.assertIn(b"Register as a visitor", response.data)

    # checks if visitor check in is working with proper parameter
    def test_visitor_check_in(self):
        tester = app.test_client()
        data = dict(
            type="check-in",
            device_id="dfjslfjslfjsjf",
            qr_data="jdsljfksjkfdjsjf",
            login_form="",
        )
        response = tester.post(
            "/visitor_home", data=data, follow_redirects=True)
        self.assertIn(b"You have checked in successfully", response.data)

    # checks if visitor check in is not working with wrong parameter
    def test_visitor_check_in_error(self):
        tester = app.test_client()
        data = dict(
            type="check-in",
            qr_data="jdsljfksjkfdjsjf",
            login_form="",
        )
        response = tester.post(
            "/visitor_home", data=data, follow_redirects=True)
        self.assertIn(b"400 Bad Request", response.data)

    # checks if visitor check out is working with all parameter
    def test_visitor_check_out(self):
        tester = app.test_client()
        data = dict(
            type="check-out",
            qr_data="jdsljfksjkdffdfjsf",
            login_form="",
        )
        response = tester.post(
            "/visitor_home", data=data, follow_redirects=True)
        self.assertIn(b"qr-reader", response.data)

    # checks if visitor check out is not working with missing parameter
    def test_visitor_check_out_error(self):
        tester = app.test_client()
        data = dict(
            type="check-out",
            login_form="",
        )
        response = tester.post("/visitor_home", data=data)
        self.assertIn(b"400 Bad Request", response.data)

    def test_visitor_entry_type_error(self):
        tester = app.test_client()
        data = dict(
            type="******",
            qr_data="jdsljfksjkdffdfjsf",
            login_form="",
        )
        response = tester.post("/visitor_home", data=data)
        self.assertIn(
            b"An error Occured in mentioning entry type", response.data)

    # checks if post is not working with wrong check in type
    def test_visitor_entry_type_error(self):
        tester = app.test_client()
        data = dict(
            type="******",
            qr_data="jdsljfksjkdffdfjsf",
            login_form="",
        )
        response = tester.post("/visitor_home", data=data)
        self.assertIn(
            b"An error Occured in mentioning entry type", response.data)

    # checks if homepage of website is working or not
    def test_index_get(self):
        tester = app.test_client()
        response = tester.get("/")
        self.assertIn(b"Let's put an end to corona", response.data)

    # checks if register page of visitor is working
    def test_visitor_register_get(self):
        tester = app.test_client()
        response = tester.get("/register_visitor")
        self.assertIn(b"Create an account", response.data)

    # checks if register page of place is working
    def test_place_register_get(self):
        tester = app.test_client()
        response = tester.get("/register_place")
        self.assertIn(b"Register your place", response.data)

    # checks if login page of agent is working or not
    def test_agents_get(self):
        tester = app.test_client()
        response = tester.get("/agents")
        self.assertIn(b"Login as an agent", response.data)

    # checks if agent Homepage is working or not
    def test_agent_homepage_get(self):
        tester = app.test_client()
        response = tester.get("/agent_home")
        self.assertIn(b"Agent's homepage", response.data)

    # checks if hospital login page is working or not
    def test_hospitals_get(self):
        tester = app.test_client()
        response = tester.get("/hospitals")
        self.assertIn(b"Login as a hospital", response.data)

    # checks if Hospital homepage is working or not
    def test_hospital_homepage_get(self):
        tester = app.test_client()
        response = tester.get("/hospital_home")
        self.assertIn(b"Hospital's homepage", response.data)

    # checks if hospital registration request page is working or not
    def test_hospital_request_get(self):
        tester = app.test_client()
        response = tester.get("/hospital_request")
        self.assertIn(b"Hospital registration request", response.data)


if __name__ == "__main__":
    unittest.main()
