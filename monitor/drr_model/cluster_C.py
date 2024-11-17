from flask import Flask, request
import os
import time

app = Flask(__name__)
DATA_DIR = 'c_data'

os.system(f'rm -rf {DATA_DIR}')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


@app.route('/files', methods=['POST'])
def receive_files():
    files = request.files.getlist('files')

    if not files:
        return "No files received", 400

    first_file_time = float(files[0].filename.split('_')[1].split('.')[0])

    for file in files:
        file_path = os.path.join(DATA_DIR, file.filename)
        file.save(file_path)
        print(f"Received file {file.filename} from B.")

    receive_time = time.time()
    delay = receive_time - first_file_time
    log_delay(delay)

    return "Files received", 200


def log_delay(delay):
    with open(os.path.join(DATA_DIR, 'delay.txt'), 'a') as delay_file:
        delay_file.write(f'{delay}\n')
        delay_file.flush()


if __name__ == '__main__':

    delay_file = open(f'{DATA_DIR}/delay.txt', 'w')
    app.run(host='0.0.0.0', port=7000)
    delay_file.close()
