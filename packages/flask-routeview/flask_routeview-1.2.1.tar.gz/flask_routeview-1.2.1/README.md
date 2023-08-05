# Flask RouteView

## Usage

```
# __init__.py

# Create your Flask application
from flask import Flask, request
app = Flask(__name__)

# Register your Flask application in Flask_RouteView
import flask_routeview
flask_routeview.set_app(app)

# Import your views to enable them
from FlaskWebProject.views import IndexView, ...
```

```py
# views.py

class MyView(RouteView):

    route = "/url"
    name = "MyView"

    def get(*args, **kwargs):
        pass
```