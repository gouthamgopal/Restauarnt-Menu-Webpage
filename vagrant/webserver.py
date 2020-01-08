# from http.server import BaseHTTPRequestHandler, HTTPServer # For python3.
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

#Initial setup done for accessing database through python.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>Hello folks!</h1>"
                output += "<form method='POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?</h2>"
                output += "<input type='text' name='message' /><input type='submit' value='Submit' /> </form>"
                output += "</body></html>"

                self.wfile.write(output)
                print("Output", output)
                return
            
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>Hola</h1><a href='/hello'>Go back</a>"
                output += "<form method='POST' enctype = 'multipart/form-data' action = '/hello'><h2>What would you like me to say?</h2>"
                output += "<input type='text' name='message' /><input type='submit' value='Submit' /> </form>"
                output += "</body></html>"

                self.wfile.write(output)
                print("Output", output)
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<h1>List of restaurants</h1>"
                for restaurant in restaurants:
                    output += "<h3>"
                    output += restaurant.name
                    output += "</h3>"
                    output += "<a href='/restaurants/"+str(restaurant.id)+"/edit'>Edit</a><br /><a href='/restaurants/"+str(restaurant.id)+"/delete'>Delete</a>"

                output += "<h3>Want to add a new resataurant?</h3>"
                output += "<a href='/create'>Create new restaurant</a>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
            
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                idx = self.path.split('/')[2]

                restaurant = session.query(Restaurant).filter_by(id = idx).first()
                output = ""
                output += "<html><body>"
                output += "<h1>" + restaurant.name +  "</h1>"
                output += "<h3>What changes would you wish to make to this restaurant?</h3>"
                output += "<form method='POST' action='"+self.path+"' enctype='multipart/form-data'><h3>What name would you like to give the restaurant?</h3>"
                output += "<label for='name'><input id='name' type='text' name='name' /><input type='submit' value='Update' /> </form>"

                output += "</body></html>"

                self.wfile.write(output)
                print output
            
            if self.path.endswith("/create"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2>Enter the name of the restaurant that you want to add to the list!</h2>"
                output += "<form method='POST' action='/created' enctype='multipart/form-data'>"
                output += "<input type='text' name='name' /><input type='submit' value='Create' /> </form>"
                output += "</body></html>"
            
                self.wfile.write(output)
                print output
            
            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                idx = self.path.split('/')[2]

                resto = session.query(Restaurant).filter_by(id = idx).first()
                session.delete(resto)
                session.commit()

                output = ""
                output += "<html><body>"
                output += "<h2>Restaurant " + resto.name + " has been deleted!, Do you wish to go back to the restaurants list?</h2>"
                output += "<a href='/restaurants'>Go to Restaurants list</a>"
                output += "</body></html>"

                self.wfile.write(output)
                print "Deleted" + resto.name

        except IOError:
            self.send_error(404, "File node found in {self.path}")
    
    def do_POST(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                
                output = ""
                output += "<html></body>"
                output += "<div><h2>Okay, How about this?</h2>"
                output += "<p>" + messagecontent[0] + "</p></div>"

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2>"
                output += "<input type='text' name='message' /><input type='submit' value='Submit' /> </form>"

                output += "</body></html>"
                
                self.wfile.write(output)
                print( messagecontent[0])

            if self.path.endswith('/edit'):
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('name')
                
                idx = self.path.split('/')[2]
                restaurant = session.query(Restaurant).filter_by(id = idx).first()

                # Update by updating the attribute.
                restaurant.name = name[0]
                session.add(restaurant)
                session.commit()
                # Think of error handling here.

                output = ""
                output += "<html><body>"
                output += "<h2>Your changes have been updated</h2>"
                output += "<a href='/restaurants'>Do you wish to go back to restaurants secction?</a>"
                output += "</body></html>"

                self.wfile.write(output)
                print "Updated" + name
            
            if self.path.endswith("/created"):
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('name')
                
                resto = Restaurant(name = name[0])
                session.add(resto)
                session.commit()

                output = ""
                output += "<html><body>"
                output += "<h2>Your changes have been updated</h2>"
                output += "<a href='/restaurants'>Do you wish to go back to restaurants secction?</a>"
                output += "</body></html>"

                self.wfile.write(output)
                print "Created restaurant" + name

        except:
            print("POSt not working properly")

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Server running in port", port
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("^C was pressed, stopping server")
        server.socket.close()

if __name__ == "__main__":
    main()