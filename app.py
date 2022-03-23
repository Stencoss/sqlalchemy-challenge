import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/start_date (In year-month-day Format)</br>"
        f"/api/v1.0/start_date/end_date(In year-month-day Format)"
    )

@app.route("/api/v1.0/precipitation")
def preceipation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    temp_list = []
    for date, prcp in results:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['prcp'] = prcp
        temp_list.append(temp_dict)

    return (jsonify(temp_list))

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    m_active = session.query(Measurement.station).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    session.close()

    test = list(np.ravel(m_active))

    return (jsonify(test))

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    m_station = session.query(Measurement.tobs, Measurement.date).filter(Measurement.station == 'USC00519281', Measurement.date > "2016-08-24").all()
    session.close()

    test = list(np.ravel(m_station))

    return (jsonify(test))


@app.route("/api/v1.0/<date>")
def dates_after(date):
    session = Session(engine)
    m_station = session.query(func.min(Measurement.prcp), func.avg(Measurement.prcp), func.max(Measurement.prcp)).filter( Measurement.date > date).all()
    session.close()

    test = list(np.ravel(m_station))

    return (jsonify(test))

@app.route("/api/v1.0/<date>/<date2>")
def dates_before_after(date, date2):
    session = Session(engine)
    m_station = session.query(func.min(Measurement.prcp), func.avg(Measurement.prcp), func.max(Measurement.prcp)).filter( date < Measurement.date, Measurement.date < date2).all()
    session.close()

    test = list(np.ravel(m_station))

    return (jsonify(test))

if __name__ == "__main__":
    app.run(debug=True)