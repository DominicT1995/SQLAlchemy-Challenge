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
        f"/api/v1.0/start/&ltstart&gt<br/>"
        f"/api/v1.0/start-end/&ltstart&gt/&ltend&gt<br/><br/>"
        f"Dates for &ltstart&gt and &ltend&gt should be formatted as mm-dd-yyyy or mmddyyyy."
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

    station_list = session.query(measure.station).\
        group_by(measure.station).order_by(func.count(measure.station).desc()).all()

    session.close()

    return jsonify(list(np.ravel(station_list)))

@app.route("/api/v1.0/tobs")
def tobs():

    temp_query_date = dt.date(2017, 8, 18) - dt.timedelta(days=365)

    active_station = session.query(measure.station).\
        group_by(measure.station).order_by(func.count(measure.station).desc()).first()

    temp_data = session.query(measure.date, measure.tobs)\
        .filter(measure.date >= temp_query_date).filter(measure.station == active_station[0]).all()

    session.close()

    all_temps = []
    for date, tobs in temp_data:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = tobs
        all_temps.append(temp_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/start/<start>")
def start_date(start):

    canon = start.replace("-", "")

    mm = int(canon[slice(0, 2)])
    dd = int(canon[slice(2, 4)])
    yyyy = int(canon[slice(4, 8)])

    user_start_input = dt.date(yyyy, mm, dd)

    db_check = list(np.ravel(session.query(measure.date).all()))

    if user_start_input.strftime("%Y-%m-%d") in db_check:

        start_search = session.query(func.min(measure.tobs), func.max(measure.tobs), func.avg(measure.tobs)).\
            filter(measure.date >= user_start_input).all()
        
        session.close()

        start_results = []
        for stat in start_search:
            start_dict = {}
            start_dict["min"] = stat[0]
            start_dict["max"] = stat[1]
            start_dict["avg"] = stat[2]
            start_results.append(start_dict)

        return jsonify(start_results)
    
    else:
        
        session.close()

        return jsonify({"error": f"Date: {start} not found in database."}), 404

@app.route("/api/v1.0/start-end/<start>/<end>")
def start_end_date(start, end):

    canon_start = start.replace("-", "")
    canon_end = end.replace("-", "")

    mm_st = int(canon_start[slice(0, 2)])
    dd_st = int(canon_start[slice(2, 4)])
    yyyy_st = int(canon_start[slice(4, 8)])

    mm_ed = int(canon_end[slice(0, 2)])
    dd_ed = int(canon_end[slice(2, 4)])
    yyyy_ed = int(canon_end[slice(4, 8)])

    user_start_input = dt.date(yyyy_st, mm_st, dd_st)
    user_end_input = dt.date(yyyy_ed, mm_ed, dd_ed)

    db_check = list(np.ravel(session.query(measure.date).all()))

    if (user_start_input.strftime("%Y-%m-%d") and user_end_input.strftime("%Y-%m-%d") in db_check) and (user_end_input > user_start_input):

        dates_search = session.query(func.min(measure.tobs), func.max(measure.tobs), func.avg(measure.tobs)).\
            filter(measure.date >= user_start_input, measure.date <= user_end_input).all()
        
        session.close()

        dates_results = []
        for stat in dates_search:
            dates_dict = {}
            dates_dict["min"] = stat[0]
            dates_dict["max"] = stat[1]
            dates_dict["avg"] = stat[2]
            dates_results.append(dates_dict)

        return jsonify(dates_results)
    
    elif user_start_input.strftime("%Y-%m-%d") and user_end_input.strftime("%Y-%m-%d") not in db_check:
        
        session.close()

        return jsonify({"error": f"Date: '{start}' or '{end}' not found in database."}), 404
    
    elif user_end_input < user_start_input:

        session.close()

        return jsonify({"error": f"start date '{start}' is later than end date '{end}', null values returned."}), 404

if __name__ == "__main__":
    app.run(debug=True)