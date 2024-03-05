# Import the dependencies.
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np
import pandas as pd
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measure = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate API.<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start-end/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    year_prec = session.query(measure.date, measure.prcp).filter(measure.date >= query_date).order_by(measure.date).all()

    session.close()

    prec_list = [(item[0], 0.0) if item[1] == None else item for item in year_prec]

    prec_dict = {}
    item_list = []
    x = prec_list[0][0]

    for item in prec_list:

        if x == item[0]:

            item_list.append(item[1])

        else:

            prec_dict[x] = item_list
            item_list = []
            item_list.append(item[1])

        x = item[0]

    prec_dict[x] = item_list

    return jsonify(prec_dict)

@app.route("/api/v1.0/stations")
def stations():

    station_list = session.query(measure.station).group_by(measure.station).order_by(func.count(measure.station).desc()).all()

    session.close()

    return jsonify(list(np.ravel(station_list)))

if __name__ == "__main__":
    app.run(debug=True)