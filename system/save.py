from configparser import ConfigParser


# Сохранение игрового процесса
def save_game_progress(player=None, man=None):
    if player is not None:
        player.save_progress()
    if man is not None:
        man.save_progress()


def save_new_player(player):
    config = ConfigParser()
    config.read('./data/save.ini', encoding='utf8')
    section = 'section_player'
    keys = ['gender', 'gender_partner', 'age', 'characters', 'characters_partner', 'happiness_value',
            'wealth_value', 'compatibility_value', 'character_value', 'money']
    for key in keys:
        player.setdefault(key, 'null')
        config.set(section, key, player[key])

    with open('./data/save.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)


# Получение громкости из сохранения
def get_volume_from_save():
    config = ConfigParser()
    config.read('./data/save.ini', encoding='utf8')
    section = 'section_settings'
    return config.getfloat(section, 'volume')


# Функция сохранения настроек
def save_settings(**settings):
    config = ConfigParser()
    config.read('./data/save.ini', encoding='utf8')
    section = 'section_settings'
    for setting, value in settings.items():
        config.set(section, setting, str(value))

    with open('./data/save.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)


# Функция рестарта игры
def restart_game():
    config = ConfigParser()
    config.read('./data/save.ini', encoding='utf8')
    section = 'section_man'
    keys = ['gender', 'age', 'name', 'characters', 'job', 'property', 'happiness_value', 'wealth_value',
            'compatibility_value', 'character_value', 'body', 'face', 'hair', 'pants']

    for key in keys:
        config.set(section, key, 'null')

    section = 'section_player'
    keys = ['gender', 'gender_partner', 'age', 'characters', 'characters_partner', 'happiness_value',
            'wealth_value', 'compatibility_value', 'character_value', 'money']

    for key in keys:
        config.set(section, key, 'null')

    with open('./data/save.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)


def restart_player():
    config = ConfigParser()
    config.read('./data/save.ini', encoding='utf8')
    section = 'section_player'
    keys = ['happiness_value', 'wealth_value', 'compatibility_value', 'character_value', 'money']
    for key in keys:
        config.set(section, key, 'null')

    section = 'section_man'
    keys = ['gender', 'age', 'name', 'characters', 'job', 'property', 'happiness_value', 'wealth_value',
            'compatibility_value', 'character_value', 'body', 'face', 'hair', 'pants']

    for key in keys:
        config.set(section, key, 'null')

    with open('./data/save.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)


def check_null_in_save():
    config = ConfigParser()
    config.read('./data/save.ini', encoding='utf8')
    section = 'section_man'
    keys = ['gender', 'age', 'name', 'characters', 'job', 'property', 'happiness_value', 'wealth_value',
            'compatibility_value', 'character_value', 'body', 'face', 'hair', 'pants']
    values_man = {config.get(section, key) for key in keys}

    section = 'section_player'
    keys = ['gender', 'gender_partner', 'age', 'characters', 'characters_partner', 'happiness_value',
            'wealth_value', 'compatibility_value', 'character_value', 'money']
    values_player = {config.get(section, key) for key in keys}

    return values_man == values_player == {'null'}
