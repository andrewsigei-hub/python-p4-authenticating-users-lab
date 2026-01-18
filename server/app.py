from flask import Flask, request, session, jsonify
from flask_restful import Resource, Api
from models import db, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
api = Api(app)

class Login(Resource):
    
    def post(self):
        # Get username from request JSON
        username = request.get_json()['username']
        
        # Find user by username
        user = User.query.filter(User.username == username).first()
        
        # Set user_id in session
        session['user_id'] = user.id
        
        # Return user as JSON with 200 status
        return user.to_dict(), 200

class Logout(Resource):
    
    def delete(self):
        # Remove user_id from session
        session['user_id'] = None
        
        # Return no data with 204 status
        return '', 204

class CheckSession(Resource):
    
    def get(self):
        # Get user_id from session
        user_id = session.get('user_id')
        
        # If user_id exists in session, find and return user
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 200
        
        # If no user_id in session, return 401
        return {}, 401

# Register resources with API
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)