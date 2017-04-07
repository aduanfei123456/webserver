#coding: utf-8
import BaseHTTPServer
import os
class ServerException(Exception):
    '''for internal error reporting  '''
    pass
class case_handler(object):
    def __init__(self):
        pass
    def act(self,handler):
        raise NotImplementedError()
    def test(self,handler):
        raise NotImplementedError()
    def __call__(self, handler, **kwargs):
        if self.test(handler):
            self.act(handler)
            return True
        return False
class case_no_file(case_handler):
    def test(self,handler):
        return not os.path.exists(handler.full_path)
    def act(self,handler):
        raise ServerException("{0} not found".format(handler.path))
class case_existing_file(case_handler):
    def test(self,handler):
        return  os.path.isfile(handler.full_path)
    def act(self,handler):
        handler.handle_file(handler.full_path)
class case_directory_index_file(case_handler):
    ''' serve index.html page for a directory'''
    def index_path(self,handler):
        return os.path.join(handler.full_path,'index.html')
    def test(self,handler):
        return os.path.isdir(handler.full_path) and \
        os.path.isfile(self.index_path(handler))
    def act(self,handler):
        handler.handle_file(self.index_path(handler))
class case_always_fail(case_handler):
    def test(self,handler):
        return True
    def act(self,handler):
        raise ServerException("Unknow object{0}".format(handler.path))
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    Cases=[case_no_file(),
             case_existing_file(),
             case_directory_index_file(),
             case_always_fail()]
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

            self.full_path=os.getcwd()+self.path.replace("/","\\")
            for case in self.Cases:
               if case(self):
                  return
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
        page=self.Error_Page.format(path=self.path,msg=msg)
        self.send_content(page)
if __name__=='__main__':
        serverAddress=('',8081)
        server=BaseHTTPServer.HTTPServer(serverAddress,RequestHandler)
        server.serve_forever()
