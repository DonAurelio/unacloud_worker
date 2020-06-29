from flask import Flask
from flask import request
from flask_restplus import Api
from flask_restplus import Resource

import yaml


app = Flask(__name__)
api = Api(app)


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

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8082)