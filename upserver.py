from http.server import HTTPServer , CGIHTTPRequestHandler
import os
import cgi
import argparse

seperator = '/'
if os.name == 'nt':
    seperator = '\\'

blacklist = ['py','ipynb']

workingdir = None

upload_page = """
         <html>
         <body>
            <h3>File:</h3> 
            <form method="POST" action = "webserver.py" enctype="multipart/form-data">
                  <input type='file' name='filename'><br>
                  <input type='submit' name='upload'><br>
            </form>
         </body>
         </html>
    """

class requesthandler(CGIHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/list'):
            self.send_response(200)
            self.send_header("content-type",'text/html')
            self.end_headers()


            directory_listing ="""
             <html>
             <body>
                <h2>Index of </h3> 
        """ 
            data=[f"{round(os.stat(i).st_size/1024,2)}k : {i}" for i in os.listdir()]
            for i in data:
                directory_listing += i+"<br>"
            
            directory_listing += """
             </body>
             </html>
            """
            self.wfile.write(directory_listing.encode())

        elif self.path.endswith('/upload'):
            self.send_response(200)
            self.send_header("content-type",'text/html')
            self.end_headers()
            self.wfile.write(upload_page.encode())

        else:
            self.send_response(200)
            self.send_header("content-type",'text/html')
            self.end_headers()
            self.wfile.write("Don\'t Pwn me".encode()) 

    def deal_post_data(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'],})
        # print(form)
        fileitem = form['filename']
        # Test if the file was uploaded
        if fileitem.filename:
             # strip leading path from file name to avoid errors/ path traversal
            fn = os.path.basename(fileitem.filename)
            # print(fn)
            try:
                extension = fn.split('.')[1]
                if extension in blacklist:
                    print("Extension  is Blacklisted!!")
                    return False
            except IndexError:
                pass
            data =fileitem.file.read()
            # print(data)
            with open(workingdir+seperator+fn,'wb') as file:
                file.write(data)
                print(f"File uploded at {workingdir+seperator+fn} by POST from {self.client_address}")
            return True
        else:
            return False

    def do_POST(self):
        status = self.deal_post_data()
        self.send_response(200)
        self.send_header("content-type",'text/html')
        self.end_headers()
        if status:
            self.wfile.write('Success'.encode())
        else:
            self.wfile.write('Failed'.encode())


def main(PORT,dir):
    server = HTTPServer(('',PORT),requesthandler)
    print(f"Server Running on port {PORT}")
    print(f"Files will be saved at {dir}")
    server.serve_forever()


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description="A Simple http server to upload for temporary use")
    parser.add_argument('-p','--port',help="Port to use avoid using 80,443 for non root user",default=8080)
    parser.add_argument('-d','--directory',help="Working Directory", default=os.getcwd())
    args = parser.parse_args()
    workingdir = args.directory
    main(int(args.port),args.directory)


