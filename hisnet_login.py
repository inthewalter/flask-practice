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

      # code = crawling(_id, _password)
      with requests.Session() as _session:
        login_request = _session.post('https://hisnet.handong.edu/login.php/_login.php', data={"id":_id, "password":_password})

        post = _session.get('https://hisnet.handong.edu/myboard/list.php?Board=B0029')
        soup = bs(post.text, 'html.parser')
        table = soup.find_all('table')[3].find_all('table')[6]
        count = 0
        for trs in table.find_all('tr'):
          if count == 0:
            count += 1
            continue
          if count == 16:
            break
          print(trs.find_all('a')[0]['href'])
          print(trs.find_all('td')[0].get_text())
          

         return login_request.status_code
    except Exception as err:
      return {'error': str(err)}