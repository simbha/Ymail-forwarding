from google.appengine.ext import ndb

class MailActivity(ndb.Model):
    id = ndb.UserProperty()
    y_mail = ndb.StringProperty(required=True)
    y_passwd = ndb.StringProperty(required=True)
    g_mail = ndb.StringProperty()
    send_spam = ndb.BooleanProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    def __refr__(self):
        return 'From %s to %s' %(self.y_mail, self.g_mail)

def mailActivityKey(user_id):
    return ndb.Key('ProfilePage', user_id)
