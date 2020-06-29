# WORKER API SERVICE


## Setting

Create a python virtual environment.

```sh 
virtualenv --python=python3 .env 
```

Activate te environment.

```sh
source .env/bin/activate
```

Install the required python modules.

```sh
pip install -r requirements.txt
```

## Running 

```sh
python api.py
```

## Testing

Open a python console and run the following code to tests the service.

```python
import requests

url = 'http://localhost:8082/environments/'

data = {
    "id": 1,
    "url": "http://localhost:8081/api/environment/environments/1/",
    "name": "ejemplo_30",
    "provider": "virtualbox",
    "address": '',
    "deployment": "http://localhost:8081/api/environment/deployments/1/",
    "cores": 1,
    "memory": 256,
    "status": "",
    "last_report_date": '',
    "worker": "http://localhost:8081/api/worker/workers/1/"
}

response =  requests.post(url,json=data)
print(response.status_code)
print(response.json())
```