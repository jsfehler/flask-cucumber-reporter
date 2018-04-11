import json

from flask import render_template, request
from flask.views import MethodView

from cucumber_output import prepare_feature_data


class AppView(MethodView):
    """Base class for Views in this app."""
    default_css_style = 'hazel'

    @property
    def css_style(self):
        """Returns the style query param from a request."""
        return request.args.get('style', self.default_css_style)

    def render_template(self, template, **kwargs):
        return render_template(
            template,
            css_style=self.css_style,
            **kwargs
        )


class CucumberReporterView(AppView):
    def get_cucumber_data(self):
        """Method that must return a dictionary with the cucumber data."""
        with open('sample_cucumber.json', 'r') as f:
            cucumber_output = json.loads(f.read())

        return cucumber_output

    def get(self):
        data = prepare_feature_data(self.get_cucumber_data())
        return self.render_template(
            'cucumber_overview.html',
            cucumber_output=data["cucumber_output"],
            general_stats=data,
            )
