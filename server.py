#!/usr/bin/env python

from dateutil.parser import parse
from math import modf
from time import mktime
import csv
import StringIO
import sleepdebugger.config as config
from flask import Flask, request, flash, url_for, render_template, redirect, Response
from flask_debugtoolbar import DebugToolbarExtension
from influxdb import InfluxDBClient

app = Flask(__name__,
    static_url_path = "/static",
    static_folder = "sleepdebugger/web/static",
    template_folder = "sleepdebugger/web/template")

app.secret_key = config.SECRET_KEY
app.debug = config.DEBUG
toolbar = DebugToolbarExtension(app)

@app.route("/", methods=['GET'])
def index():
    return render_template("index")

@app.route("/", methods=['POST'])
def record():
    txt = request.form['entry']
    try:
        influx = InfluxDBClient(config.INFLUX_HOST, config.INFLUX_PORT, config.INFLUX_USER, config.INFLUX_PASSWD, config.INFLUX_DB)
    except Exception as err:
        flash("Entry was not recorded. Influx connection error: %s" % str(err))

    if influx:
        json_body = [
            {
                "measurement": "notes",
                "tags":
                {
                    "sleeper": config.SLEEPER
                },
                "fields": { 'note' : txt }
            }
        ]
        try:
            influx.write_points(json_body)
            flash('Entry recorded.')
        except Exception as err:
            flash("Entry was not recorded. Influx write error: %s" % str(err))

    return render_template("index")

@app.route("/export", methods=['GET'])
def export():
    return render_template("export")

@app.route("/export", methods=['POST'])
def export_data():
    start = request.form['start']
    end = request.form['end']

    try:
        start = parse(start)
    except ValueError:
        flash("Cannot decipher format of start time.")
        return render_template("export", start=request.form['start'], end=request.form['end'])

    try:
        end = parse(end)
    except ValueError:
        flash("Cannot decipher format of end time.")
        return render_template("export", start=request.form['start'], end=request.form['end'])
    
    try:
        influx = InfluxDBClient(config.INFLUX_HOST, config.INFLUX_PORT, config.INFLUX_USER, config.INFLUX_PASSWD, config.INFLUX_DB)
    except Exception as err:
        flash("Cannot connect to DB.")
        return render_template("export", start=request.form['start'], end=request.form['end'])

    decimal, integer = modf(mktime(start.timetuple()))
    start = "%d" % integer + "%09d" % (decimal * 1000000000)

    decimal, integer = modf(mktime(end.timetuple()))
    end = "%d" % integer + "%09d" % (decimal * 1000000000)
    
    query = "SELECT mag FROM sleep WHERE time >= %s and time <= %s" % (start, end)
    try:
        results = influx.query(query)
    except Exception as e:
        flash("Cannot query influx: %s" % str(e))
        return render_template("export", start=request.form['start'], end=request.form['end'])

    si = StringIO.StringIO()
    cw = csv.writer(si)
    for result in results.get_points(measurement="sleep"):
        print result 
        cw.writerow([ result['time'], result['mag'] ])

    return Response(si.getvalue().strip('\r\n'), mimetype='text/csv')

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, threaded=True)
