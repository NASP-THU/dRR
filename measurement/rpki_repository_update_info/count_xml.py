import requests
import xml.etree.ElementTree as ET
import time
from get_repository import read_routinator_repo
from datetime import datetime


def fetch_notifications(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_first_delta(xml_data):
    root = ET.fromstring(xml_data)
    delta = root.find('.//{http://www.ripe.net/rpki/rrdp}delta')
    if delta is not None:
        uri = delta.attrib.get('uri')
        serial = delta.attrib.get('serial')
        return serial, uri
    return None, None


def parse_update_uris(xml_data):
    root = ET.fromstring(xml_data)
    update_uris = []

    for publish in root.findall('.//{http://www.ripe.net/rpki/rrdp}publish'):
        publish_uri = publish.attrib.get('uri')
        if publish_uri:
            update_uris.append(publish_uri)

    for withdraw in root.findall('.//{http://www.ripe.net/rpki/rrdp}withdraw'):
        withdraw_uri = withdraw.attrib.get('uri')
        if withdraw_uri:
            update_uris.append(withdraw_uri)

    return update_uris


def main():
    last_serial = dict()

    while True:
        routinator_repo = read_routinator_repo()
        update_uris = []
        update_uris_roa = []
        for url in routinator_repo:
            try:
                xml_data = fetch_notifications(url)
                serial, uri = parse_first_delta(xml_data)

                if url not in last_serial.keys():
                    last_serial[url] = None

                if serial is not None and (last_serial[url] is None or int(serial) > int(last_serial[url])):
                    last_serial[url] = serial
                    update_data = fetch_notifications(uri)
                    temp_update_uris = parse_update_uris(update_data)
                    for update_uri in temp_update_uris:
                        if update_uri[-4:] == '.roa':
                            update_uris_roa.append(update_uri)
                        update_uris.append(update_uri)

            except Exception as e:
                pass

        only_roa.write(f"{','.join(update_uris_roa)}\n")
        only_roa.write(f'{len(update_uris_roa)}\n')
        only_roa.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        only_roa.flush()

        all_cert.write(f"{','.join(update_uris)}\n")
        all_cert.write(f'{len(update_uris)}\n')
        all_cert.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        all_cert.flush()

        time.sleep(60)


if __name__ == '__main__':

    only_roa = open('data/repo_roa.txt', 'w')
    all_cert = open('data/update_cert.txt', 'w')

    main()

    only_roa.close()
    all_cert.close()
