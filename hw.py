import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
def welcome():
    return (
        f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
		f"/api/v1.0/stations<br/>"
		f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/temp/start/end<br/>"
    )

   


@app.route("/api/v1.0/precipitation")
def precipitation():
 
   
    precipitation = session.query(Measurement.date, Measurement.prcp).all()

    

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

	stations = session.query(Station.station).all()
	
	return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
	sel = [Measurement.date, Measurement.tobs]
	

	query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
	tobs = session.query(*sel).filter(Measurement.date >= query_date).group_by(Measurement.date).order_by(Measurement.date).all()

	
	return jsonify(tobs)
	
@app.route("/api/v1.0/temp/start/end")
def temps():
	temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= '2016-10-01').filter(Measurement.date <= '2016-10-10').all()
	
	return jsonify(temps)



if __name__ == '__main__':
    app.run(debug=True)
