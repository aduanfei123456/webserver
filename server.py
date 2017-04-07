#coding: utf-8
import BaseHTTPServer
class ServerException(Exception):
    '''for internal error reporting  '''
    pass
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    Page='''<html>
<body>
<table>
<tr>  <td>Header</td>         <td>Value</td>          </tr>
<tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
<tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
<tr>  <td>Client port</td>    <td>{client_port}s</td> </tr>
<tr>  <td>Command</td>        <td>{command}</td>      </tr>
<tr>  <td>Path</td>           <td>{path}</td>         </tr>
</table>
</body>
</html>  '''
    def do_GET(self):
        page=self.create_page()
        self.send_page(page)
    def create_page(self):
        values={
            'date_time':self.date_time_string(),
            'client_host':self.client_address[0],
            'client_port':self.client_address[1],
            'command':self.command,
            'path':self.path
        }
        page=self.Page.format(**values)
        print(page)
        return page
    def send_page(self,page):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.send_header("Çontent-Length",str(len(page)))
        self.end_headers()
        self.wfile.write(page)
if __name__=='__main__':
        serverAddress=('',8000)
        server=BaseHTTPServer.HTTPServer(serverAddress,RequestHandler)
        server.serve_forever()
