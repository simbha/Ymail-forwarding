import webapp2, os, jinja2, urllib, sys, cgi
from google.appengine.api import users
sys.path.append('./models')
import models

JINJA_ENVIRONMENT = jinja2.Environment(
        loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions = ['jinja2.ext.autoescape'])

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            template_values = {
                    'nickname' : user.nickname(),
                    'logout_url' : users.create_logout_url('/'),
                    'login_url' : users.create_login_url(self.request.uri),
                    }
        else:
            template_values = {
                    'nickname' : 'guest',
                    'login_url' : users.create_login_url(self.request.uri),
                    }
        template = JINJA_ENVIRONMENT.get_template('templates/index.html')
        self.response.write(template.render(template_values))

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            mail_query = models.MailActivity.query( ancestor = 
                    models.mailActivityKey(user.user_id())).fetch()
            subscribtions = []
            for entry in mail_query:
                dict = {}
                dict['from'] = entry.y_mail;
                dict['to'] = entry.g_mail;
                if entry.send_spam:
                    dict['spam'] = 'Yes'
                else:
                    dict['spam'] = 'No'
                subscribtions.append(dict)

            template_values = { 'nickname' : user.nickname(),
                    'logout_url' : users.create_logout_url('/'),
                    'subscribtions' : subscribtions
                    }
            template = JINJA_ENVIRONMENT.get_template('templates/profile.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/guest')

    def post(self):
        mail_activity = models.MailActivity(parent = 
                models.mailActivityKey(users.get_current_user().user_id()))
        mail_activity.id = users.get_current_user()
        mail_activity.y_mail = str(cgi.escape(self.request.get('y_mail')))
        mail_activity.y_passwd = str(cgi.escape(self.request.get('y_passwd')))
        mail_activity.g_mail = str(cgi.escape(self.request.get('g_mail')))
        mail_activity.send_spam = ('on' == str(cgi.escape(self.request.get('send_spam'))))
        mail_activity.put()
        self.get()

class CheckDB(webapp2.RequestHandler):
    def get(self):
        #user1 = models.MailActivity(id="test1")
        #user2 = models.MailActivity(id="test2")
        #user1.put()
        #user2.put()
        mail_query = models.MailActivity.query(models.MailActivity.id=='test3')
        self.response.write('<html>')
        for entry in mail_query:
            #resp = 'from ' + entry.y_mail + ' to ' + entry.g_mail
            resp = 'id ' + entry.id + ' date: ' + str(entry.date)
            entry.key.delete()
            self.response.write('<div> %s </div>'% (resp))
        self.response.write('</html>')

class Guest(webapp2.RequestHandler):
    def get(self):
        template_values = {'login_url' : users.create_login_url(self.request.uri)}
        template = JINJA_ENVIRONMENT.get_template('templates/guest.html')
        self.response.write(template.render(template_values))

class Unsubscribe(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            mail_query = models.MailActivity.query( ancestor = 
                    models.mailActivityKey(user.user_id())).fetch()
            subscribtions = []
            for entry in mail_query:
                dict = {}
                dict['from'] = entry.y_mail;
                dict['to'] = entry.g_mail;
                if entry.send_spam:
                    dict['spam'] = 'Yes'
                else:
                    dict['spam'] = 'No'
                subscribtions.append(dict)

            if subscribtions == []:
                self.redirect('/profile')

            template_values = { 'nickname' : user.nickname(),
                    'logout_url' : users.create_logout_url('/'),
                    'subscribtions' : subscribtions
                    }
            template = JINJA_ENVIRONMENT.get_template('templates/unsubscribe.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/guest')

    def post(self):
        y_mail = str(cgi.escape(self.request.get('y_mail')))
        g_mail = str(cgi.escape(self.request.get('g_mail')))
        user = users.get_current_user()
        if user:
            mail_query = models.MailActivity.query( 
                    models.MailActivity.y_mail == y_mail,
                    models.MailActivity.g_mail == g_mail,
                    ancestor = models.mailActivityKey(user.user_id()))
            subscrib = mail_query.get()
            if subscrib:
                subscrib.key.delete()
        self.get()

                



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/profile', ProfilePage),
    ('/db', CheckDB),
    ('/guest', Guest),
    ('/unsubscribe', Unsubscribe),
    ], debug = True)

