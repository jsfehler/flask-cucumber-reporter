import json

from flask import Flask, render_template, request

from cucumber_output import prepare_feature_data

app = Flask(__name__)


@app.route("/")
def reporter_main():
    # CSS Style can be modified with a query string.
    # ie: ?style=dark
    css_style = request.args.get('style', 'hazel')

    with open('sample_cucumber.json', 'r') as f:
        cucumber_output = json.loads(f.read())

    data = prepare_feature_data(cucumber_output)

    return render_template(
        'overview.html',
        css_style=css_style,
        cucumber_output=data["cucumber_output"],
        general_stats=data
    )
