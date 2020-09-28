import vk_api
import datetime
import sqlite3
from vk_api.longpoll import VkLongPoll, VkEventType

class Bot():
    def __init__(self):
        self.db = sqlite3.connect('users.db')  # for data base
        self.cursor = self.db.cursor()         #     ^
        self.token = "0740fac27ff8a970964df25d0888295c6773ee48eb86ce9d23d4229fc8e86e8939b3fc4754f7b51d09c7c"
        self.connect = vk_api.VkApi(token = self.token)
        self.longpoll = VkLongPoll(self.connect)
        self.message = None     # messages text

    def main(self):     # main function
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                self.message = event.text

                user = event.user_id

                if self.cursor.execute("SELECT have FROM users WHERE user_id = ?", (user, )).fetchall() != []:   # find user in db
                    print("\n user was found\n")

                else:       # insert user in db if not exists
                    self.cursor.execute("""
                    INSERT INTO users VALUES(
                        ?, 1, 1
                    )
                    """, (user, ))
                    self.db.commit()

                    print('user add to data base')

                if self.message[0] == '!':      # check message on have command
                    if self.message == "!время":
                        self.getTime(event.user_id)
                    elif self.message == '!привет':
                        self.writeMessage('Привет!' ,event.user_id)
                    elif self.message == "!установить статус":
                        user_id = event.user_id
                        target_id, new_status = self.getInfo(user_id)
                        self.setStatus(user_id, new_status, target_id)
                    else:
                        pass

    def getTime(self, user_id):  # fuction for take date from system
        a = datetime.datetime.now()
        self.message = str(a.hour) + ':' + str(a.minute) + ':' + str(a.second) + ' по Москве'
        self.writeMessage(self.message, user_id)
        self.main()

    def getInfo(self, user_id):
        self.writeMessage("Введите имя пользователя", user_id)

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                target_id = event.text
                break

        self.writeMessage("Введите новый статус пользователся", user_id)

        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                new_status = event.text
                if int(new_status) > 10:
                    self.writeMessage("Ошибка", user_id) 
                    self.getInfo(user_id)
                    break

                else:
                    return target_id, new_status
                    

    def setStatus(self, user_id, new_status, target_id):
        user_status = self.cursor.execute('SELECT status FROM users WHERE user_id = ?', user_id)
        target_status = self.cursor.execute('SELECT status FROM users WHERE user_id = ?', target_id)

        if user_status > target_status:
            if new_status <= user_status:
                self.cursor.execute("""
                    UPDATE users SET status = ? WHERE user_id = ?
                """, (new_status, target_id)
                )

    def writeMessage(self, message, user_id):
        self.connect.method('messages.send', {
            'user_id': user_id,
            'message': message,
            'random_id': 0
        })

bot = Bot()
bot.main()