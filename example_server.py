from server import HTTPServer
import mimetypes
from urllib.parse import urljoin
mimetypes.init()

class ExampleHTTPServer(HTTPServer):
    URL_REWRITE = {b'/': b'/index.html'}

    def generate_response(self, caddr, headers):
        if headers[b'URL'] == b'/favicon.ico':
            code = b'200 OK'
            headers = {b'Server': b'PyServer/0.1',
                       b'Content-Type': b'image/x-icon'}
            with open('favicon.ico', 'rb') as file:
                data = file.read()
        else:
            try:
                with open(urljoin(b'.', headers[b'URL'].lstrip(b'/')), 'rb') as file:
                    data = file.read()
                file_mime_type = mimetypes.guess_type(
                    headers[b'URL'].decode('utf-8'))[0].encode()
                code = b'200 OK'
                headers = {b'Server': b'PyServer/0.1',
                       b'Content-Type': file_mime_type}
            except FileNotFoundError:
                with open(b'404.html', 'rb') as file:
                    data = file.read()
                code = b'404 NOT FOUND'
                headers = {b'Server': b'PyServer/0.1',
                       b'Content-Type': b'text/html'}
            
        return code, headers, data

def main():
    server = ExampleHTTPServer('', 8080, timeout=10, listen=50000)
    server.serve()

if __name__ == '__main__':
#    import cProfile as profile
#    profile.run('main()', sort='tottime')
    main()
