#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Sign Up</h1>

"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

# this is the form
form = """
    <form method='post'>
    <table>
        <tr>
            <td>
                <label for="username">Username</label>
            </td>
            <td>
                <input name="username" type="text" value="%(username)s" />
                <span class="error">%(username_error)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label for="password">Password</label>
            </td>
            <td>
                <input name="password" type="password" />
                <span class="error">%(no_pass_error)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label for="verify">Verify Password</label>
            </td>
            <td>
                <input name="verify" type="password" />
                <span class="error">%(pass_match_error)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <label for="email">Email (optional)</label>
            </td>
            <td>
                <input name="email" type="text" value="%(email)s" />
                <span class="error">%(email_error)s</span>
            </td>
        </tr>
        <tr>
            <td>
                <input name='signup' id='signup' type='submit' value='Submit'/>
            </td>
        </tr>
    </table>
    </form>
"""

# validation
username_validation = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
email_validation = re.compile(r"^[\S]+@[\S]+.[\S]+$")
password_validation = re.compile(r"^.{3,20}$")

def validate_username(username):
    return username_validation.match(username)

def validate_email(email):
    return email_validation.match(email)

def validate_password(password):
    return password_validation.match(password)

class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
    """
    def write_form(self, username_error="", no_pass_error="", \
        pass_match_error="", email_error="", username="", email=""):
        self.response.out.write(form % {"username_error": username_error,
                                        "no_pass_error": no_pass_error,
                                        "pass_match_error": pass_match_error,
                                        "email_error": email_error,
                                        "username": username,
                                        "email": email})

    def get(self):
        self.response.out.write(page_header)
        self.write_form()
        self.response.out.write(page_footer)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        username_error = ""
        no_pass_error = ""
        pass_match_error = ""
        email_error = ""

        error = False

        if not validate_username(username):
            username_error = "Invalid Username"
            error = True

        if not validate_password(password):
            no_pass_error = "Invalid Password"
            error = True

        if password != verify:
            pass_match_error = "Passwords must match"
            error = True

        if email:
            if not validate_email(email):
                email_error = "Invalid Email"
                error = True

        if error:
            self.response.out.write(page_header)
            self.write_form(username_error, no_pass_error, pass_match_error, \
                email_error, username, email)
            self.response.out.write(page_footer)
        else:
            self.redirect("/welcome?name=" + username)

class Welcome(webapp2.RequestHandler):
    """ Handles requests coming in to '/welcome'
    """
    def get(self):
        username = self.request.get("name")
        self.response.out.write("<h1>Welcome, " + username + "!</h1>")


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
