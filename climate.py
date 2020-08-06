import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False})

Base = automap_base()
Base.prepare(engine, reflect = True)
Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

#weather app

app = Flask(__name__)


latest_date = (session.query(Measurement.date).order_by(Measurement.date.desc()).first())
latest_date = list(np.ravel(latest_date))[0]
latest_date = dt.datetime.strptime(latest_date, '%Y-%m-%d')

latest_year = int(dt.datetime.strftime(latest_date, '%Y'))
latest_month = int(dt.datetime.strftime(latest_date, '%m'))
latest_day = int(dt.datetime.strftime(latest_date, '%d'))

oneyear_ago = dt.date(latest_year, latest_month, latest_day) - dt.timedelta(days=365)
oneyear_ago = dt.datetime.strftime(oneyear_ago, '%Y-%m-%d')

@app.route("/")
def home():
    return(
        f"Welcome to Surf's up! Climate API <br/>"
        f"Available routes are: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/<start> <br/>"
        f"/api/v1.0/<end>" 

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    rain_data = (session.query(Measurement.date, Measurement.prcp,Measurement.station)\
             .filter(Measurement.date > oneyear_ago) \
             .order_by(Measurement.date).all())

    precipitation_data = []
    for rain in rain_data:
        precipitation_dict = {rain.date: rain.prcp, "Station": rain.station }
        precipitation_data.append(precipitation_dict)

    return jsonify(precipitation_dict)


@app.route("/api/v1.0/stations")
def stations():
    all_stations = session.query(Station.name).all()
    all_stations = list(np.ravel(all_stations))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    temperature_data = session.query(Measurement.date, Measurement.tobs, Measurement.station)\
                        .filter(Measurement.date > oneyear_ago)\
                        .order_by(Measurement.date).all()
    tempData = []
    for temp in temperature_data:
        temp_dict = {temp.date: temp.tobs, "Station": temp.station}
        tempData.append(temp_dict)
    
    return jsonify(tempData)


if __name__ == "__main__":
    app.run(debug=True)
