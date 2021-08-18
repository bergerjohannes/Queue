def get_name_for_civ(index):
        civs = ['Britons', 'Franks', 'Goths', 'Teutons', 'Japanese', 'Chinese', 'Byzantines', 'Persians', 'Saracens',
            'Turks', 'Vikings', 'Mongols', 'Celts', 'Spanish', 'Aztecs', 'Mayans', 'Huns', 'Koreans', 'Italians',
            'Indians', 'Incas', 'Magyars', 'Slavs', 'Portuguese', 'Ethiopians', 'Malians', 'Berbers', 'Khmer', 'Malay',
            'Burmese', 'Vietnamese', 'Bulgarians', 'Tatars', 'Cumans', 'Lithuanians', 'Burgandians', 'Sicilians', 'Poles', 'Bohemians']
        return civs[index - 1]

# Only possible for EN & DE translations at the moment
# ToDo: add additional translations
def chat_indicates_age_up(message, player_name):
        if ' advanced to the ' in message or 'zeit vorangeschritten.' in message:
                if (' ' + player_name + ' advanced to the Feudal Age.' in message) or (' ' + player_name + ' ist zur Feudalzeit vorangeschritten.' in message):
                        return True
                if (' ' + player_name + ' advanced to the Castle Age.' in message) or (' ' + player_name + ' ist zur Ritterzeit vorangeschritten.' in message):
                        return True
                if (' ' + player_name + ' advanced to the Imperial Age.' in message) or (' ' + player_name + ' ist zur Imperialzeit vorangeschritten.' in message):
                        return True
        return False