import wsgiref.handlers, urlparse, StringIO, logging, base64, zlib, os, sys
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors

class MainPage(webapp.RequestHandler):
    def myError(self, status, description, encodeResponse):
        # header
        self.response.out.write('HTTP/1.1 %d %s\r\n' % (status, description))
        self.response.out.write('Server: %s\r\n' % self.Software)
        self.response.out.write('Content-Type: text/html\r\n')
        self.response.out.write('\r\n')
        # body
        content = '<h1>Fetch Server Error</h1><p>Error Code: %d<p>Message: %s' % (status, description)
        if encodeResponse == 'base64':
            self.response.out.write(base64.b64encode(content))
        elif encodeResponse == 'compress':
            self.response.out.write(zlib.compress(content))
        else:
            self.response.out.write(content)

    def get(self):
        #origUrl = self.request.url
        # check path
        #(scm, netloc, path, params, query, _) = urlparse.urlparse(origUrl)
        #netloc = 'twitter.com'
        #newUrl = urlparse.urlunparse((scm, netloc, path, params, query, ''))
        #self.response.out.write(newUrl)
        self.response.out.write(data)

class LoginHandler(webapp.RequestHandler):
    def get(self):
        # Wrapping in a huge try/except isn't the best approach. This is just
        # an example for how you might do this.
        try:
          # Parse the header to extract a user/password combo.
          # We're expecting something like "Basic XZxgZRTpbjpvcGVuIHYlc4FkZQ=="
          auth_header = self.request.headers['Authorization']

          # Isolate the encoded user/passwd and decode it
          auth_parts = auth_header.split(' ')
          user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
          user_arg = user_pass_parts[0]
          pass_arg = user_pass_parts[1]

          self.response.out.write(user_arg + '++++++' + pass_arg)

        except Exception, e:

          # Here's how you set the headers requesting the browser to prompt
          # for a user/password:
          self.response.set_status(401, message="Authorization Required")
          self.response.headers['WWW-Authenticate'] = 'Basic realm="Secure Area"'

          # Rendering a 401 Error page is a good way to go...
          self.response.out.write('sigh')

class TwitterHandler(webapp.RequestHandler):
    def get(self):
        url = "http://twitter.com/statuses/followers.xml"
        login = 'test'
        password = 'test'
        base64string = base64.encodestring('%s:%s' % (login, password))[:-1]
        headers = {'Authorization': "Basic %s" % base64string} 
        #self.response.out.write(authString)
        data = urlfetch.fetch(url, headers=headers)
        self.response.out.write('Content-Type: text/html\r\n')
        self.response.out.write(data.content)




def main():
    application = webapp.WSGIApplication( [(r'/.*', TwitterHandler)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()