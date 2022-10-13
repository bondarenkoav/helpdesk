import requests

# telegram url
url = ""


def send_mess(text):
    params = {'chat_id': -1001422493774, 'text': text}
    response = requests.post(url + '/sendMessage', data=params)
    return response


# send_mess(result_you_want_to_send)
