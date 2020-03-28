from xmlrpc.server import SimpleXMLRPCServer

def add(x,y):
	return x+y
def subtract(x,y):
	return x-y	
def multiply(x,y):
	return x*y	
def divide(x,y):
	return x//y	

port = 8000
server = SimpleXMLRPCServer(("localhost",port))
print(f"listening at {port} port")

server.register_function(add , "add")
server.register_function(subtract , "subtract")
server.register_function(multiply , "multiply")
server.register_function(divide , "divide")

server.serve_forever()
