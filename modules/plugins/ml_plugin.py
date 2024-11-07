# modules/plugins/ml_plugin.py

from modules.plugins import PluginBase
from flask import Blueprint, request, jsonify
import numpy as np

class MLPlugin(PluginBase):
    def register(self, app):
        bp = Blueprint('ml_plugin', __name__, url_prefix='/ml')

        @bp.route('/predict', methods=['GET', 'POST'])
        def predict():
            if request.method == 'POST':
                data = request.json
                if not data or 'input' not in data:
                    return jsonify({'error': 'No input provided.'}), 400
                try:
                    # Ensure input is a list of numbers
                    data['input'] = [float(x) for x in data['input']]
                except (ValueError, TypeError):
                    return jsonify({'error': 'Invalid input format.'}), 400
            else:
                # For GET requests, parse input from query parameters
                input_str = request.args.get('input')
                if not input_str:
                    return jsonify({'error': 'No input provided.'}), 400
                try:
                    data = {'input': [float(x) for x in input_str.split(',')]}
                except ValueError:
                    return jsonify({'error': 'Invalid input format.'}), 400

            # Dummy prediction logic
            x = np.array(data['input'])
            prediction = x.sum()
            # Convert prediction to native Python data type
            return jsonify({'prediction': prediction.item()})

        app.register_blueprint(bp)

plugin = MLPlugin()
