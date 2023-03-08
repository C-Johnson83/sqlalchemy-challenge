
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
        f"Welcome to my weather station API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Set precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation measurements"""
    # Query all precipitation
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >=  (dt.date(2017,8,23)- dt.timedelta(days=365))).\
    order_by(measurement.date).all()

    # close session
    session.close()

   # Make an empty list to store the dictionary results of the appended row data with 
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
    results = session.query(measurement.station,measurement.date,measurement.tobs).filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= (dt.date(2017,8,23)- dt.timedelta(days=365))).\
        order_by(measurement.date).all()
    
    # close session
    session.close()
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)
    # all_tobs = []
    # for station, date, prcp in results:
    #     prcp_dict = {}
    #     prcp_dict[date] = (station,prcp )
     
    #     all_tobs.append(prcp_dict)

    # return jsonify(all_tobs)

# Return a json list of the minimum temperature, the average temperature,
# and the maximum temperature for a specified start or start-end range. 






# For a specified start, calculate 
# TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
@app.route("/api/v1.0/<start>")
def Start(start):
    session = Session(engine)
    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    results = session.query(measurement.date,func.min(measurement.tobs),
              func.max(measurement.tobs),
              func.avg(measurement.tobs)).\
              filter(measurement.date >= start).all()
    session.close()
    start_tobs = []
    for date,min, max, avg in results:
        start_tobs_dict = {}
        start_tobs_dict["date"] = date
        start_tobs_dict["min_tobs"] = min
        start_tobs_dict["max_tobs"] = max
        start_tobs_dict["avg_tobs"] = avg
        start_tobs.append(start_tobs_dict)
    print (start_tobs)
    return jsonify(start_tobs)   
   
# For a specified start date and end date, calculate TMIN, TAVG, 
# and TMAX for the dates from the start date to the end date, inclusive
@app.route("/api/v1.0/<start>/<end>")
def Start_End(start,end):
    session = Session(engine)
    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    results = session.query(func.min(measurement.tobs),
              func.max(measurement.tobs),
              func.avg(measurement.tobs)).\
              filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    start_end_tobs = []
    for min, max, avg in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_tobs"] = min
        start_end_tobs_dict["max_tobs"] = max
        start_end_tobs_dict["avg_tobs"] = avg
        start_end_tobs.append(start_end_tobs_dict)
    return jsonify(start_end_tobs)

#     if search_term == date:
#         return jsonify(date)
#     return jsonify({"error": f"Im sorry the date {date} was not found."}), 404
    



if __name__ == '__main__':
    app.run(debug=True)
