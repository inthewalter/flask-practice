import requests
from bs4 import BeautifulSoup as bs

from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse

# hisnet login class
class HisnetLogin(Resource):
  def post(self):
    try:
      parser = reqparse.RequestParser()
      parser.add_argument('id', type=str)
      parser.add_argument('password', type=str)
      args = parser.parse_args()

      _id = args['id']
      _password = args['password']

      code = crawling(_id, _password)

      return code
    except Exception as err:
      return {'error': str(err)}

  def crawling(self, _id, _password):
    with requests.Session() as s:
      login_reqest = s.post('https://hisnet.handong.edu/login.php/_login.php', data={"id":_id, "password":_password})
      return login_request.status_code