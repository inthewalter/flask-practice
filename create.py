from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

class CreateUser(Resource):
  def post(self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('email', type=str)
      parser.add_argument('user_name', type=str)
      parser.add_argument('password', type=str)
      args = parser.parse_args()

      _userEmail = args['email']
      _userName = args['user_name']
      _userPassword = args['password']
      return {'Email': args['email'], 'UserName': args['user_name'], 'Password': args['password']}
    except Exception as err:
      return {'error': str(err)}
