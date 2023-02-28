from http.server import HTTPServer,BaseHTTPRequestHandler
import yaml
import cgi
import os
import shutil

from nvflare.lighter import provision


class helloHandler(BaseHTTPRequestHandler):


    def do_GET(self):
        if self.path.endswith('/upload'):
            response = """
                    <html><body>
                    <h1></h1></br>
                    <h1>This is a demo application to build the NVFlare scripts and related files ( such as certificate... ) </h1>
                    <h2>Please upload the yaml configuration file for NVFlare: </h5></br>
                    <form method="POST" enctype="multipart/form-data" action="/BuildResult" >
                    <p>Yaml File: <input name="file" type="file" placeholder="Upload file"></p>
                    <p><input type="submit" value="Upload"></p>
                    </form>
                    </br>
                    <h10>Yaml Example:</h10></br>
                    <h10>_______________________________________________________________________________________________</h10></br>
                    <h10>api_version: 2</h10></br>
                    <h10>name: ExampleProject</h10></br>
                    <h10>description: NVIDIA FLARE sample project yaml file</h10></br>
                    <h10></h10></br>
                    <h10>participants:</h10></br>
                    
                    <h10>&nbsp;&nbsp;- name: example.com</h10></br>
                    <h10>&nbsp;&nbsp;&nbsp;&nbsp;type: server</h10></br>
                    <h10>&nbsp;&nbsp;&nbsp;&nbsp;org: nvidia</h10></br>
                    <h10>&nbsp;&nbsp;&nbsp;&nbsp;fed_learn_port: 8002</h10></br>
                    <h10>&nbsp;&nbsp;&nbsp;&nbsp;admin_port: 8003</h10></br>
                    <h10>&nbsp;&nbsp;&nbsp;&nbsp;# enable_byoc loads python codes in app.  Default is false.</h10></br>
                    <h10>&nbsp;&nbsp;&nbsp;&nbsp;enable_byoc: true</h10></br>
                    <h10>&nbsp;</h10></br>
                    <h10># The same methods in all builders are called in their order defined in builders section</h10></br>
                    <h10>builders:</h10></br>
                    <h10>&nbsp;&nbsp;- path: nvflare.lighter.impl.workspace.WorkspaceBuilder</h10></br>
                    <h10>&nbsp;&nbsp;&nbsp;&nbsp;args:</h10></br>
                    <h10>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;template_file: master_template.yml</h10></br>
                    <h10>_______________________________________________________________________________________________</h10></br>
                    </body></html>
                    """
            self.respond(response)

        else:
            SelfPath = str(self.path)
            FILEPATH = SelfPath.split('/')[-1]
            print('FILEPATH: ' + FILEPATH)

            if os.path.exists(FILEPATH):
                print(FILEPATH + " found, start downloading...")
                with open(FILEPATH, 'rb') as f:
                    print(' open file...')
                    self.send_response(200)
                    self.send_header("Content-Type", 'application/octet-stream')
                    self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(FILEPATH)))
                    fs = os.fstat(f.fileno())
                    self.send_header("Content-Length", str(fs.st_size))
                    self.end_headers()
                    print('End setting headers: ' + str(self.headers))
                    self.wfile.write(f.read())

            else:
                self.send_response(301)
                self.send_header('content-type', 'text/html')
                self.send_header('Location','/upload')
                self.end_headers()


    def do_POST(self):
        if self.path.endswith('/BuildResult'):
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            #print(form)
            filename = form['file'].filename
            data = form['file'].file.read()
            yamlProjectData = "project.yml"  # "Upload/" + filename
            FromFile = open(yamlProjectData, "wb")
            print('start uploading: ' + str(filename))
            FromFile.write(data)
            FromFile.close()
            print('file loaded')

            respondMessage = ""
            BuildSuccess = 0
            projectPath = ''
            projectName = ''
            try:
                provision.main()
                BuildSuccess = 1
                respondMessage = "Result Build successful.\n"

                project_data = yaml.safe_load(open('project.yml', 'r'))
                projectName = project_data.get("name")
                projectPath = "workspace\\" + projectName
                dir_list = os.listdir(projectPath)

                respondMessage = "Result Build successful.\n"
                respondMessage = respondMessage + "Generated result in " + projectPath + " as below:\n"
                for item in dir_list:
                    respondMessage = respondMessage + str(item) + '\n'

            except:
                BuildSuccess = 0
                respondMessage = "Something else went wrong, please upload again.\n"
                print(respondMessage)

            VulnList = '<html><body>\n'
            VulnList += '<h1> Generated items: </h1>\n'
            for line in respondMessage.splitlines():
                VulnList += '<h10>'+ line +'</h10>'
                VulnList += '</br>\n'

            if BuildSuccess == 1:
                dir_name = projectPath
                output_filename = projectName
                shutil.make_archive(output_filename, 'zip', dir_name)
                output_filename = projectName + ".zip"

                VulnList += '</br>\n'
                VulnList += '<h10><a href="/' + output_filename + '">' + "Download generated file: " + output_filename + '</a></h10>'
                VulnList += '</br>\n'

            VulnList += '</br>\n'
            VulnList += '<h10><a href="/upload"> Return to upload page. </a></h10>'
            VulnList += '</br>\n'

            VulnList += '</body></html>'

            self.headers['content-length']
            self.respond(VulnList)


    def respond(self, response, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(response))
        self.end_headers()
        self.wfile.write(response.encode())



def main():
    PORT = 8000
    server = HTTPServer(("0.0.0.0",PORT),helloHandler)
    print('server running on ' + str(server.server_address)[1:-1])
    server.serve_forever()

if __name__ == '__main__':
    main()