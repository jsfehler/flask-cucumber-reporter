from flask import Flask

from views import CucumberReporterView

app = Flask(__name__)
app.add_url_rule('/', view_func=CucumberReporterView.as_view('index'))
