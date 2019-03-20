import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import json
import firebase_Create # to communicate with firebase
import my_telegram

class NoticeCrawling :
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

  def __init__(self) :
    self.telegram = my_telegram.MyTelegram()
    self.firebase = firebase_Create.FirebaseCreate()

  def read_database(self):
    with open("notice_list.txt", "r") as f:
      self.notice_list = f.read()

  def write_database(self, info):
    with open("notice_list.txt", "w") as f:
      f.write(info)

  def compare_data(self):
    with open("data.json") as f:
      pass

  def crawling(self, code_name, code_url):
    print(code_name)
    # TODO: seperate into file
    LOGIN_INFO = {
      "id":'mdlee0425',
      "password":'ghkfkd12'
    }
    notice_data = {}
    while(1):
      try:
        with requests.Session() as session:
          login_reqest = session.post('https://hisnet.handong.edu/login/_login.php', data=LOGIN_INFO)
          if login_reqest.status_code != 200:
            raise Exception('ID or password is wrong')
          while(1) :
            try:
              post = session.get('https://hisnet.handong.edu/myboard/' + code_url)
              soup = bs(post.text, 'html.parser')
              if code_name == 'General' :
                table_index = 5
              elif code_name == 'ComputerScience' or code_name == 'Scholarship' or code_name == 'Career':
                table_index = 6
              else :
                table_index = 5

              print('START ' + code_name, code_url, table_index)
              table = soup.find_all('table')[3].find_all('table')[table_index]
              count = 0
              for trs in table.find_all('tr'):
                if count == 0 : # 첫번째 쓰레기 값 skip
                  count += 1
                  continue
                if count == 16 : # 마지막 데이터를 넘기면 break
                  break

                detail_href = trs.find_all('a')[0]['href']
                notice_data['no'] = trs.find_all('td')[0].get_text() 
                notice_data['link'] = detail_href

                if notice_data['no'] != '공지':
                  count += 1
                else:
                  continue

                while(1) :
                  try:
                    post2 = session.get('https://hisnet.handong.edu/myboard/' + detail_href)
                    soup2 = bs(post2.text, 'html.parser')
                    if code_name == 'General' :
                      is_category = True
                      table_index = 9
                    elif code_name == 'ComputerScience':
                      is_category = True
                      table_index = 10
                    elif code_name == 'Career':
                      is_category = True
                      table_index = 9
                    else :
                      is_category = False
                      table_index = 9

                    table2 = soup2.find_all('table')[table_index]
                    trs2 = table2.find_all('tr')

                    notice_data['deep_no'] = trs2[0].find_all('span')[0].get_text()
                    notice_data['title'] = trs2[0].find_all('span')[1].get_text()
                    notice_data['date'] = trs2[0].find_all('span')[3].get_text()
                    notice_data['writer'] = trs2[2].find_all('span')[1].get_text()
                    notice_data['hit'] = trs2[2].find_all('span')[3].get_text()
                    if is_category is True:
                      # notice_data['category'] = trs2[2].find_all('span')[5].get_text() 
                      pass

                    if '첨부 #' in trs2[4].get_text() :
                      download_links = trs2[4].find_all('a')
                      for i in range(0, len(download_links)) :
                        notice_data['download_link#'+str(i)] = download_links[i]['href']
                      # print("내용")
                      # print(trs2[7].find_all('td')[0])
                      notice_data['content'] = str(trs2[7].find_all('td')[0])
                      notice_data['download_link_number'] = len(download_links)
                      pass
                    else:
                      # print("내용")
                      # print(trs2[4].find_all('td')[0])
                      notice_data['content'] = str(trs2[4].find_all('td')[0])
                      pass

                    # TODO: check if it is new or not
                    print(notice_data)
                    self.read_database()
                    if notice_data['deep_no'] in self.notice_list :
                      print('이미~')
                      pass
                    else :
                      self.notice_list = self.notice_list + " " + notice_data['deep_no']
                      self.write_database(self.notice_list)
                      self.firebase.upload(code_name, notice_data)
                    break # 3rd while break
                  except Exception as err :
                    print('<3rd while> error code :')
                    print(err)
                    break
                    # continue
              break # 2rd while break
            except Exception as err :
              print('<2nd while>')
              print(err)
              continue
        break # 1st while break
      except Exception as err :
        print('<1st while>')
        print(err)
        continue

if __name__ == "__main__":
  crawler = noticeCrawling()
  for i in crawler.CODE :
    # print(i)
    # print(crawler.CODE[i])
    crawler.crawling(i, crawler.CODE[i])
