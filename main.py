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
import cgi

class MainHandler(webapp2.RequestHandler):	
	def get(self):
		error_user = ""
		error_email = ""
		error_pass = ""
		error_pass_confirm = ""
		
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
							<input type="text" id="user" name="username" required />
							<p class="error-msg">{0}</p>
						</div>	
						<div class="form-field">
							<label for="mail">Email</label>
							<input type="email" id="mail" name="email" />
							<p class="error-msg">{1}</p>
						</div>
						<div class="form-field">
							<label for="pass">Password&#42;</label>
							<input type="password" id="pass" name="password" required />
							<p class="error-msg">{2}</p>
						</div>
						<div class="form-field">
							<label for="pass-confirm">Confirm Password&#42;</label>
							<input type="password" id="pass-confirm" name="password-confirm" required />
							<p class="error-msg">{3}</p>
						</div>
						<div class="form-field">
							<input type="submit" />
						</div>
					</form>
				</body>
			</html>
		""".format(error_user, error_email, error_pass, error_pass_confirm)
		
		self.response.write(page_content)
		
class RegisterUser(webapp2.RequestHandler):
	def user_input_is_valid(self, data):
		# TODO: check username for invalid characters (e.g.: @, &, whitespace, tab)
		if data["password"] != data["password-confirm"]:
			return False
		
		return True
	
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
		
		if self.user_input_is_valid(user_data):
			self.response.write(page_content2)
		else:
			# TODO: check for specific errors and display the appropriate messages on the home page
			self.redirect('/')

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/submit', RegisterUser)
], debug=True)
