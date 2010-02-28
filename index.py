import wsgiref.handlers, urlparse, base64
from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors

gtapVersion = '0.3'

_hoppish = {
    'connection':1,
    'keep-alive':1,
    'proxy-authenticate':1,
    'proxy-authorization':1,
    'te':1,
    'trailers':1,
    'transfer-encoding':1,
    'upgrade':1,
    'proxy-connection':1
}

def is_hop_by_hop(header):
    #check if the given header is hop_by_hop
    return _hoppish.has_key(header.lower())

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
            self.myOutput('text/html', 'here is the proxy of \"twitter.com\" by GTAP %s !' % (gtapVersion))
        else:
            if 'Authorization' not in self.request.headers :
                headers = {}
            else:
                auth_header = self.request.headers['Authorization']
                auth_parts = auth_header.split(' ')
                user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
                user_arg = user_pass_parts[0]
                pass_arg = user_pass_parts[1]
                base64string = base64.encodestring('%s:%s' % (user_arg, pass_arg))[:-1]
                headers = {'Authorization': "Basic %s" % base64string}

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

            if newpath == '/' or newpath == '':
                self.myOutput('text/html', 'here is the proxy of \"'+ netloc + '\" by GTAP %s !' % (gtapVersion))
            else:
                newUrl = urlparse.urlunparse((scm, netloc, newpath, params, query, ''))
                
                data = urlfetch.fetch(newUrl, payload=origBody, method=method, headers=headers)
                self.response.set_status(data.status_code)
                self.response.headers.add_header('GTAP-Version', gtapVersion)
                for resName, resValue in data.headers.items():
                    if is_hop_by_hop(resName) is False and resName!='status':
                        self.response.headers.add_header(resName, resValue)
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
