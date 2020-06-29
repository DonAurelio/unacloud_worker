from flask import Flask
from flask import request
from flask_restplus import Api
from flask_restplus import Resource

import yaml
import requests

app = Flask(__name__)
api = Api(app)


# Base API url without the ending slash
API_SERVER_BASE_URL = 'http://localhost:8081'


@api.route('/environments/')
class Environment(Resource):
    def post(self):
        environment = request.get_json()
        eid = environment.get('id')
        provider = environment.get('provider')
        cpus = environment.get('cores')
        memory = environment.get('memory')

        data = {
            'provider': provider,
            'name': eid,
            'specs': {
                'cpus': cpus,
                'memory': memory
            }
        }

        file_path = '../deployd/manifests/%s.yml' % eid
        with open(file_path, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

        response = {
            'message': 'Execituon was stored sucessfully !!'
        }
        return response,200


@api.route('/environments/deployment/status_updates/')
class Deployment(Resource):
    def post(self):
        """
        Forwards the data received by the deployd to the 
        API SERVER. The data is related with the deployment 
        status of an environment.
        """

        try:
            data = request.get_json()
            endpoint = '/deployment/status_updates/'
            url = API_SERVER_BASE_URL + endpoint

            response = requests.post(url)
            response.raise_for_status()

            response = {
                'status_updated': True,
                'message': 'Deployment status successfully updated in the API SERVER'
            }

        except Exception as e:
            response = {
                'status_updated': False,
                'message': str(e)
            }
            
        return response,200

# @api.route('/environments/action/status_updates/')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8082)