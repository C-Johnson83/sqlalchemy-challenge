
# Import dependancies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

# Create database connection
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect the existing tables into classes
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to my climate station API!<br/>"
        f'<br/>'
        f"The Available Routes:<br/>"
        f'<br/>'
        f"/api/v1.0/precipitation<br/>"        
        f"/api/v1.0/stations<br/>"       
        f"/api/v1.0/tobs<br/>"
        f'<br/>'
        f'<br/>'
        f'The Dynamic Routes<br/>'
        f'Search by single date<br/>'
        f"/api/v1.0/<start><br/>"
        f'Please enter search dates as y-m-d format (2012-05-28)<br/>'
        f'<br/>'
        f'Search by start and end dates<br/>'
        f"/api/v1.0/<start>/<br/>"
        f'Please enter search dates as y-m-d format with the forward slash between them (2012-05-28/2015-05-28)<end>'
       
        
        
    )

# Set precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a dictionary of precipitation measurements"""
    # Query all precipitation and filter for the last year
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >=  (dt.date(2017,8,23)- dt.timedelta(days=365))).\
    order_by(measurement.date).all()

    # close session
    session.close()

    # Make an empty list to store the appended dictionary results of the row data with 
    # Date as the key and the measurement as the value. Return the list as a json file
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
     
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

# Set station route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the stations"""
    # Query all stations
    results = session.query(station.station).all()
    # close session
    session.close()
    # Convert list of tuples into normal list and return as a json file
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


# Set tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates and the tobs for the most active station"""
    # Query the active station tobs for the past year
    results = session.query(measurement.date,measurement.tobs).filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= (dt.date(2017,8,23)- dt.timedelta(days=365))).\
        order_by(measurement.date).all()
    
    # close session
    session.close()
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)
  
# Return a json list of the minimum temperature, the average temperature,
# and the maximum temperature for a specified start or start-end range.
# 
# For a specified start, 
# calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
@app.route("/api/v1.0/<start>")
def start_tob(start):

      # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of temperature observations (TOBS) from the provided start date to the most r ecent data point."""
    # Query the tobs for all the dates greater than or equal to the start date and calculate TMIN, TAVG, and TMAX for the range
    results = (session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), \
              func.avg(measurement.tobs)).filter((measurement.date) >= start).group_by(measurement.date).all())
    
    # close session
    session.close()

    # Make an empty list to store the tobs of the appended rows date 
    # Make a dictionary for the TMIN, TAVG, and TMAX of each date and append to the empty list. Return the list as a json file
    start_tobs = []
    for date, min,max,avg in results:
        start_tob_dict = {}
        start_tob_dict["date"] = date
        start_tob_dict["min_tobs"] = min
        start_tob_dict["max_tobs"] = max
        start_tob_dict["avg_tobs"] = avg
        start_tobs.append(start_tob_dict)
 
    return jsonify(start_tobs)    

   
# For a specified start date and end date, 
# calculate TMIN, TAVG, and TMAX for all of the dates from the start date to the end date, inclusive
@app.route("/api/v1.0/<start>/<end>")
def start_end_tob(start,end):
    # Create our session (link) from Python to the DB

    session = Session(engine)

    """Return a JSON list of temperature observations (TOBS) from the provided start date and end dates."""
    # Query the tobs for all the dates greater than or equal to the start and less than or equal to the end date
    # Calculate TMIN, TAVG, and TMAX for the dates in the range
    results = (session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs), \
              func.avg(measurement.tobs)).filter((measurement.date) >= start, measurement.date <= end).group_by(measurement.date).all())
    
    # close session
    session.close()

    # Make an empty list to store the tobs of the appended rows data 
    # Make a dictionary for the TMIN, TAVG, and TMAX of each date and append to the empty list. Return the list as a json file
    start_tobs = []
    for date, min,max,avg in results:
        start_end_tob_dict = {}
        start_end_tob_dict["date"] = date
        start_end_tob_dict["min_tobs"] = min
        start_end_tob_dict["max_tobs"] = max
        start_end_tob_dict["avg_tobs"] = avg
        start_tobs.append( start_end_tob_dict)
 
    return jsonify(start_tobs)   
     



if __name__ == '__main__':
    app.run(debug=True)
