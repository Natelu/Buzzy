from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, CGIHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
import sys


class MySimpleHttpRequest(SimpleHTTPRequestHandler):

    def guess_type(self, path):
        return 'application/vnd.dcos.universe.repo+json'



def test(HandlerClass=BaseHTTPRequestHandler,
         ServerClass=ThreadingHTTPServer,
         protocol="HTTP/1.0", port=8000, bind=""):
    """Test the HTTP request handler class.
    This runs an HTTP server on port 8000 (or the port argument).
    """
    server_address = (bind, port)

    HandlerClass.protocol_version = protocol
    with ServerClass(server_address, HandlerClass) as httpd:
        sa = httpd.socket.getsockname()
        serve_message = "Serving HTTP on {host} port {port} (http://{host}:{port}/) ..."
        print(serve_message.format(host=sa[0], port=sa[1]))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--cgi', action='store_true',
                       help='Run as CGI Server')
    parser.add_argument('--bind', '-b', default='', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory '
                        '[default:current directory]')
    parser.add_argument('port', action='store',
                        default=8000, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8000]')
    args = parser.parse_args()
    if args.cgi:
        handler_class = CGIHTTPRequestHandler
    else:
        handler_class = partial(MySimpleHttpRequest,
                                directory=args.directory)
    test(HandlerClass=handler_class, port=args.port, bind=args.bind)