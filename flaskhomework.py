# import dependencies 
import datetime 
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def welcome():

     return (
         f"Avalable Routes:<br/>"
         f"/api/v1.0/precipitation"
         f"- Dates and temperature observations from the last year<br/>"

         f"/api/v1.0/stations"
         f"- List of stations<br/>"

         f"/api/v1.0/tobs"
         f"- Temperature Observations from the past year<br/>"

         f"/api/v1.0/<start>"
         f"- Minimum temperature, the average temperature, and the max temperature for a given start day<br/>"

         f"/api/v1.0/<start>/<end>"
         f"- Minimum temperature, the average temperature, and the max temperature for a given start-end range<br/>"
     )

@app.route("/api/v1.0/precipitation")
def pcrp():
    # create the date range, use today as the api here does not take a start/end date
    today = datetime.datetime.today()
    today = today.date()
    last_year = today - datetime.timedelta(365)
    pcp_year = session.query(Measurement.date, Measurement.prcp).filter(and_(Measurement.date <= today, Measurement.date >= last_year)).all()
    return jsonify(pcp_year)

@app.route("/api/v1.0/stations")
def station_list():
    st_list = session.query(Station.station).all()

    all_stations= list(np.ravel(st_list))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temp_year():
    # create the date range, use today as the api here does not take a start/end date
    today = datetime.datetime.today()
    today = today.date()
    last_year = today - datetime.timedelta(365)
    temp_year = session.query(Measurement.date, Measurement.tobs).filter(and_(Measurement.date <= today, Measurement.date >= last_year)).all()

    return jsonify(temp_year)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    # get the min/avg/max
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    return jsonify(temp_data)

    

@app.route("/api/v1.0/<start>/<end>")
def range_temp(start, end):
 # get the min/avg/max
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(and_(Measurement.date >= start, Measurement.date <= end)).all()
    
    return jsonify(temp_data)

if __name__ == '__main__':
    app.run(debug=True)