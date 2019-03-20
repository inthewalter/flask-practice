# flask
from flask import Flask
from flask_restful import Resource, Api

# modules
from create import CreateUser
from hisnet_login import HisnetLogin
from notice_crawling import NoticeCrawling
app = Flask(__name__)
api = Api(app)

api.add_resource(CreateUser, '/user')
api.add_resource(HisnetLogin, '/login')
api.add_resource(NoticeCrawling, '/crawling')


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)