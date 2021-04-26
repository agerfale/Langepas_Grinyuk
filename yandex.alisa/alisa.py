from flask import Flask, request
import logging
from flask_ngrok import run_with_ngrok
import json

app = Flask(__name__)
run_with_ngrok(app)
logging.basicConfig(level=logging.INFO)


sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:

        sessionStorage[user_id] = {
            'suggests': [
                "хочу",
                "мультики",
                'ужасы',
                'драма',
                'детектив',
                'комедия',
                'боевик',
                'триллер',
                'мелодрама',
                'турецкие сериалы',
            ]
        }
        res['response']['text'] = 'Привет! Хочешь посмотреть фильм?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'да, хочу скрасить свой вечер просмотром великолепных картин!',
        'с удовольствием',
        'ок',
        'хочу',
    ]:
        res['response']['text'] = 'Какой жанр? Может ужасы или драму? Или тебе нравятся детективы или мелодрамы? ' \
                                  'Или может быть турецкие сериалы? Что думаешь о том, чтобы посмотреть мультики ' \
                                  'или комедию? А может быть ты фанат триллеров и боевиков?'

        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() in [
        'ужасы',
        'Ужасы'
    ]:
        res['response']['text'] = \
            f"хорошая идея посмотреть {req['request']['original_utterance']}, но советую тебе решить вариант" \
            f" ЕГЭ по физике!"
        res['response']['buttons'] = get_suggests(user_id)

    if req['request']['original_utterance'].lower() in [
        'я уже решила',
        'я уже решил',
        'Я уже решила',
        'Я уже решил',
        'Не хочу',
        'не хочу'
    ]:
        res['response']['text'] = \
            f"Тогда давай помогу выбрать. Ты любишь старые или новые хорроры?"
        res['response']['buttons'] = get_suggests(user_id)

    if req['request']['original_utterance'].lower() in [
        'Старые',
        'старые'
    ]:
        res['response']['text'] = \
            f"{req['request']['original_utterance']} фильмы? Хорошо! Советую посмотреть: Сияние, Оно, " \
            f"Мизери, Криминальная россия!"
        res['response']['buttons'] = get_suggests(user_id)
    elif req['request']['original_utterance'].lower() in [
        'Новые',
        'новые'
    ]:
        res['response']['text'] = \
            f"{req['request']['original_utterance']} фильмы? Хорошо! Советую посмотреть: Я иду искать," \
            f" Астрал, Астрал: Последний ключ "

    elif req['request']['original_utterance'].lower() in [
        'Комедия',
        'комедия'
    ]:
        res['response']['text'] = \
            f" {req['request']['original_utterance']}? Отличный выбор! Советую посмотреть следующие картины: " \
            f"Реальные упыри, Реальные пацаны, Семейка Аддамс."
        res['response']['buttons'] = get_suggests(user_id)
        res['response']['buttons'] = get_suggests(user_id)
        return

    elif req['request']['original_utterance'].lower() in [
        'Драма',
        'драма'
    ]:
        res['response']['text'] = \
            f" {req['request']['original_utterance']}? Может лучше что-то весёлое...?"
        res['response']['buttons'] = get_suggests(user_id)

    if req['request']['original_utterance'].lower() in [
        'Не хочу',
        'не хочу'

    ]:
        res['response']['text'] = \
            f"Надеюсь вы не грустите...Советую посмотреть следующие фильмы: Мальчик в полосатой пижаме, Искупление, " \
            f"Общество мёртвых поэтов, 1 + 1."
        res['response']['buttons'] = get_suggests(user_id)

    elif req['request']['original_utterance'].lower() in [
        'Турецкие сериалы',
        'турецкие сериалы'
    ]:
        res['response']['text'] = \
            f" {req['request']['original_utterance']} ПРЕКРАСНЫЙ ВЫБОР!!!! МНЕ НЕ ПОСЛЫШАЛОСЬ? Тогда вот вам мои " \
            f"любимые: Чёрная любовь, Любовь не понимает слов, Постучись в мою дверь, Великолепный век, " \
            f"Госпожа Фазилет и её дочери"
        res['response']['buttons'] = get_suggests(user_id)

    elif req['request']['original_utterance'].lower() in [
        'мелодрама',
        'Мелодрама'
    ]:
        res['response']['text'] = \
            f" {req['request']['original_utterance']}? Отлично! Советую вам Сумерки, Багровый пик, Великий Гэтсби!"
        res['response']['buttons'] = get_suggests(user_id)

    elif req['request']['original_utterance'].lower() in [
        'Мультики',
        'мультики'
    ]:
        res['response']['text'] = \
            f" {req['request']['original_utterance']} это прекрасно!! Вот самые лучшие: Наруто, " \
            f"Наруто Чиби: Весна юности Рока Ли, Скуби-ду, Смешарики"
        res['response']['buttons'] = get_suggests(user_id)

    elif req['request']['original_utterance'].lower() in [
            'Детективы',
            'детективы'
    ]:
        res['response']['text'] = \
            f" {req['request']['original_utterance']}? Отличный выбор! А вы предпочитаете современные или ретро-фильмы?"
        res['response']['buttons'] = get_suggests(user_id)

    if req['request']['original_utterance'].lower() in [
        'ретро',
        'Ретро'

    ]:
        res['response']['text'] = \
            f"Тогда советую посмотреть следующие картины: Место встречи изменить нельзя, " \
            f"12 стульев, Профессия – следователь."
        res['response']['buttons'] = get_suggests(user_id)

    if req['request']['original_utterance'].lower() in [
        'современные',
        'Современные'

    ]:
        res['response']['text'] = \
            f"Тогда советую посмотреть следующие картины: Достать ножи, Шерлок, Убийство в Восточном экспрессе."
        res['response']['buttons'] = get_suggests(user_id)

    elif req['request']['original_utterance'].lower() in [
            'боевик',
            'Боевик',
            'триллер',
            'Триллер'
    ]:
        res['response']['text'] = \
            f" {req['request']['original_utterance']}? Круто, а вам нравится Джейсон Стетхем?"
        res['response']['buttons'] = get_suggests(user_id)

    if req['request']['original_utterance'].lower() in [
        'да',
        'Да'

    ]:
        res['response']['text'] = \
            f"Тогда советую посмотреть следующие картины: Перевозчик, Последний рубеж, Гнев человеческий."
        res['response']['buttons'] = get_suggests(user_id)

    if req['request']['original_utterance'].lower() in [
        'нет',
        'Нет',

    ]:
        res['response']['text'] = \
            f"Тогда советую посмотреть Форсаж, Довод, Лига Справедливости."
        res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][2:]
    sessionStorage[user_id] = session

    return suggests


if __name__ == '__main__':
    app.run()
