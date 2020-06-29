from flask import Flask
from flask import request
from flask_restplus import Api
from flask_restplus import Resource

import yaml
import requests
import logging


app = Flask(__name__)
api = Api(app)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

# Base API url without the ending slash
API_SERVER_BASE_URL = 'http://localhost:8081/api'


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

@api.route('/actions/')
class Action(Resource):
    def post(self):
        action_data = request.get_json()
        action_id = action_data.get('action_id')
        environment_id = action_data.get('environment_id')
        provider = action_data.get('provider')
        action = action_data.get('action')

        data = {
            'name': environment_id,
            'provider': provider,
            'action': action,
            'action_id': action_id
        }

        file_path = '../deployd/manifests/%s.yml' % environment_id
        with open(file_path, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)

        response = {
            'message': 'Action was stored sucessfully !!'
        }
        return response,200

@api.route('/environment/deployment/status_update/')
class Deployment(Resource):
    def post(self):
        """
        Forwards the data received by the deployd to the 
        API SERVER. The data is related with the deployment 
        status of an environment.
        """

        # try:
        data = request.get_json()
        endpoint = '/environment/deployment/status_update/'
        url = API_SERVER_BASE_URL + endpoint

        response = requests.post(url,json=data)
        response.raise_for_status()

        response = {
            'status_updated': True,
            'message': 'Deployment status successfully updated in the API SERVER'
        }

        # except Exception as e:
        #     logger.exception(e)
        #     response = {
        #         'status_updated': False,
        #         'message': str(e)
        #     }
            
        return response,200


@api.route('/environment/action/status_update/')
class ActionDeployment(Resource):
    def post(self):
        """
        Forwards the data received by the deployd to the 
        API SERVER. The data is related with the deployment 
        status of an environment.
        """

        # try:
        data = request.get_json()
        endpoint = '/environment/action/status_update/'
        url = API_SERVER_BASE_URL + endpoint

        response = requests.post(url,json=data)
        response.raise_for_status()

        response = {
            'status_updated': True,
            'message': 'Action status successfully updated in the API SERVER'
        }

        # except Exception as e:
        #     logger.exception(e)
        #     response = {
        #         'status_updated': False,
        #         'message': str(e)
        #     }
            
        return response,200

# @api.route('/environments/action/status_updates/')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8082)