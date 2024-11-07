# modules/plugins/sample_plugin.py

from modules.plugins import PluginBase
from flask import Blueprint

class SamplePlugin(PluginBase):
    def register(self, app):
        # Create a blueprint for the plugin
        bp = Blueprint('sample_plugin', __name__, url_prefix='/sample_plugin')

        @bp.route('/')
        def index():
            return "Hello from Sample Plugin!"

        # Register the blueprint with the app
        app.register_blueprint(bp)

# Instantiate the plugin
plugin = SamplePlugin()
