import connexion
import flask
import json
import os
from werkzeug.wrappers import Response
#from werkzeug._compat import BytesIO
#from werkzeug._compat import to_bytes
from io import BytesIO

ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR, 'data')


def init_app(specification_dir, file_name):
    app = connexion.FlaskApp(__name__, specification_dir=specification_dir)
    app.add_api(file_name)
    return app


def get_original_data():
    return {
        "123": {
            "description": "old description",
            "recordId": "123"
        }
    }


def get_updated_data():
    return {
        "123": {
            "description": "this is new description",
            "recordId": "123",
            "status": True
        }
    }


def reset_data():
    data = get_original_data()
    data_file_path = os.path.join(DATA_DIR, 'data.json')
    with open(data_file_path, 'w') as fh:
        json.dump(data, fh, indent=4, sort_keys=True)


def run_exercise(swagger_file):
    reset_data()
    app = init_app('swagger', swagger_file)
    environ = {
        'CONTENT_TYPE': 'application/json',
        'QUERY_STRING': '',
        'PATH_INFO': '/example/123',
        'REQUEST_METHOD': 'GET',
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '80',
        'wsgi.url_scheme': 'http',
        'wsgi.input': BytesIO()
    }
    response = Response.from_app(app, environ=environ)
    data = response.get_data()
    data_json = json.loads(data)
    assert response.status_code == 200
    assert data_json == get_original_data()

    # now do the update
    body = {
        'description': 'this is new description'
    }
    #body_encoded = to_bytes(json.dumps(body).encode('utf-8'), charset='utf-8')
    body_encoded = json.dumps(body).encode('utf-8')
    body_bytes_io = BytesIO(body_encoded)


    # update the request data
    environ['CONTENT_LENGTH'] = str(len(body_encoded))
    environ['wsgi.input'] = body_bytes_io
    environ['REQUEST_METHOD'] = 'PUT'
    response = Response.from_app(app, environ=environ)
    assert response.status_code == 200
    data = response.get_data()
    data_json = json.loads(data)
    assert data_json == get_updated_data()


if __name__ == '__main__':
    print('running first round with swagger 2 file')
    run_exercise('swagger2.yaml')
    print('running second round with swagger 3 file')
    run_exercise('swagger3.yaml')

