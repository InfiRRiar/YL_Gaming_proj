import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import time
from data import db_session
from data.users import User
from werkzeug.security import generate_password_hash


def main():
    vk_session = vk_api.VkApi(
        token="27fb14f84106404a44cf021312a233bffa80516ed7e18e9e497f373de7eb9ec986c5381bd0edf289a6c85")

    longpoll = VkBotLongPoll(vk_session, '194157847')
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            id = event.obj.message['from_id']
            user_data = vk.users.get(user_ids=id)
            print('Текст нового сообщения:', event.obj.message['text'])
            print(user_data)
            session = db_session.create_session()
            if event.obj.message['text'].lower() == "сброс пароля":
                user = session.query(User).filter(User.vk_id == id).first()
                if user:
                    new_password = ""
                    for i in range(8):
                        i = random.randint(0, 10)
                        new_password += str(i)
                    hashed_password = generate_password_hash(new_password)
                    user.hashed_password = hashed_password
                    session.add(user)
                    session.commit()
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"""Сброс пароля выполнен. Используйте код {new_password} для входа
                                     в аккаунт и измените пароль как можно быстрее.""",
                                     random_id=random.randint(0, 2 ** 64))
                else:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"""Профиль с данным VK не найден. Скорее всего, Вы не привязали
                                                ваш VK к акканту. Это можно сделать на страничке Вашего профиля""",
                                     random_id=random.randint(0, 2 ** 64))
            else:
                flag = True
                user = session.query(User).filter(User.submit_code == event.obj.message['text']).first()
                time.sleep(1)
                if user:
                    if not user.is_submit:
                        user.is_submit = True
                        user.vk_id = str(user_data[0]["id"])
                        session.commit()
                        vk.messages.send(user_id=event.obj.message['from_id'],
                                         message=f"""Ваш аккаунт подтвержден""",
                                         random_id=random.randint(0, 2 ** 64))
                        flag = False
                if flag:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message=f"""Ошибка при подтверждении аккаунта""",
                                     random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    db_session.global_init("db/blogs.sqlite")
    main()
