from flask import Flask, request, send_file
import os
import time
import random
import threading
import requests

app = Flask(__name__)
DATA_DIR = 'data'

os.system(f'rm -rf {DATA_DIR}')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

roa_file = open('xxx.roa', 'rb')
roa_content = roa_file.read()
roa_file.close()


def generate_data(machine_id):
    while True:
        num_files = random.randint(1, 10)
        files = []
        for _ in range(num_files):
            file_name = f"A{machine_id}_{time.time()}.txt"
            file_path = os.path.join(DATA_DIR, file_name)
            with open(file_path, 'wb') as f:
                f.write(roa_content)
            print(f"A{machine_id} updated data: {file_name}.")
            files.append(file_name)

        if machine_id == 1:
            notify_b(machine_id, files)
        else:
            notify_a1(machine_id, files)

        time.sleep(10)


def notify_a1(updated_machine_id, files):
    a1_url = 'http://machine_A1:5000/notifications'
    requests.post(a1_url, json={"updated_machine": updated_machine_id, "files": files})


@app.route('/notifications', methods=['POST'])
def receive_notification():
    data = request.json
    updated_machine = data.get("updated_machine")
    files = data.get("files")
    print(f"A1 received notification from A{updated_machine} with file: {files}.")

    notify_b(updated_machine, files)
    return "Notification received", 200


def notify_b(updated_machine, files):
    b_url = 'http://machine_B:6000/sync'
    requests.post(b_url, json={"machine_id": updated_machine, "files": files})


@app.route('/files/<filename>', methods=['GET'])
def send_file_route(filename):
    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    return "File not found!", 404


if __name__ == '__main__':
    threading.Thread(target=generate_data, args=(machine_id,)).start()
    app.run(host='0.0.0.0', port=5000)
