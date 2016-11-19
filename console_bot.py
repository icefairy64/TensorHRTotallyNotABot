import business_logic as bl


def send(id, text, keyboard):
    print(text)
    answer = raw_input()
    bl.handle_incoming_message('1', answer, False, send)

send('1', '/start', [])
