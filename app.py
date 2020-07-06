import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


# 4. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    results = session.query(Measurement.date, Measurement.prcp).all()
    df = pd.DataFrame(results, columns=['date','prcp'])
    df = df.dropna()
    df['date'] = pd.to_datetime(df.date)
    df = df.sort_index(ascending=False)
    df = df[:365]
    return df.to_json(orient='split')


if __name__ == "__main__":
    app.run(debug=True)
