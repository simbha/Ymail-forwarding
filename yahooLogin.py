from mechanize import Browser
import mechanize

login_url = 'https://login.yahoo.com/config/login_verify2?&.src=ym&.intl=us'
br = Browser()
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

br.open(login_url)
br.select_form(nr=0)
br.form['login'] = 'mihai_mv13@yahoo.com'
br.form['passwd'] = '' ########
response = br.submit()
forms = mechanize.ParseResponse(response, backwards_compat=False)
form = forms[0]
for control in br.form.controls:
    print control
    print "type=%s, name=%s value=%s" % (control.type, control.name, br[control])

#print br.response().get_data()

