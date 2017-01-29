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

# ISSUES:
# - Unexpected behavior on submission of username containing the hash symbol ('#')
#   This is because browsers read everything behind the hash as a URL fragment,
#   and escaping the text doesn't solve the problem.

import webapp2
import cgi
import re

class MainHandler(webapp2.RequestHandler):	
	def get(self):
		username_input = self.request.get("username_input")
		email_input = self.request.get("email_input")
		error_user = self.request.get("err_invalid_username")
		error_email = self.request.get("err_invalid_email")
		error_pass_invalid = self.request.get("err_pass_invalid")
		error_pass_mismatch = self.request.get("err_pass_mismatch")
		
		page_content = """
			<html>
				<head>
					<title>User Signup</title>
					<link rel="stylesheet" href="css/style.css" type="text/css" />
				</head>
				<body>
					<h1>Register a user account</h1>
					<p>(&#42; = required field)</p>
					<form method="post" action="/submit">
						<div class="form-field">
							<label for="user">Username&#42;</label>
							<input type="text" id="user" name="username" value="{0}" required />
							<span class="error-msg">{1}</span>
						</div>	
						<div class="form-field">
							<label for="mail">Email</label>
							<input type="email" id="mail" name="email" value="{2}" />
							<span class="error-msg">{3}</span>
						</div>
						<div class="form-field">
							<label for="pass">Password&#42;</label>
							<input type="password" id="pass" name="password" required />
							<span class="error-msg">{4}</span>
						</div>
						<div class="form-field">
							<label for="pass-confirm">Confirm Password&#42;</label>
							<input type="password" id="pass-confirm" name="password-confirm" required />
							<span class="error-msg">{5}</span>
						</div>
						<div class="form-field">
							<input type="submit" />
						</div>
					</form>
				</body>
			</html>
		""".format(username_input, error_user, email_input, error_email, error_pass_invalid, error_pass_mismatch)
		
		self.response.write(page_content)
		
class RegisterUser(webapp2.RequestHandler):
	def user_input_is_valid(self, data):
		# Initialize return values
		username_valid, email_valid, password_valid, passwords_match = (True, True, True, True)
		username_regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		email_regex = re.compile(r"^[\S]+@[\S]+.[\S]+$")
		password_regex = re.compile(r"^.{3,20}$")

		#Check if username is valid (between 3 and 20 characters, doesn't contain characters other than letters, digits, or underscores)
		if not username_regex.match(data["username"]):
			username_valid = False
		
		#Check if email is valid (is in correct format), but only if the user entered one
		if data["email"] != "":
			if not email_regex.match(data["email"]):
				email_valid = False
		
		# Check if the password is valid (between 3 and 20 characters)
		if not password_regex.match(data["password"]):
			password_valid = False
		
		# Check if passwords match
		if data["password"] != data["password-confirm"]:
			passwords_match = False
		
		return (username_valid, email_valid, password_valid, passwords_match)
	
	def post(self):
		user_data = {
			'username': cgi.escape(self.request.get("username")),
			'email': cgi.escape(self.request.get("email")),
			'password': cgi.escape(self.request.get("password")),
			'password-confirm': cgi.escape(self.request.get("password-confirm"))
		}
		
		page_content2 = """
			<html>
				<head>
					<title>User Signup</title>
					<link rel="stylesheet" href="css/style.css" type="text/css" />
				</head>
				<body>
					<p>Welcome, {0}! Your account has been registered successfully!</p>
				</body>
			</html>
		""".format(user_data["username"])
		
		user_valid, email_valid, pass_valid, pass_match = self.user_input_is_valid(user_data)
		username_input, mail_input = (user_data["username"], user_data["email"])
		err_invalid_username, err_invalid_email, err_pass_mismatch, err_pass_invalid = ("", "", "", "")
		
		if user_valid and email_valid and pass_valid and pass_match:
			self.response.write(page_content2)
		else:
			if user_valid == False:
				err_invalid_username = "Usernames must be between 3 and 20 characters long, and must only contain letters, numbers, or underscores"
			if email_valid == False:
				err_invalid_email = "The email address you entered is not valid."
			if pass_valid == False:
				err_pass_invalid = "A password must be between 3 and 20 characters long."
			if pass_match == False:
				err_pass_mismatch = "The passwords you entered do not match. Please try again."
		
			self.redirect('/?username_input=' + username_input + '&email_input=' + mail_input + '&err_invalid_username=' + err_invalid_username + '&err_invalid_email=' + err_invalid_email + '&err_pass_invalid=' + err_pass_invalid + '&err_pass_mismatch=' + err_pass_mismatch)

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/submit', RegisterUser)
], debug=True)
