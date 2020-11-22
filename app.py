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

# flask run

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
# flask run    

# 9.5.6
# Statistics Route 

# @app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create a function called stats() to put our code in.
# We need to add parameters to our stats()function: a start parameter and an end parameter.
# With the function declared, we can now create a query to select the minimum,
# average, and maximum temperatures from our SQLite database. 
# We'll start by just creating a list called sel, with the following code:
# We'll need to query our database using the list that we just made. Then, 
# we'll unravel the results into a one-dimensional array and convert them to a list. 
# Finally, we will jsonify our results and return them.
# NOTE In the following code, take note of the asterisk in the query next to the set list. 
# Here the asterisk is used to indicate there will be multiple results for our query: 
# minimum, average, and maximum temperatures.
# Now we need to calculate the temperature 
# minimum, average, and maximum with the start and end dates.
# We'll use the sel list, which is simply the data points we need to collect. 
# Let's create our next query, which will get our statistics data.

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Finally, we need to run our code. To do this, navigate to the "surfs_up" folder in the
# command line, and then enter the following command to run your code: flask run.

# This code tells us that we have not specified a start and end date for our range. 
# Fix this by entering any date in the dataset as a start and end date.
# For example, let's say we want to find the minimum, maximum, and average temperatures 
# for June 2017. You would add the following path to the address in your 
# web browser: /api/v1.0/temp/2017-06-01/2017-06-30.
# When you run the code, it should return the following result:["temps":[71.0,77.21989528795811,83.0]]