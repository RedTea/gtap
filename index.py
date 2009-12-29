import wsgiref.handlers, urlparse, base64
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors

gtapVersion = '0.2.2'

class MainPage(webapp.RequestHandler):
    def myOutput(self, contentType, content):
        self.response.status = '200 OK'
        self.response.headers.add_header('GTAP-Version', gtapVersion)
        self.response.headers.add_header('Content-Type', contentType)
        self.response.out.write(content)

    def doProxy(self, method):
        origUrl = self.request.url
        origBody = self.request.body
        (scm, netloc, path, params, query, _) = urlparse.urlparse(origUrl)
        if path == '/':
            self.myOutput('text/html', 'Thank you for using GTAP on version %s !' % (gtapVersion))
        else:
            if 'Authorization' not in self.request.headers :
                headers = {}
            else:
                auth_header = self.request.headers['Authorization']
                #auth_parts = auth_header.split(' ')
                #user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
                #user_arg = user_pass_parts[0]
                #pass_arg = user_pass_parts[1]
                #base64string = base64.encodestring('%s:%s' % (user_arg, pass_arg))[:-1]
                #headers = {'Authorization': "Basic %s" % base64string}
                headers = {'Authorization': "Basic %s" % auth_header}

            path_parts = path.split('/')
            if path_parts[1] == 'search':
                netloc = 'search.twitter.com'
                newpath = path[7:]
            elif path_parts[1] == 'api':
                netloc = 'api.twitter.com'
                newpath = path[4:]
            else:
                netloc = 'twitter.com'
                newpath = path

            newUrl = urlparse.urlunparse((scm, netloc, newpath, params, query, ''))
            
            data = urlfetch.fetch(newUrl, payload=origBody, method=method, headers=headers)
            self.response.status = data.status_code
            self.response.headers = data.headers
            self.response.out.write(data.content)


    def post(self):
        self.doProxy('post')
    
    def get(self):
        self.doProxy('get')

def main():
    application = webapp.WSGIApplication( [(r'/.*', MainPage)], debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
