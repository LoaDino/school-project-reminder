import requests
from lxml import html

class EventGetter:
    def getEvent(self, url):
        data = requests.get(url)

        olymps = {
            "https://olimpiada.ru/activity/73": "Всероссийская Олимпиада Школьников",
            "https://olimpiada.ru/activity/72": "Всероссийская Олимпиада Школьников",
            "https://olimpiada.ru/activity/80": "Всероссийская Олимпиада Школьников",
            "https://olimpiada.ru/activity/153": "Высшая проба",
            "https://olimpiada.ru/activity/149": "Высшая проба",
            "https://olimpiada.ru/activity/160": "Высшая проба",
            "https://olimpiada.ru/activity/1": "Московская олимпиада",
            "https://olimpiada.ru/activity/102": "Московская олимпиада",
            "https://olimpiada.ru/activity/348": "Ломоносов",
            "https://olimpiada.ru/activity/343": "Ломоносов",
            "https://olimpiada.ru/activity/465": "Олимпиада СПбГУ",
            "https://olimpiada.ru/activity/443": "Олимпиада СПбГУ",
            "https://olimpiada.ru/activity/395": "Физтех",
            "https://olimpiada.ru/activity/246":"Санкт-Петербургская олимпиада школьников",
            "https://olimpiada.ru/activity/5371": "ТехноКубок",
            "https://olimpiada.ru/activity/5283": "Innopolis Open"

        }

        subjects = {
            "https://olimpiada.ru/activity/73": "Информатика",
            "https://olimpiada.ru/activity/72": "Математика",
            "https://olimpiada.ru/activity/80": "Русский язык",
            "https://olimpiada.ru/activity/153": "Информатика",
            "https://olimpiada.ru/activity/149": "Математика",
            "https://olimpiada.ru/activity/160": "Русский язык",
            "https://olimpiada.ru/activity/1": "Математика",
            "https://olimpiada.ru/activity/348": "Математика",
            "https://olimpiada.ru/activity/443": "Математика",
            "https://olimpiada.ru/activity/395": "Математика",
            "https://olimpiada.ru/activity/246": "Математика",
            "https://olimpiada.ru/activity/102": "Информатика",
            "https://olimpiada.ru/activity/5371": "Информатика",
            "https://olimpiada.ru/activity/343": "Информатика",
            "https://olimpiada.ru/activity/465": "Информатика",
            "https://olimpiada.ru/activity/5283": "Информатика"
        }

        subject = subjects[url]
        olymp = olymps[url]

        tree = html.fromstring(data.text)
        eventsTable = tree.xpath('//table[@class = "events_for_activity"]')[0]
        dates = eventsTable.xpath('.//tbody')[0]
        actualDates = dates.xpath('.//tr[@class = "notgreyclass"]')

        if len(actualDates) == 0:
            return ((-1, -1), (-1, -1), olymp, subject, "")

        event = actualDates[0]\
            .xpath('.//td[@colspan = "2"]')[0]\
                .xpath('.//a')[0]\
                    .xpath('.//div[@class = "event_name"]')[0]\
                        .text
        date = actualDates[0]\
            .xpath('.//td[@colspan = "1"]')[0]\
                .xpath('.//a')[0]\
                    .text\
                        .lower()
        a = list(map(lambda x: x.split('...'), date.split()))
        b = []

        months = {
            "янв" : 1,
            "фев" : 2,
            "мар" : 3,
            'апр' : 4,
            'мая' : 5,
            'июн' : 6,
            'июл' : 7,
            'авг' : 8,
            'сен' : 9,
            'окт' : 10,
            'ноя' : 11,
            'дек' : 12
        }

        for i in a:
            for j in i:
                if j.lower() == 'до':
                    b.append(j)
                elif len(j) == 3:
                    b.append(months[j.lower()])
                else:
                    b.append(int(j))


        startDay = startMonth = endDay = endMonth = 0

        if len(b) == 2: #single date
            startDay = endDay = b[0]
            startMonth = endMonth = b[1]

        elif len(b) == 3:
            if b[0] == 'до':
                startDay = startMonth = -1
                endDay = b[1]
                endMonth = b[2]
            else:
                startMonth = endMonth = b[2]
                startDay = b[0]
                endDay = b[1]
        elif len(b) == 4:
            startDay = b[0]
            startMonth = b[1]
            endDay = b[2]
            endMonth = b[3]

        return ((startDay, startMonth), (endDay, endMonth), olymp, subject, event)

if __name__ == "__main__":
    cl = EventGetter()

    print(cl.getEvent("https://olimpiada.ru/activity/80"))
    print(cl.getEvent("https://olimpiada.ru/activity/153"))