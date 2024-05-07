from flask import Flask, request, render_template
import requests
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        access_tokens = request.files.getlist('accessToken')
        thread_id = request.form.get('threadId')
        sender_name = request.form.get('senderName')
        message_file = request.files['txtFile']
        time_interval = int(request.form.get('time'))

        messages = message_file.read().decode().splitlines()

        for access_token in access_tokens:
            for message in messages:
                try:
                    api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                    full_message = f'{sender_name} {message}'
                    parameters = {'access_token': access_token, 'message': full_message}
                    response = requests.post(api_url, data=parameters)
                    if response.status_code == 200:
                        print(f"Message sent using token {access_token.filename}: {full_message}")
                    else:
                        print(f"Failed to send message using token {access_token.filename}: {full_message}")
                    time.sleep(time_interval)
                except Exception as e:
                    print(f"Error while sending message using token {access_token.filename}: {full_message}")
                    print(e)
                    time.sleep(30)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
