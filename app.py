#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask.ext.httpauth import HTTPBasicAuth
from functools import wraps

app = Flask(__name__)


infoPoints = [
         {
         'id': 'chapelcredits',
         'data': u'23'
         },
         {
         'id': 'mealpoints',
         'data': u'351',
         },
         {
         'id': 'mealpointsperday',
         'data': u'13',
         },
         {
         'id': 'daysleftinsemester',
         'data': u'88',
         },
         {
         'id': 'studentid',
         'data': u'1111',
         },
         {
         'id': 'temperature',
         'data': u'95',
         }
              
]

def check_auth(username, password):
    return username == 'iGordon' and password == 'swift'

def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)
    
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="\api\"'
    
    return resp

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authT = request.authorization
        if not authT:
            return authenticate()
        
        elif not check_auth(authT.username, authT.password):
            return authenticate()
        return f(*args, **kwargs)
    
    return decorated

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error':'Not found'}), 404)



@app.route('/igordon/api/v1.0/gordoninfo/<string:info_desc>', methods=['GET'])
@requires_auth
def get_gordoninfo(info_desc):
    #refactor this line !!!
     infopoint = [obj for obj in infoPoints if obj['id'] == info_desc]
         # check for a single result
     if len(infopoint) == 0:
        abort(404)
     return jsonify(infopoint[0])

#@app.route('/igordon/api/v1.0/gordoninfo/login', methods=['GET'])
#def get_login():
#    print('LOGIN IN PROGRESS')





if __name__ == '__main__':
    app.run(debug=True)
