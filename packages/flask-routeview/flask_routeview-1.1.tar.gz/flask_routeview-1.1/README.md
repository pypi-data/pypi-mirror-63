# Flask RouteView

## Usage

```py
Use like this:

class MyView(RouteView):

    route = "/url"
    name = "MyView"

    def get(*args, **kwargs):
        pass
```