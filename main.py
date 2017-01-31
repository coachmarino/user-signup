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

#import webapp2

#class MainHandler(webapp2.RequestHandler):
#    def get(self):
#        self.response.write('Hello world!')

#app = webapp2.WSGIApplication([
#    ('/', MainHandler)
#], debug=True)


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

#def getCurrentWatchlist():
#    """ Returns the user's current watchlist """

    # for now, we are just pretending
    #return [ "Star Wars", "Minions", "Freaky Friday", "My Favorite Martian" ]


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
    """
    def get(self):

        # this is the user-signup
        complete_form = """
        <h1>
            Signup
        </h1>
        <br>
        <form action="/welcome" method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="">
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password">
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password">
                        <span class="error"></span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" type="email" value="">
                        <span class="error"></span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
        """

        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        #error_element = "<p class='error'>" + error + "</p>" if error else ""

        # combine all the pieces to build the content of our response
        main_content = complete_form + error
        content = page_header + main_content + page_footer
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


class CrossOffMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/cross-off'
        e.g. www.flicklist.com/cross-off
    """

    def post(self):
        # look inside the request to figure out what the user typed
        crossed_off_movie = self.request.get("crossed-off-movie")

        if (crossed_off_movie in getCurrentWatchlist()) == False:
            # the user tried to cross off a movie that isn't in their list,
            # so we redirect back to the front page and yell at them

            # make a helpful error message
            error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)
            error_escaped = cgi.escape(error, quote=True)

            # redirect to homepage, and include error as a query parameter in the URL
            self.redirect("/?error=" + error_escaped)

        # if we didn't redirect by now, then all is well
        crossed_off_movie_element = "<strike>" + crossed_off_movie + "</strike>"
        confirmation = crossed_off_movie_element + " has been crossed off your Watchlist."
        content = page_header + "<p>" + confirmation + "</p>" + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome),
    ('/cross-off', CrossOffMovie)
], debug=True)
