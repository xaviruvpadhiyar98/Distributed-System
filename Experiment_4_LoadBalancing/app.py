#install flask first 
#pip3 install --user flask
#to run use ---- make three instance 
#python3 app.py 5000
#python3 app.py 5001
#python3 app.py 5002
#go to  browser with localhost:5000/hello , localhost:5001/hello ,localhost:5002/hello
#Finally go to localhost/hello and refresh


from flask import Flask
from sys import argv
import os
app = Flask(__name__)

@app.route('/hello')
def ping():
    return (f"Served From {os.getpid()}",200)

if __name__ =='__main__':
    app.run('0.0.0.0' ,port=argv[1], debug = True)
    
