import wsgiref.handlers, urlparse, StringIO, logging, base64, zlib, os, sys
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors

class MainPage(webapp.RequestHandler):
    serverName = 'GTAP / 0.2'

    def myOutput(self, contentType, content):
        self.response.status = '200 OK'
        self.response.headers.add_header('GTAP-Version', self.serverName)
        self.response.headers.add_header('Content-Type', contentType)
        self.response.out.write(content)

    def doProxy(self, method):
        origUrl = self.request.url
        origBody = self.request.body
        (scm, netloc, path, params, query, _) = urlparse.urlparse(origUrl)
        if path == '/' and method == 'get':
            self.myOutput('text/html', 'Thank you for using %s!' % (self.serverName))
        else:
            try:
                auth_header = self.request.headers['Authorization']
                auth_parts = auth_header.split(' ')
                user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
                user_arg = user_pass_parts[0]
                pass_arg = user_pass_parts[1]

                netloc = 'twitter.com'
                newUrl = urlparse.urlunparse((scm, netloc, path, params, query, ''))

                base64string = base64.encodestring('%s:%s' % (user_arg, pass_arg))[:-1]
                headers = {'Authorization': "Basic %s" % base64string}

                data = urlfetch.fetch(newUrl, payload=origBody, method=method, headers=headers)
                self.response.out.write(data.content)

            except Exception, e:
                self.response.set_status(401, message="Authorization Required")
                self.response.headers['WWW-Authenticate'] = 'Basic realm="Secure Area"'
                self.response.out.write("Requires Basec Authorization!!\r\n\r\n")

    def post(self):
        self.doProxy('post')
    
    def get(self):
        self.doProxy('get')

def main():
    application = webapp.WSGIApplication( [(r'/.*', MainPage)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()