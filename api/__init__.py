import flask
import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data')


def get_record(recordId):
    data_file_path = os.path.join(DATA_DIR, 'data.json')
    with open(data_file_path, 'r') as fh:
        data = json.load(fh)

    record = data.get(recordId, None)

    if record:
        return {
            recordId: record
        }, 200

    flask.abort(404, 'NotFound')


def update_description(recordId, body):
    print('this is body in handler: ', body)

    # here we add another key to body
    body['status'] = True
    return secondary_function(recordId)


def secondary_function(recordId):

    # here we get the body from flask.request.json
    # notice with the swagger2 file it is updated
    # with the new key "status"
    # but with the swagger 3 file it is not
    body = flask.request.json
    print('this is body in secondary function: ', body)

    data_file_path = os.path.join(DATA_DIR, 'data.json')
    with open(data_file_path, 'r') as fh:
        data = json.load(fh)

    record = data.get(recordId, None)
    if record:
        for k, v in body.items():
            record[k] = v
    else:
        return flask.abort(404, 'NotFound')

    with open(data_file_path, 'w') as fh:
        json.dump(data, fh, indent=4, sort_keys=True)

    return {
        recordId: record
    }, 200


if __name__ == '__main__':
    r = get_record('123')
    r = update_description(recordId='123', body={'description': 'new description'})
