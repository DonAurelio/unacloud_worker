import requests


if __name__ == '__main__':

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