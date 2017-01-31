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

import webapp2
import cgi
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

"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

username_validation = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
email_validation = re.compile(r"^[\S]+@[\S]+.[\S]+$")
password_validation = re.compile(r"^.{3,20}$")

username_form = """
<div class="row">
<label for='user_name'>User Name:&nbsp;</label>
<input name='user_name' id='user_name' value=""/>
<span class="noerr">Not a valid user name</span>
</div>
"""

password_form = """
<br>
<div class="row">
<label for='password'>Password:&nbsp;</label>
<input name='password' id='password' type="password" value=""/>
<span class="noerr">Not a valid user password</span>
</div>
"""

v_password_form = """
<br>
<div class="row">
<label for='verify_pw'>Verify:&nbsp;</label>
<input name='verify_pw' id='verify_pw' type="password" value=""/>
<span class="noerr">Passwords don't match.</span>
</div>
"""

email_form = """
<br>
<div class="row">
<label for='email'>Email (Optonal):&nbsp;</label>
<input name='email' id='email' value=""/>
<span class="noerr">Not a valid user email</span>
</div>
"""

def validate_username(username):
    return username_validation.match(user)


def validate_password(password):
    return password_validation.match(pw)


def validate_email(email):
    if email:
        return email_validation.match(email)
    return True

class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
    """
    def get(self):

        # this is the user-signup
        content = page_header + "<h1>Sign Up</h1><div class='err_container'> \
            <form action='/welcome' method='post'>" + username_form \
            + password_form + v_password_form + email_form + \
            "<input type='submit'></form></div>" + page_footer

        #form_header = """
        #    <h1>
        #        Signup
        #    </h1>
        #    """
        #form_open_tags = """
        #<form action="/welcome" method="post">
        #    <table>
        #    """
        #form_content = username_form + password_form + v_password_form + email_form

        #form_close_tags = """
        #    </table>
        #    <input type="submit">
        #</form>
        #"""

        #content = page_header + form_header + form_open_tags +
        #    form_content + form_close_tags + page_footer
        self.response.write(content)


class Welcome(webapp2.RequestHandler):
    """ Handles requests coming in to '/welcome'
    """

    def post(self):
        # look inside the request to figure out what the user typed
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        # if the username is blank, error

        if username == "":

            error = "That's not a valid username"
            #error_escaped = cgi.escape(error, quote=True)

        # redirect to homepage, and include error as a query parameter in the URL
            #self.redirect("/?error=" + error_escaped)
            self.redirect("/?error=" + "<span class='error'>" + error + "</span>")

        # if the password is blank, error

        if password == "":

            pass_error = "That's not a valid password"
            #error_escaped = cgi.escape(error, quote=True)

        # redirect to homepage, and include error as a query parameter in the URL
            #self.redirect("/?error=" + error_escaped)
            self.redirect("/?error=" + "<span class='error'>" + pass_error + "</span>")



        # TODO 3
        # if the user wants to add a terrible movie, redirect and yell at them
        #if new_movie in terrible_movies:
        #    error = "That's awful, try again!"
        #    error_escaped = cgi.escape(error, quote=True)
        #    self.redirect("/?error=" + error_escaped)


        # TODO 1
        # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
        username = cgi.escape(username)
        password = cgi.escape(password)
        verify = cgi.escape(verify)
        email = cgi.escape(email)


        # build response content
        welcome_sentence = "<h1>Welcome, " + username + "!</h1>"
        content = page_header + "<p>" + welcome_sentence + "</p>" + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)

], debug=True)
