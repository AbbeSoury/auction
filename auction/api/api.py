import pandas as pd
import flask
import urllib.parse
from flask import request, jsonify

from auction.session.operators import Drouot, Interencheres

app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET'])
def home():
    return """
        <h1>Drout & Interencheres scrapper results</h1>
        <p>Prototype API to get results of auctions.</p>"""


@app.route('/api/v1/resources/drouotinter/search', methods=['GET'])
def api_drout_inter():

    if 'item' in request.args:
        item = request.args['item']
    else:
        return """Error: No item field provided.
                Please specify an item to search."""
    # Get items from drouot website
    drouot = Drouot(item)
    df_drouot = drouot.transform()

    # Get items from interencheres
    interencheres = Interencheres(item)
    df_interencheres = interencheres.transform()

    df = pd.concat([df_drouot, df_interencheres])
    return jsonify(df.to_dict('records'))


@app.route('/api/v1/resources/drouot/search', methods=['GET'])
def api_drout():

    if 'item' in request.args:
        print(request.args['item'], urllib.parse.unquote(request.args['item']))
        item = request.args['item']
    else:
        return """Error: No item field provided.
                Please specify an item to search."""
    # Get items from drouot website
    drouot = Drouot(item)
    df_drouot = drouot.transform()

    df = df_drouot.copy()
    return jsonify(df.to_dict('records'))


@app.route('/api/v1/resources/inter/search', methods=['GET'])
def api_inter():

    if 'item' in request.args:
        print(request.args['item'], urllib.parse.unquote(request.args['item']))
        item = request.args['item']
    else:
        return """Error: No item field provided.
                Please specify an item to search."""

    # Get items from interencheres
    interencheres = Interencheres(item)
    df_interencheres = interencheres.transform()

    df = df_interencheres.copy()
    return jsonify(df.to_dict('records'))


app.run()
