# Plugin System Documentation

The plugin system allows you to extend the functionality of your application by adding modular, self-contained components. Plugins can register their own routes, blueprints, and other Flask extensions to the main application.

This documentation covers how to create and integrate plugins into your application, using the provided `PluginBase` class. We'll also go through examples of existing plugins: `sample_plugin.py` and `ml_plugin.py`.

## Table of Contents

- [Plugin System Documentation](#plugin-system-documentation)
  - [Table of Contents](#table-of-contents)
  - [Plugin Base Class](#plugin-base-class)
  - [Creating a Plugin](#creating-a-plugin)
  - [Sample Plugin](#sample-plugin)
    - [Code Overview](#code-overview)
    - [Usage](#usage)
  - [ML Plugin](#ml-plugin)
    - [Code Overview](#code-overview-1)
    - [Endpoints](#endpoints)
      - [`/ml/predict`](#mlpredict)
        - [GET Request](#get-request)
        - [POST Request](#post-request)
    - [Usage](#usage-1)
      - [GET Request Example](#get-request-example)
      - [POST Request Example](#post-request-example)
      - [Error Handling](#error-handling)
  - [Integrating Plugins](#integrating-plugins)
  - [Testing Plugins](#testing-plugins)
    - [Sample Plugin Tests](#sample-plugin-tests)
    - [ML Plugin Tests](#ml-plugin-tests)
  - [Conclusion](#conclusion)

## Plugin Base Class

All plugins should inherit from the `PluginBase` class provided in `modules/plugins/__init__.py`.

```python
# modules/plugins/__init__.py

class PluginBase:
    def register(self, app):
        """
        Method to register the plugin with the Flask app.
        Must be implemented by all plugins.
        """
        raise NotImplementedError("Plugins must implement the 'register' method.")
```

The `register` method is where you define how your plugin integrates with the main Flask application.

## Creating a Plugin

To create a new plugin:

1. **Create a new Python file** in the `modules/plugins/` directory, e.g., `my_plugin.py`.

2. **Import the `PluginBase` class** and inherit from it.

3. **Implement the `register` method**, where you can set up blueprints, routes, and any other integration.

Example skeleton:

```python
# modules/plugins/my_plugin.py

from modules.plugins import PluginBase
from flask import Blueprint

class MyPlugin(PluginBase):
    def register(self, app):
        bp = Blueprint('my_plugin', __name__, url_prefix='/my_plugin')

        @bp.route('/')
        def index():
            return "Hello from My Plugin!"

        app.register_blueprint(bp)

plugin = MyPlugin()
```

## Sample Plugin

The `sample_plugin.py` is a simple example demonstrating how to create and register a plugin.

### Code Overview

```python
# modules/plugins/sample_plugin.py

from modules.plugins import PluginBase
from flask import Blueprint

class SamplePlugin(PluginBase):
    def register(self, app):
        bp = Blueprint('sample_plugin', __name__, url_prefix='/sample_plugin')

        @bp.route('/')
        def index():
            return "Hello from Sample Plugin!"

        app.register_blueprint(bp)

plugin = SamplePlugin()
```

### Usage

- **Endpoint:** `/sample_plugin/`
- **Method:** `GET`
- **Response:** Returns a simple greeting message.

**Example Request:**

```bash
GET /sample_plugin/
```

**Example Response:**

```
Hello from Sample Plugin!
```

## ML Plugin

The `ml_plugin.py` provides a more complex example, including handling of POST and GET requests with input validation and processing using NumPy.

### Code Overview

```python
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
                    data['input'] = [float(x) for x in data['input']]
                except (ValueError, TypeError):
                    return jsonify({'error': 'Invalid input format.'}), 400
            else:
                input_str = request.args.get('input')
                if not input_str:
                    return jsonify({'error': 'No input provided.'}), 400
                try:
                    data = {'input': [float(x) for x in input_str.split(',')]}
                except ValueError:
                    return jsonify({'error': 'Invalid input format.'}), 400

            x = np.array(data['input'])
            prediction = x.sum()
            return jsonify({'prediction': prediction.item()})

        app.register_blueprint(bp)

plugin = MLPlugin()
```

### Endpoints

#### `/ml/predict`

- **Methods:** `GET`, `POST`

##### GET Request

- **Query Parameter:** `input` (comma-separated numbers)
- **Example:** `/ml/predict?input=1,2,3`

##### POST Request

- **Content-Type:** `application/json`
- **Body:**

  ```json
  {
    "input": [1, 2, 3]
  }
  ```

### Usage

#### GET Request Example

**Request:**

```bash
GET /ml/predict?input=1,2,3,4,5
```

**Response:**

```json
{
  "prediction": 15.0
}
```

#### POST Request Example

**Request:**

```bash
POST /ml/predict
Content-Type: application/json

{
  "input": [1, 2, 3, 4, 5]
}
```

**Response:**

```json
{
  "prediction": 15.0
}
```

#### Error Handling

- If the `input` parameter is missing or invalid, the endpoint returns a `400 Bad Request` with an error message.

**Example:**

```json
{
  "error": "Invalid input format."
}
```

## Integrating Plugins

The plugins are automatically discovered and registered by the application during startup. This is handled in the `create_app` function in `app/__init__.py`.

```python
# app/__init__.py

def load_plugins(app):
    from modules.plugins import PluginBase
    import modules.plugins

    for _, name, is_pkg in pkgutil.iter_modules(modules.plugins.__path__):
        if not is_pkg:
            module = importlib.import_module(f'modules.plugins.{name}')
            if hasattr(module, 'plugin') and isinstance(module.plugin, PluginBase):
                module.plugin.register(app)
```

To integrate a new plugin:

1. **Place your plugin file** in the `modules/plugins/` directory.

2. **Ensure your plugin class** inherits from `PluginBase` and implements the `register` method.

3. **Instantiate your plugin** at the bottom of your plugin file:

   ```python
   plugin = MyPlugin()
   ```

4. The application will automatically discover and register your plugin when it starts.

## Testing Plugins

Tests for plugins are located in the `tests/plugins/` directory. Each plugin should have corresponding tests to ensure its functionality.

### Sample Plugin Tests

**File:** `tests/plugins/test_sample_plugin.py`

```python
def test_sample_plugin(client):
    response = client.get('/sample_plugin/')
    assert response.status_code == 200
    assert response.data.decode() == 'Hello from Sample Plugin!'
```

### ML Plugin Tests

**File:** `tests/plugins/test_ml_plugin.py`

```python
import json

def test_ml_plugin_post(client):
    response = client.post('/ml/predict', json={'input': [1, 2, 3, 4, 5]})
    assert response.status_code == 200
    data = response.get_json()
    assert data['prediction'] == 15.0

def test_ml_plugin_post_invalid_input(client):
    response = client.post('/ml/predict', json={'input': 'invalid'})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid input format.'

def test_ml_plugin_get(client):
    response = client.get('/ml/predict?input=1,2,3,4,5')
    assert response.status_code == 200
    data = response.get_json()
    assert data['prediction'] == 15.0

def test_ml_plugin_get_no_input(client):
    response = client.get('/ml/predict')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'No input provided.'

def test_ml_plugin_get_invalid_input(client):
    response = client.get('/ml/predict?input=a,b,c')
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Invalid input format.'
```

## Conclusion

The plugin system provides a flexible way to extend the functionality of your application. By following the `PluginBase` structure and registering your plugins properly, you can modularize features and maintain a clean codebase.

Remember to:

- **Inherit from `PluginBase`** for all plugins.
- **Implement the `register` method** to integrate with the Flask app.
- **Use blueprints** to encapsulate plugin routes.
- **Add tests** to ensure your plugins work as expected.

For any questions or further assistance, feel free to reach out or consult the existing plugin examples.

---
