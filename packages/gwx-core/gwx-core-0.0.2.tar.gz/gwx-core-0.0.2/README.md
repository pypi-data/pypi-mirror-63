<div align="center">
 <img alt="GWX Core" src="https://repository-images.githubusercontent.com/245329234/a1e78400-614a-11ea-9463-d54c4a260e90" width="300px" height="150px" />
</div>

<div align="center">
Is a collection of reusable tools and libraries that can be used within your flask projects.
</div>
<br />

---

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
from gwx_core.utils import response

class User(Resource):
    def get(self):
        return response.success('Success', {'key': 'value'}, {'SAMPLE-HEADER': 'header value'})
```

### Usage Documentation
To be added on beta release.



