#coding: utf-8
import BaseHTTPServer
import os
class ServerException(Exception):
    '''for internal error reporting  '''
    pass
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    ''' return file or error page '''
    Error_Page="""
     <html>
     <body>
     <h1> Error accessing{path}</h1>
     <p>{msg}</p>
     </body>
     </html>
     """

    def do_GET(self):

        try:

            full_path=os.getcwd()+self.path.replace("/","\\")
            if not os.path.exists(full_path):
                raise ServerException("{path} not found".format(self.path))
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            else:
                raise ServerException("Unknow object {0}".format(self.path))
        except Exception as msg:
            self.handle_error(msg)
    def handle_file(self,full_path):
        try:
            with open(full_path,'rb') as reader:
                content=reader.read()
                self.send_content(content)
        except IOError as msg:
            msg='{0} cannot be read {1}'.format(self.path,msg)
            self.handle_error(msg)
    def send_content(self,content):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header("Çontent-Length",str(len(content)))
        self.end_headers()
        self.wfile.write(content)
    def handle_error(self,msg):
        page=self.Error_Page.format(self.path,msg)
        self.send_content(page)
if __name__=='__main__':
        serverAddress=('',8000)
        server=BaseHTTPServer.HTTPServer(serverAddress,RequestHandler)
        server.serve_forever()
