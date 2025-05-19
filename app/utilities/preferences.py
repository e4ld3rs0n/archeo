from flask import session

def init_preferences(app):
    @app.before_request
    def setup_preferences():
        """
        Retrieve preferences from the database or set up default preferences for the user session.
        """
        if "default_view" not in session:
            session["default_view"] = "grid"