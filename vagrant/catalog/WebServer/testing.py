from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # Objective 3 Step 2 - Create /restarants/new page
            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurant/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></html></body>"
                self.wfile.write(output)
                return
            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h2>"
                    output += myRestaurantQuery.name
                    output += "</h2>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurant/%s/edit' >" % restaurantIDPath
                    output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h2>"
                    output += "Are you Sure you want to delete "
                    output += myRestaurantQuery.name
                    output += "</h2>"
                    output += "<form method='POST' enctype='multipart/form-data' action = '/restaurant/%s/delete' >" % restaurantIDPath
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)        

            if self.path.endswith("/restaurant"):
                restaurants = session.query(Restaurant).all()
                output = ""
                # Objective 3 Step 1 - Create a Link to create a new menu item
                output += "<a href = '/restaurant/new' > <h2>Make a New Restaurant Here </h2></a></br></br>"

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    # Objective 2 -- Add Edit and Delete Links
                    # Objective 4 -- Replace Edit href
                    output += "<a href ='/restaurants/%s/edit' >Edit </a> " % restaurant.id
                    output += "</br>"
                    output += "<a href ='/restaurant/%s/delete'> Delete </a> " % restaurant.id
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Objective 3 Step 3- Make POST method
    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurant')
                        self.end_headers()

            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    restaurantIDPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        session.delete(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurant')
                        self.end_headers()            

            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

        except:
            pass


def main():
    try:
        server = HTTPServer(('', 8000), webServerHandler)
        print 'Web server running...open localhost:8000/restaurant in your browser'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()


if __name__ == '__main__':
    main()