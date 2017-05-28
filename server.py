#!/usr/bin/env python

import sleepdebugger.config as config
from flask import Flask, request, flash, url_for, render_template, redirect
app = Flask(__name__,
    static_url_path = "/static",
    static_folder = "sleepdebugger/web/static",
    template_folder = "sleepdebugger/web/template")

app.secret_key = config.SECRET_KEY

@app.route("/", methods=['GET'])
def index():
    return render_template("index")

@app.route("/", methods=['POST'])
def record():
    flash('Entry recorded.')
    return render_template("index")

if __name__ == "__main__":
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT, threaded=True)
