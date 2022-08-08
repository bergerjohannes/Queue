from constants import *

def get_name_for_civ(index):
        civs = ['Britons', 'Franks', 'Goths', 'Teutons', 'Japanese', 'Chinese', 'Byzantines', 'Persians', 'Saracens',
            'Turks', 'Vikings', 'Mongols', 'Celts', 'Spanish', 'Aztecs', 'Mayans', 'Huns', 'Koreans', 'Italians',
            'Hindustanis', 'Incas', 'Magyars', 'Slavs', 'Portuguese', 'Ethiopians', 'Malians', 'Berbers', 'Khmer', 'Malay',
            'Burmese', 'Vietnamese', 'Bulgarians', 'Tatars', 'Cumans', 'Lithuanians', 'Burgandians', 'Sicilians', 'Poles', 'Bohemians', 'Dravidians', 'Bengalis', 'Gurjaras']
        return civs[index - 1]

def get_color(index):
        colors = ['Blue', 'Red', 'Green', 'Yellow', 'Cyan', 'Pink', 'Grey', 'Orange']
        return colors[index]

# Supporting all localizations that are available as of September 2021: BR, DE, EN ES, FR, HI, IT, JP, KO, MS, MX, PL, RU, TR, TW, VI, ZH
def chat_indicates_age_up(message, player_name):
        age_up_chat_texts_feudal_age = [" avançou para a Idade Feudal.", 
        " ist zur Feudalzeit vorangeschritten.",
        " advanced to the Feudal Age.",
        " avanzó a la Edad Feudal.",
        " a progressé vers l'âge féodal.",
        " सामंतवादी युग में उन्नत है।",
        " passaggio all'età feudale.",
        " が領主の時代に進化しました。",
        " 님이 봉건 시대로 발전했습니다.",
        " telah mara ke Zaman Feudal.",
        " avanzó a la Edad Feudal.",
        " wkroczyło w Erę Feudalną.",
        " — переход в феодальную эпоху.",
        ", Feodal Çağ'a geçti.",
        " 升級至封建時代。",
        " đã phát triển lên Thời phong kiến.",
        " 升级至封建时代。"]

        age_up_chat_texts_castle_age = [" avançou para a Idade dos Castelos.",
        " ist zur Ritterzeit vorangeschritten.",
        " advanced to the Castle Age.",
        " avanzó a la Edad de los Castillos.",
        " a progressé vers l'âge des châteaux.",
        " परिवर्तन युग में उन्नत है।",
        " passaggio  all'età dei castelli.",
        " が城主の時代に進化しました。",
        " 님이 성주 시대로 발전했습니다.",
        " telah mara ke Zaman Kastil.",
        " avanzó a la Edad de los Castillos.",
        " wkroczyło w Erę Zamków.",
        " — переход в замковую эпоху.",
        ", Kale Çağı'na geçti.",
        " 升級至城堡時代。",
        " đã phát triển lên Thời lâu đài.",
        " 升级至城堡时代。"]

        age_up_chat_texts_imperial_age = [" avançou para a Idade Imperial.",
        " ist zur Imperialzeit vorangeschritten.",
        " advanced to the Imperial Age.",
        " avanzó a la Edad Imperial.",
        " a progressé vers l'âge impérial.",
        " साम्राज्यवादी युग में उन्नत है।",
        " passaggio all'età imperiale.",
        " が帝王の時代に進化しました。",
        " 님이 왕정 시대로 발전했습니다.",
        " telah mara ke Zaman Empayar.",
        " avanzó a la Edad Imperial.",
        " wkroczyło w Erę Imperiów.",
        " — переход в имперскую эпоху.",
        ", İmparatorluk Çağı'na geçti.",
        " 升級至帝王時代",
        " đã phát triển lên Thời đế quốc.",
        " 升级至帝王时代"]

        for string in age_up_chat_texts_feudal_age:
                if ' ' + player_name + string in message:
                        return FEUDAL
        for string in age_up_chat_texts_castle_age:
                if ' ' + player_name + string in message:
                        return CASTLE
        for string in age_up_chat_texts_imperial_age:
                if ' ' + player_name + string in message:
                        return IMPERIAL

        return NO_AGE_UP