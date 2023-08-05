# GWX Core
Is a collection of reusable tools and libraries that can be used within your flask projects.

### Dependencies
- Python 3.7^
- Flask Restplus 0.13^


### Installation
Install the package using pip, by executing:
```python
pip install -U gwx-core
```

### Quick start


Import the **Response Module**, this will handle the formatting of your responses for your `flask_restplus` routes. 
```python
from gwx_core.utils.response import success

class User(Resource):
    def get(self):
        return success('Success', {'key': 'value'}, {'SAMPLE-HEADER': 'header value'})
```

### Usage Documentation
To be added on beta release.



