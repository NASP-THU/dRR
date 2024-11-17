import os
import requests
from flask import Flask, request
import threading

app = Flask(__name__)
DATA_DIR = 'b_data'

a_machine = {number1: A1_IP,
             number2: A2_IP,
             number3: A3_IP,
             number4: A4_IP,
             number5: A5_IP
             }

os.system(f'rm -rf {DATA_DIR}')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


@app.route('/sync', methods=['POST'])
def sync_data():
    data = request.json
    machine_id = data.get("machine_id")
    files = data.get("files")
    print(f"B1 received sync request for A{machine_id} with file: {files}.")

    threads = []
    for file_name in files:
        thread = threading.Thread(target=fetch_and_save_file, args=(machine_id, file_name))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return "Sync Data Successful", 200


def fetch_and_save_file(machine_id, file_name):
    print(f"Fetching {file_name} from A{machine_id}")
    response = requests.get(f'http://{a_machine[machine_id]}:5000/files/{file_name}')
    if response.status_code == 200:
        save_file(response.content, file_name)
    else:
        print(f"Failed to retrieve data from A{machine_id} for file {file_name}")


def save_file(file_content, file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, 'wb') as f:
        f.write(file_content)
    print(f"B1 saved file {file_name}.")

    thread = threading.Thread(target=send_file_to_c, args=([file_name],))
    thread.start()


def send_file_to_c(file_names):
    c_ips = [C_machine_IPs ......]
    c_machines = [f'http://{ip}:7000/files' for ip in c_ips]

    files = []
    for file_name in file_names:
        file_path = os.path.join(DATA_DIR, file_name)
        with open(file_path, 'rb') as f:
            files.append((file_name, f.read()))

    def send_file(c_url, file_data):
        try:
            response = requests.post(c_url, files=[('files', (file_data[0], file_data[1], 'application/octet-stream'))])
            if response.status_code == 200:
                print(f"Successfully sent file to {c_url}")
            else:
                print(f"Failed to send file to {c_url}: Status Code {response.status_code}")
        except Exception as e:
            print(f"Error sending file to {c_url}: {e}")

    threads = []
    for c_url in c_machines:
        for file_data in files:
            thread = threading.Thread(target=send_file, args=(c_url, file_data))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
