# Copyright (C) 2011 Google Inc.
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


from flask import Flask
webapp = Flask(__name__)

@webapp.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    webapp.debug = True
    webapp.run()




# import webapp2
# import os
# from webapp2_extras import jinja2

# from apiclient.discovery import build
# from oauth2client.appengine import OAuth2DecoratorFromClientSecrets

# JINJA_ENVIRONMENT = jinja2.Environment(
#     loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
#     extensions=['jinja2.ext.autoescape'],
#     autoescape=True)

# decorator = OAuth2DecoratorFromClientSecrets(
#     os.path.join(os.path.dirname(__file__), 'client_secrets.json'),
#     scope='https://www.googleapis.com/auth/plus')

# service = build('tasks', 'v1')


# class MainHandler(webapp2.RequestHandler):

#   def render_response(self, template, **context):
#     renderer = jinja2.get_jinja2(app=self.app)
#     rendered_value = renderer.render_template(template, **context)
#     self.response.write(rendered_value)

#   @decorator.oauth_aware
#   def get(self):
#     if decorator.has_credentials():
#       result = service.tasks().list(tasklist='@default').execute(
#           http=decorator.http())
#       tasks = result.get('items', [])
#       for task in tasks:
#         task['title_short'] = truncate(task['title'], 26)
#       self.render_response('index.html', tasks=tasks)
#     else:
#       url = decorator.authorize_url()
#       self.render_response('index.html', tasks=[], authorize_url=url)


# def truncate(s, l):
#   return s[:l] + '...' if len(s) > l else s


# application = webapp2.WSGIApplication([
#     ('/', MainHandler),
#     (decorator.callback_path, decorator.callback_handler()),
#     ], debug=True)