import telegram

class MyTelegram:
  def __init__(self):
    self.my_token = '436711366:AAEFFkIqht-rljMfoBtgRIwlmRqwnKGPs0U' # 텔레그램 토큰
    self.chat_id = '442713085'
    self.bot = telegram.Bot(token = self.my_token)
    pass

  def sendNotification(self, msg):
    self.bot.sendMessage(chat_id = self.chat_id, text = msg)
    pass
