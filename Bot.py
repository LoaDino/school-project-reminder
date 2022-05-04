GROUP_ID = '209327238'
GROUP_TOKEN = '59ae3dfdb6233f3cafce3b1671c8579d46a0bfc9bc168b58d378b0779fdf658c2b51d1bcd8f35c7ed4514'

#----------------------------------------------------------------------------------------------------------------------------

from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import threading
import datetime

#----------------------------------------------------------------------------------------------------------------------------

from EventGetter import EventGetter

eg = EventGetter()

associative_dict = {
    "Математика": [
        "https://olimpiada.ru/activity/72", "https://olimpiada.ru/activity/149",
        "https://olimpiada.ru/activity/1", "https://olimpiada.ru/activity/348",
        "https://olimpiada.ru/activity/443", "https://olimpiada.ru/activity/395",
        "https://olimpiada.ru/activity/246"
    ],
                    
    "Русский язык": [
        "https://olimpiada.ru/activity/80", "https://olimpiada.ru/activity/160"
    ],
                    
    "Информатика": [
        "https://olimpiada.ru/activity/73", "https://olimpiada.ru/activity/153",
        "https://olimpiada.ru/activity/102", "https://olimpiada.ru/activity/5371",
        "https://olimpiada.ru/activity/343", "https://olimpiada.ru/activity/465",
        "https://olimpiada.ru/activity/5283"
    ],
                    
    "Всероссийская Олимпиада Школьников": [ 
        "https://olimpiada.ru/activity/73", "https://olimpiada.ru/activity/72",
        "https://olimpiada.ru/activity/80" 
    ],
                    
    "Высшая проба": [
        "https://olimpiada.ru/activity/153", "https://olimpiada.ru/activity/149",
        "https://olimpiada.ru/activity/160"
    ],

    "Московская олимпиада": [
        "https://olimpiada.ru/activity/1", "https://olimpiada.ru/activity/102"
    ],

    "Ломоносов": [
        "https://olimpiada.ru/activity/348", "https://olimpiada.ru/activity/343"
    ],

    "Олимпиада СПбГУ": [
        "https://olimpiada.ru/activity/465", "https://olimpiada.ru/activity/443"
    ],

    "Физтех": [
        "https://olimpiada.ru/activity/395"
    ],

    "Санкт-Петербургская олимпиада школьников": [
        "https://olimpiada.ru/activity/246"
    ],

    "ТехноКубок": [
        "https://olimpiada.ru/activity/5371"
    ],

    "Innopolis Open": [
        "https://olimpiada.ru/activity/5283"
    ]
}

#----------------------------------------------------------------------------------------------------------------------------

vk_session = VkApi(token = GROUP_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id = GROUP_ID)

#----------------------------------------------------------------------------------------------------------------------------

main_menu = VkKeyboard(one_time = False, inline = True)

main_menu.add_callback_button(
                              label='Найти олимпиаду по предмету',
                              color=VkKeyboardColor.POSITIVE,
                              payload={ "type": "menu_choose", "choose": "subject" }
                             )
main_menu.add_line()

main_menu.add_callback_button(
                              label='Найти олимпиаду по названию', 
                              color=VkKeyboardColor.POSITIVE,
                              payload={ "type": "menu_choose", "choose": "name" }
                             )

#----------------------------------------------------------------------------------------------------------------------------

start_keyboard = VkKeyboard(one_time = False, inline = False)

start_keyboard.add_button(label = "Искать🔎", color = VkKeyboardColor.NEGATIVE)
start_keyboard.add_button(label = "Мои олимпиады", color = VkKeyboardColor.PRIMARY)
start_keyboard.add_line()

start_keyboard.add_button(label = "О создателях", color = VkKeyboardColor.SECONDARY)

#----------------------------------------------------------------------------------------------------------------------------

subjects_names = ["Математика", "Русский язык", "Информатика"]

keyboard_subjects = VkKeyboard(one_time = False, inline = True)

for name in subjects_names:
    keyboard_subjects.add_callback_button(
                                          label = name,
                                          color = VkKeyboardColor.SECONDARY,
                                          payload = {"type": "subject_type", "name": name}
                                         )

    if name != subjects_names[-1]:
        keyboard_subjects.add_line()

#----------------------------------------------------------------------------------------------------------------------------

olympiads_names = [
    "Всероссийская Олимпиада Школьников", "Высшая проба",
    "Московская олимпиада", "Ломоносов",
    "Олимпиада СПбГУ", "Физтех",
    "Санкт-Петербургская олимпиада школьников", "ТехноКубок",
    "Innopolis Open"
]

keyboard_olympiads = VkKeyboard(one_time = False, inline = True)

i = 1
for name in olympiads_names:
    keyboard_olympiads.add_callback_button(
                                           label = name,
                                           color = VkKeyboardColor.SECONDARY,
                                           payload = {"type": "olympiad_type", "name": name}
                                          )
    
    if i%3 == 0 and name != olympiads_names[-1]:
        keyboard_olympiads.add_line()

    i += 1

#----------------------------------------------------------------------------------------------------------------------------

class Buttons:
    def menu(obj):
        vk.messages.send(
                         user_id = obj.message['from_id'],
                         random_id = get_random_id(),
                         keyboard = main_menu.get_keyboard(),
                         message = "Выберите действие:"
                        )

    def creators(obj):
        vk.messages.send(
                         user_id = obj.message['from_id'],
                         random_id = get_random_id(),
                         message = "Создатели: @loadingo (Варначёв Игорь), @id560966675 (Алиев Антон)\nБот сделан как школьный проект."
                        )

    def reminders(obj):
        message = "Список Ваших напоминалок:\n"

        if str(obj.message['from_id']) not in users_reminders:
            users_reminders[str(obj.message['from_id'])] = {}

        months = {
                1 : "января",
                2 : "февраля",
                3 : "марта",
                4 : 'апреля',
                5 : 'мая',
                6 : 'июня',
                7 : 'июля',
                8 : 'августа',
                9 : 'сентября',
                10 : 'октября',
                11 : 'ноября',
                12 : 'декабря'
            }

        for remind in users_reminders[str(obj.message['from_id'])]:
            date = users_reminders[str(obj.message['from_id'])][remind]

            message += f"* {remind} - {date[0]} {months[date[1]]}\n\n"

        vk.messages.send(
                         user_id = obj.message['from_id'],
                         random_id = get_random_id(),
                         message = message
                        )

#----------------------------------------------------------------------------------------------------------------------------

def reminding(THREAD):
    for user in users_reminders:

        for olymp, date in users_reminders[user].items():
            print(olymp, date, [ int(now.day), int(now.month) ] )

            if [ int(now.day)-1, int(now.month) ] == date:
                vk.messages.send(
                        user_id = int(user),
                        random_id = get_random_id(),
                        message = f"Уже завтра начнется {olymp}"
                    )

            if [ int(now.day), int(now.month) ] == date:
                vk.messages.send(
                        user_id = int(user),
                        random_id = get_random_id(),
                        message = f"Сегодня начнется {olymp}"
                    )

    if not THREAD.is_set():
        threading.Timer(86400, reminding, [THREAD]).start()

#----------------------------------------------------------------------------------------------------------------------------

now = datetime.datetime.now()

users_reminders = {}
#users_reminders = { user_id: { "olymp": "date" } }

print("Bot started.")

THREAD = threading.Event()
reminding(THREAD)

for event in longpoll.listen():

    #----------------------------------------------------------------------------------------------------------------------------

    if event.type == VkBotEventType.MESSAGE_NEW:

        if event.obj.message['text'].lower() == "искать🔎":
            Buttons.menu(event.object)

        elif event.obj.message['text'].lower() == "о создателях":
            Buttons.creators(event.object)

        elif event.obj.message['text'].lower() == "мои олимпиады":
            Buttons.reminders(event.object)


        elif event.obj.message['text'].lower() in ("начать", "start"):

            user_name = vk.users.get(user_ids = event.object.message['from_id'])[0]['first_name']
            vk.messages.send(
                             user_id = event.obj.message['from_id'],
                             random_id = get_random_id(),
                             keyboard = start_keyboard.get_keyboard(),
                             message = f"Приветствую Вас, {user_name}\nЧтобы мною пользоваться, используйте кнопки навигации↓"
                            )

    #----------------------------------------------------------------------------------------------------------------------------

    elif event.type == VkBotEventType.MESSAGE_EVENT:
        type_event = event.object.payload.get('type')


        if type_event == "menu_choose":
            choose = event.obj.payload.get("choose")

            if choose == "subject":
                keyboard = keyboard_subjects.get_keyboard()
                message = "Выберите предмет, по которому искать олимпиаду:"

            elif choose == "name":
                keyboard = keyboard_olympiads.get_keyboard()
                message = "Выберите название олимпиады:"

            vk.messages.edit(
                              peer_id = event.obj.peer_id,
                              conversation_message_id = event.obj.conversation_message_id,
                              keyboard = keyboard,
                              message = message
                            )

        #----------------------------------------------------------------------------------------------------------------------------

        elif type_event in ("subject_type", "olympiad_type"):
            event_name = event.object.payload.get("name")

            vk.messages.edit(
                             peer_id = event.obj.peer_id,
                             conversation_message_id = event.obj.conversation_message_id,
                             message = f"Идёт поиск..."
                            )

            answer = ""

            ans_keyboard = VkKeyboard( one_time = False, inline = True )

            i = 1

            months = {
                1 : "января",
                2 : "февраля",
                3 : "марта",
                4 : 'апреля',
                5 : 'мая',
                6 : 'июня',
                7 : 'июля',
                8 : 'августа',
                9 : 'сентября',
                10 : 'октября',
                11 : 'ноября',
                12 : 'декабря'
            }

            k = 0
            for url in associative_dict[event_name]:
                info = eg.getEvent(url)

                ENABLE = True

                label_button = f"В список №{i}"

                if info[0] == (-1, -1):
                    event_start = "В ближайшее время не запланировано"

                    ENABLE = False

                else:
                    day, month = info[0][0], info[0][1]

                    event_start = f"{day} {months[month]}"

                if info[1] == (-1, -1):
                    event_end = "Не запланирован"

                else:
                    day, month = info[1][0], info[1][1]

                    event_end = f"{day} {months[month]}"

                if info[4] != "":
                    add_info = f" ({info[4]})"

                else:
                    add_info = ""

                if type_event == "olympiad_type":
                    main_info = info[3]

                else:
                    main_info = info[2]

                answer += f"{i}. {main_info}{add_info}\n\tНачало: {event_start}\n\tКонец: {event_end}\n\n"

                i += 1

                if str(event.obj.user_id) not in users_reminders:
                    users_reminders[str(event.obj.user_id)] = {}

                if f"{info[2]}, {info[3]}, {info[4]}" in users_reminders[str(event.obj.user_id)]:
                    ENABLE = False


                if not ENABLE:
                    label_button += " (невозможно)"


                ans_keyboard.add_callback_button(
                    label=label_button,
                    color=VkKeyboardColor.SECONDARY,
                    payload={
                              "type": "olympiad_choose",
                              "enable": ENABLE,
                              "choose": [f"{info[2]}, {info[3]}, {info[4]}", info[0]],
                              "user_id": str(event.obj.user_id)
                            }
                )

                if i%3 ==0 and url != associative_dict[event_name][-1]:
                    ans_keyboard.add_line()

                k += 1



            vk.messages.edit(
                             peer_id = event.obj.peer_id,
                             conversation_message_id = event.obj.conversation_message_id,
                             keyboard = ans_keyboard.get_keyboard(),
                             message = answer
                            )

        #----------------------------------------------------------------------------------------------------------------------------

        elif type_event == "olympiad_choose":
            payload = event.obj.payload

            if payload["enable"]:
                if payload["user_id"] not in users_reminders:
                    users_reminders[payload["user_id"]] = {}

                info = payload["choose"]

                users_reminders[payload["user_id"]][info[0]] = info[1]

                vk.messages.send(
                    user_id = payload["user_id"],
                    random_id = get_random_id(),
                    message = "Успешно✅"
                )

            else:
                vk.messages.send(
                    user_id = payload["user_id"],
                    random_id = get_random_id(),
                    message = "невозможно❌"
                )