# from flask import Flask
# 'Create a New Flask App Instance'
# app = Flask(__name__)
# 'Create Flask Routes'
# @app.route('/')
# def hello_world():
#     return 'Hello world '


# Set Up the Flask Weather App
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///../surfs_up/hawaii.sqlite")

# Reflect the database into our classes.
Base = automap_base()

# Reflect the database:
Base.prepare(engine, reflect=True)

#Create a variable for each of the classes
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session link from Python to our database .
session = Session(engine)

# Set Up Flask .
# Create a Flask application called "app."
app = Flask(__name__)

# Notice :the __name__ variable in this code. This is a special type of variable 
# in Python. Its value depends on where and how the code is run. 
# For example, if we wanted to import our app.py file into another Python 
# file named example.py, the variable __name__ would be set to example. 
# Here's an example of what that might look like:
# import app

# print("example __name__ = %s", __name__)

# if __name__ == "__main__":
#     print("example is being run directly.")
# else:
#     print("example is being imported")

# 9.5.2 . Create the Welcome Route.
# Define the welcome route .
@app.route("/")

# Create a function to add the routing information for each of the other routes .
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# When creating routes, we follow the naming convention /api/v1.0/ followed by the
# name of the route. This convention signifies that this is version 1 of our application. 
# This line can be updated to support future versions of the app as well.

flask run

# 9.5.3 .. Precipitation Route.
@app.route("/api/v1.0/precipitation")

# Create the precipitation() function.
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)
# # Notice the .\ in the first line of our query? This is used to signify that
# we want our query to continue on the next line. You can use the combination 
#  of .\ to shorten the length of your query line so that it extends to the next line.   

# 9.5.4 
# Stations Route
@app.route("/api/v1.0/stations")

# Create a new function called stations()
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# 9.5.5
# Monthly Temperature Route
@app.route("/api/v1.0/tobs")

#Create a function called temp_monthly()    
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
flask run    

# 9.5.6
# Statistics Route 