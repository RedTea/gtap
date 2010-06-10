# -*- coding: utf-8 -*-
# Copyright under  the latest Apache License 2.0

import wsgiref.handlers, urlparse, base64, logging
from cgi import parse_qsl
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors
from wsgiref.util import is_hop_by_hop

import oauth

gtap_vrsion = '0.4'

CONSUMER_KEY = 'xzR7LOq6Aeq8uAaGORJHGQ'
CONSUMER_SECRET = 'bCgaGEfejtE9mzq5pTMZngjnjd6rRL7hf2WBFjT4'

gtap_message = """
    <html>
        <head>
        <title>GAE Twitter API Proxy</title>
        <link href='https://appengine.google.com/favicon.ico' rel='shortcut icon' type='image/x-icon' />
        <style>body { padding: 20px 40px; font-family: Verdana, Helvetica, Sans-Serif; font-size: medium; }</style>
        </head>
        <body><h2>GTAP v#gtap_version# is running!</h2></p>
        <p><a href='/oauth/session'><img src='/static/sign-in-with-twitter.png' border='0'></a> <== Need Fuck GFW First!!</p>
        <p>This is a simple solution on Google Appengine which can proxy the HTTP request to twitter's official REST API url.</p>
        <p>Now You can:</p>
        <p><strong>1</strong> use <i>https://#app_url#/</i> instead of <i>https://twitter.com/</i> <br /></p>
        <p><strong>2</strong> use <i>https://#app_url#/api/</i> instead of <i>https://api.twitter.com/</i> <br /></p>
        <p><strong>3</strong> use <i>https://#app_url#/</i> instead of <i>https://search.twitter.com/</i> <br /></p>
        <p><font color='red'><b>Don't forget the \"/\" at the end of your api proxy address!!!.</b></font></p>
    </body></html>
    """

def my_output(handler, content_type, content):
    handler.response.status = '200 OK'
    handler.response.headers.add_header('GTAP-Version', gtap_vrsion)
    handler.response.headers.add_header('Content-Type', content_type)
    handler.response.out.write(content)

class MainPage(webapp.RequestHandler):


    def do_proxy(self, method):
        orig_url = self.request.url
        orig_body = self.request.body
        (scm, netloc, path, params, query, _) = urlparse.urlparse(orig_url)
        
        path_parts = path.split('/')
        
        if path_parts[1] == 'api' or path_parts[1] == 'search':
            sub_head = path_parts[1]
            path_parts = path_parts[2:]
            path_parts.insert(0,'')
            new_path = '/'.join(path_parts).replace('//','/')
            new_netloc = sub_head + '.twitter.com'
        else:
            new_path = path
            new_netloc = 'twitter.com'

        if new_path == '/' or new_path == '':
            global gtap_message
            gtap_message = gtap_message.replace('#app_url#', netloc)
            gtap_message = gtap_message.replace('#gtap_version#', gtap_vrsion)
            my_output(self, 'text/html', gtap_message )
        else:
            if 'Authorization' not in self.request.headers :
                headers = {}
            else:
                auth_header = self.request.headers['Authorization']
                auth_parts = auth_header.split(' ')
                user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
                username = user_pass_parts[0]
                password = user_pass_parts[1] # as access secret key

            new_url = urlparse.urlunparse(('https', new_netloc, new_path.replace('//','/'), params, query, ''))
            additional_params = dict([(k,v) for k,v in parse_qsl(orig_body)])
            
            logging.debug(new_url)
            
            #new_url = 'http://api.twitter.com/1/friends/ids.xml'
            
            callback_url = "%s/oauth/verify" % self.request.host_url
            client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, callback_url)

            try:
                user_access_token  = client.get_access_token_from_db(username)
            except Exception:
                self.response.set_status(503)
                self.response.out.write("Gtap Server Error:<br />")
                return self.response.out.write(format(errno, strerror))
            else:
                user_access_secret = password
                use_method = urlfetch.GET if method=='GET' else urlfetch.POST
                
                try :
                    data = client.make_request(url=new_url, token=user_access_token, secret=user_access_secret, 
                                           method=use_method, protected=True, 
                                           additional_params = additional_params)
                except Exception:
                    self.response.set_status(503)
                    self.response.out.write("Gtap Server Error:<br />")
                    return self.response.out.write(format(errno, strerror))
                else :
                    self.response.headers.add_header('GTAP-Version', gtap_vrsion)
                    for res_name, res_value in data.headers.items():
                        if is_hop_by_hop(res_name) is False and res_name!='status':
                            self.response.headers.add_header(res_name, res_value)
                    self.response.out.write(data.content)

    def post(self):
        self.do_proxy('POST')
    
    def get(self):
        self.do_proxy('GET')


class OauthPage(webapp.RequestHandler):
    def get(self, mode=""):
        callback_url = "%s/oauth/verify" % self.request.host_url
        client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, callback_url)
        
        if mode=='session':
            # step C Consumer Direct User to Service Provider
            #try:
                url = client.get_authorization_url()
                self.redirect(url)
            #except Exception,error_message:
            #    self.response.out.write( error_message )


        if mode=='verify':
            # step D Service Provider Directs User to Consumer
            auth_token = self.request.get("oauth_token")
            auth_verifier = self.request.get("oauth_verifier")
            logging.debug("oauth_token:" + auth_token)
            logging.debug("oauth_verifier:" + auth_verifier)
            # step E Consumer Request Access Token 
            # step F Service Provider Grants Access Token
            try:
                access_token, access_secret, screen_name = client.get_access_token(auth_token, auth_verifier)
            
                # Save the auth token and secret in our database.
                client.save_user_info_into_db(username=screen_name,token=access_token)
                
                self.response.out.write( 'Your access secret key is : %s' % access_secret )
            except Exception,error_message:
                self.response.out.write( error_message )


def main():
    application = webapp.WSGIApplication( [
        (r'/oauth/(.*)', OauthPage),
        (r'/.*',         MainPage)
        ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)
    
if __name__ == "__main__":
  main()
