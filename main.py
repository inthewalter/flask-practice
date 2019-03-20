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

CODE = {
  'General': 'list.php?Board=NB0001',
  'GlobalLeadership': 'list.php?Board=B0020',
  'InternationalStudy': 'list.php?Board=B0021',
  'Management': 'list.php?Board=B0022',
  'Law': 'list.php?Board=B0023',
  'CommunicationArts': 'list.php?Board=B0024',
  'Counseling': 'list.php?Board=B0102',
  'LifeScience': 'list.php?Board=B0028',
  'SpatialEnvironmentSystem': 'list.php?Board=B0025',
  'ComputerScience': 'list.php?Board=B0029',
  'CCDesign': 'list.php?Board=B0027',
  'Mechanical': 'list.php?Board=B0026',
  'ICT': 'list.php?Board=B0419',
  'LanguageEducation': 'list.php?Board=B0031',
  'CreativeConvergenceEdu': 'list.php?Board=B0427',
  'Graduate': 'list.php?Board=B0113',
  'Scholarship': 'list.php?Board=JANG_NOTICE',
  'Career': 'list.php?Board=B0364',
}


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
  for i in CODE:
    NoticeCrawling.crawling(i, CODE[i])