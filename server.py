#!/usr/bin/env python

import sleepdebugger.config as config
from flask import Flask, request, flash, url_for, render_template, redirect
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

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, threaded=True)
