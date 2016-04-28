from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantMenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
		restaurants = session.query(Restaurant).all()
		try:
		if self.path.endswith("/restaurant"):
			    output = ""
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += " </br> <a href='/restaurant/new'> <h2> Make A New Restaurant </h2> </a>"
				for restaurant in restaurants:
				    output += restaurant.name
					output += "<a href ='/restaurants/%s/edit' >Edit </a> " % restaurant.id
					output += "</br>"
					output += " </br> <a href=\"#\"> Delete </a>"
				output += "</br></br></br>"
				output += "</body></html>"
				self.wfile.write(output)
		if self.path.endswith("/restaurant/new"):
			    output = ""
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output += "<html><body>"
				output += "<h1>Hello!</h1>"
				output += "</br> <h2> Make A New Restaurant Here.. </h2> </br>"
				output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/new'>"
				output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name' >"
				output += "<input type='submit' value='Create'> </form>"
				output += "</br></br></br>"
				output += "</body></html>"
				self.wfile.write(output)

		if self.path.endswith("/edit"):
			    restaurantIDPath = self.path.split("/")[2]
				myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
				if myRestaurantQuery:
			    	self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					output = "<html><body>"
					output += "<h1>"
					output += myRestaurantQuery.name
					output += "</h1>"
					output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
					output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
					output += "<input type = 'submit' value = 'Rename'>"
					output += "</form>"
					output += "</body></html>"
					self.wfile.write(output)	
		except IOError:
		    self.send_error(404, 'File Not Found: %s' % self.path)

def do_POST(self):
    try:
    	if self.path.endswith("/restaurant/new"):
		ctype, pdict = cgi.parse_header(self.headers.getheader('Content-type'))
		if ctype == 'multipart/form-data':
		    fields = cgi.parse_multipart(self.rfile, pdict)
			restaurantname = fields.get('newRestaurantName')
			restaurant = Restaurant(name = restaurantname[0])
			session.add(restaurant)
			session.commit()
			self.send_response(301)
			self.send_header('Location', '/restaurant')
			self.send_header('Content-type', 'text/html')
			self.end_headers()

if self.path.endswith("/edit"):
    ctype, pdict = cgi.parse_header(
        self.headers.getheader('Content-type'))
if ctype == 'multipart/form-data':
    fields = cgi.parse_multipart(self.rfile, pdict)
messagecontent = fields.get('newRestaurantName')
restaurantIDPath = self.path.split("/")[2]

myRestaurantQuery = session.query(Restaurant).filter_by(
    id = restaurantIDPath).one()
if myRestaurantQuery != []:
    myRestaurantQuery.name = messagecontent[0]
session.add(myRestaurantQuery)
session.commit()
self.send_response(301)
self.send_header('Content-type', 'text/html')
self.send_header('Location', '/restaurants')
self.end_headers()
except:
    pass

def main():
    try:
    server = HTTPServer(('', 8000), MyHandler)
print 'Web server running...open localhost:8000/restaurant in your browser'
server.serve_forever()
except KeyboardInterrupt:
    print '^C received, shutting down server'
server.socket.close()

if __name__ == '__main__':
    main()