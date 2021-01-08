from configparser import ConfigParser


# Сохранение игрового процесса
def save_game_progress(player, man):
    player.save_progress()
    man.save_progress()


# Получение громкости из сохранения
def get_volume_from_save():
    config = ConfigParser()
    config.read('save.ini', encoding='utf8')
    section = 'section_settings'
    return config.getfloat(section, 'volume')


# Функция сохранения настроек
def save_settings(**settings):
    config = ConfigParser()
    config.read('save.ini', encoding='utf8')
    section = 'section_settings'
    for setting, value in settings.items():
        config.set(section, setting, str(value))

    with open('save.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)


# Функция рестарта игры
def restart_game():
    config = ConfigParser()
    config.read('save.ini', encoding='utf8')
    section = 'section_man'
    keys = ['gender', 'age', 'name', 'characters', 'job', 'property', 'happiness_value', 'wealth_value',
            'compatibility_value', 'character_value', 'body', 'face', 'hair', 'pants']

    for key in keys:
        config.set(section, key, 'null')

    section = 'section_player'
    keys = ['gender', 'gender_partner', 'age', 'characters', 'characters_partner', 'happiness_value',
            'wealth_value', 'compatibility_value', 'character_value']

    for key in keys:
        config.set(section, key, 'null')

    with open('save.ini', 'w', encoding='utf8') as configfile:
        config.write(configfile)
