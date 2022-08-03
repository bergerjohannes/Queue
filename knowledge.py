def get_name_for_civ(index):
        civs = ['Britons', 'Franks', 'Goths', 'Teutons', 'Japanese', 'Chinese', 'Byzantines', 'Persians', 'Saracens',
            'Turks', 'Vikings', 'Mongols', 'Celts', 'Spanish', 'Aztecs', 'Mayans', 'Huns', 'Koreans', 'Italians',
            'Hindustanis', 'Incas', 'Magyars', 'Slavs', 'Portuguese', 'Ethiopians', 'Malians', 'Berbers', 'Khmer', 'Malay',
            'Burmese', 'Vietnamese', 'Bulgarians', 'Tatars', 'Cumans', 'Lithuanians', 'Burgandians', 'Sicilians', 'Poles', 'Bohemians', 'Dravidians', 'Bengalis', 'Gurjaras']
        return civs[index - 1]

# Supporting all localizations that are available as of September 2021: BR, DE, EN ES, FR, HI, IT, JP, KO, MS, MX, PL, RU, TR, TW, VI, ZH
def chat_indicates_age_up(message, player_name):
        age_up_chat_texts = [' avançou para a Idade Feudal.', ' avançou para a Idade dos Castelos.', ' avançou para a Idade Imperial.',
        ' ist zur Feudalzeit vorangeschritten.', ' ist zur Ritterzeit vorangeschritten.', ' ist zur Imperialzeit vorangeschritten.',
        ' advanced to the Feudal Age.', ' advanced to the Castle Age.', ' advanced to the Imperial Age.',
        ' avanzó a la Edad Feudal.', ' avanzó a la Edad de los Castillos.', ' avanzó a la Edad Imperial.',
        " a progressé vers l'âge féodal.", " a progressé vers l'âge des châteaux.", " a progressé vers l'âge impérial.",
        ' सामंतवादी युग में उन्नत है।', ' परिवर्तन युग में उन्नत है।', ' साम्राज्यवादी युग में उन्नत है।',
        " passaggio all'età feudale.", " passaggio  all'età dei castelli.", " passaggio all'età imperiale.",
        ' が領主の時代に進化しました。', ' が城主の時代に進化しました。', ' が帝王の時代に進化しました。',
        ' 님이 봉건 시대로 발전했습니다.', ' 님이 성주 시대로 발전했습니다.', ' 님이 왕정 시대로 발전했습니다.',
        ' telah mara ke Zaman Feudal.', ' telah mara ke Zaman Kastil.', ' telah mara ke Zaman Empayar.',
        ' avanzó a la Edad Feudal.', ' avanzó a la Edad de los Castillos.', ' avanzó a la Edad Imperial.',
        ' wkroczyło w Erę Feudalną.', ' wkroczyło w Erę Zamków.', ' wkroczyło w Erę Imperiów.',
        ' — переход в феодальную эпоху.', ' — переход в замковую эпоху.', ' — переход в имперскую эпоху.',
        ", Feodal Çağ'a geçti.", ", Kale Çağı'na geçti.", ", İmparatorluk Çağı'na geçti.",
        ' 升級至封建時代。', ' 升級至城堡時代。', ' 升級至帝王時代',
        ' đã phát triển lên Thời phong kiến.', ' đã phát triển lên Thời lâu đài.', ' đã phát triển lên Thời đế quốc.',
        ' 升级至封建时代。', ' 升级至城堡时代。', ' 升级至帝王时代']

        for string in age_up_chat_texts:
                if ' ' + player_name + string in message:
                        return True
        return False