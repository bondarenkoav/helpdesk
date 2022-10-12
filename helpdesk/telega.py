import requests

# telegram url
url = "https://api.telegram.org/bot1730861248:AAH4B5r3YKhzONijjLKEyy8zIJleuO3Nk7s"
# 1730861248:AAH4B5r3YKhzONijjLKEyy8zIJleuO3Nk7s


def send_mess(text):
    params = {'chat_id': -1001422493774, 'text': text}
    response = requests.post(url + '/sendMessage', data=params)
    return response


# send_mess(result_you_want_to_send)
