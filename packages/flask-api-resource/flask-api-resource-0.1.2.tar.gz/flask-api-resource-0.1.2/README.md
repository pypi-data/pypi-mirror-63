# Flask Api Resource

> package flask to use conveniently like django

# Usage

## Step 1

```python
from flask import Flask
from flask_api_resource import FlaskApiResource

app = Flask(__name__)
app.config['INSTALL_APPS'] = []  # your application app like user
api = FlaskApiResource()
api.init_app(app=app)  # this can auto scan your resource
```

## Step 2
According to your logic to create different app

```text
user
    __init__.py
    apis
        user.py
```

```python
# user.py
from flask_api_resource.api import BaseResource
from flask_api_resource.decorator import get

class UserResource(BaseResource):
    
    def get_urls(self):
        return [
            ('/detail', self.detail)
        ]
    
    @get
    def detail(self):
        return self.success({'id': 1})
```

```python
# __init__.py

def register(api):
    from .apis.user import UserResource
    api.register(UserResource)
```

## Step 3

run the Flask app server and open the http://127.0.0.1:5000/rest/user/detail