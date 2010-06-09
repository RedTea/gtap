# -*- coding: utf-8 -*-
# Copyright under  the latest Apache License 2.0

import wsgiref.handlers, urlparse, base64, logging
from cgi import parse_qsl
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors
from wsgiref.util import is_hop_by_hop

import oauth_util

gtap_vrsion = '0.4'

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

CONSUMER_KEY = 'xzR7LOq6Aeq8uAaGORJHGQ'
CONSUMER_SECRET = 'bCgaGEfejtE9mzq5pTMZngjnjd6rRL7hf2WBFjT4'

class MainPage(webapp.RequestHandler):
    def my_output(self, content_type, content):
        self.response.status = '200 OK'
        self.response.headers.add_header('GTAP-Version', gtap_vrsion)
        self.response.headers.add_header('Content-Type', content_type)
        self.response.out.write(content)

    def do_proxy(self, method):
        orig_url = self.request.url
        orig_body = self.request.body
        (scm, netloc, path, params, query, _) = urlparse.urlparse(orig_url)
        
        if 'Authorization' not in self.request.headers :
            headers = {}
        else:
            auth_header = self.request.headers['Authorization']
            auth_parts = auth_header.split(' ')
            user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
            username = user_pass_parts[0]
            password = user_pass_parts[1]
            base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
            headers = {'Authorization': "Basic %s" % base64string}

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

        logging.debug(new_path)

        if new_path == '/' or new_path == '':
            global gtap_message
            gtap_message = gtap_message.replace('#app_url#', netloc)
            gtap_message = gtap_message.replace('#gtap_version#', gtap_vrsion)
            self.my_output( 'text/html', gtap_message )
        else:
            new_url = urlparse.urlunparse(('https', new_netloc, new_path.replace('//','/'), params, '', ''))
            query_params = {}
            if query:
                query_params = dict([(k,v) for k,v in parse_qsl(query)])
            additional_params = dict([(k,v) for k,v in parse_qsl(orig_body)])
            query_params.update(additional_params)
            
            logging.debug(new_url)
            logging.debug(query_params)
            
            #new_url = 'http://api.twitter.com/1/friends/ids.xml'
            
            USER_TOKEN  = ''
            USER_SECRET = ''
            
            callback_url = "%s/oauth/verify" % self.request.host_url
            client = oauth_util.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, callback_url)
            
            #logging.debug(username)
            #logging.debug(password)
            
            use_method = urlfetch.GET if method=='GET' else urlfetch.POST
            
            #try :
            logging.debug(method)
            logging.debug(orig_body)
            
            data = client.make_request(url=new_url, token=USER_TOKEN, secret=USER_SECRET, 
                                       method=use_method, protected=True, 
                                       additional_params = query_params)

            
            logging.debug(data.headers)
            logging.debug(data.content)
            #except Exception:
            #    self.response.set_status(503)
            #    self.response.out.write("Gtap Server Error:<br />")
            #    return self.response.out.write(format(errno, strerror))

            
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
        client = oauth_util.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, callback_url)
        
        if mode=='session':
            # step C Consumer Direct User to Service Provider
            try:
                url = client.get_authorization_url()
                self.redirect(url)
            except Exception,error_message:
                self.response.out.write( error_message )


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
                self.response.out.write( access_token )
                self.response.out.write( "<br />" )
                self.response.out.write( access_secret )
                self.response.out.write( "<br />" )
                self.response.out.write( screen_name )
                
                user_info = client._lookup_user_info(access_token, access_secret)
                logging.debug(user_info)
                
                
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
