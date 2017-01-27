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

class MainHandler(webapp2.RequestHandler):	
	def get(self):
		page_content = """
			<html>
				<head>
					<title>User Signup</title>
					<link rel="stylesheet" href="css/style.css" type="text/css" />
				</head>
				<body>
					<h1>Register a user account</h1>
					<p>(&#42; = required field)</p>
					<form method="post" action="/">
						<div class="form-field">
							<label for="user">Username&#42;</label>
							<input type="text" id="user" name="username" required />
						</div>	
						<div class="form-field">
							<label for="mail">Email</label>
							<input type="email" id="mail" name="email" />
						</div>
						<div class="form-field">
							<label for="pass">Password&#42;</label>
							<input type="password" id="pass" name="password" required />
						</div>
						<div class="form-field">
							<label for="pass-confirm">Confirm Password&#42;</label>
							<input type="password" id="pass-confirm" name="password" required />
						</div>
						<div class="form-field">
							<input type="submit" />
						</div>
					</form>
				</body>
			</html>
		"""
		
		self.response.write(page_content)
		
	def post(self):
		self.redirect('/')

app = webapp2.WSGIApplication([
	('/', MainHandler)
], debug=True)
