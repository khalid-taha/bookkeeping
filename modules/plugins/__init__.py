# modules/plugins/__init__.py

class PluginBase:
    def register(self, app):
        """
        Method to register the plugin with the Flask app.
        Must be implemented by all plugins.
        """
        raise NotImplementedError("Plugins must implement the 'register' method.")
