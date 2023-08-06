from os import path, walk
import requests
from requests.exceptions import ConnectionError
import json
from cryptography.fernet import Fernet, InvalidToken
from .location import Location
from .track import Track
from .qrcode_detector import is_containing_qr_code
from PIL import Image
import exifread
from datetime import datetime
from .exif_data import *
import base64
from argparse import ArgumentParser


HOST_NAME = 'https://dslr-flask-server.herokuapp.com/api/v1/routes/'


def parse_arguments():
    parser = ArgumentParser(description='Process QR Code encrypted data.')
    parser.add_argument('--qrcode-value', action='store', help='QR Code value')
    parser.add_argument('--qrcode-path', action='store', help='Path of QR Code Image')

    args = parser.parse_args()
    return args


def input_passphrase_and_route_id():
    passphrase = input("Please input your passphrase: ")
    while not passphrase:
        print("Your passphrase is invalid. Please try again.")
        passphrase = input("Please input your passphrase: ")

    route_id = input("Please input your route_id: ")
    while not route_id or len(route_id) != 6:
        print("Your route_id is invalid. Please try again.")
        route_id = input("Please input your route_id: ")

    return passphrase, route_id


def input_folder_path():
    folder_path = input("Please input your folder path: ")
    while not folder_path or not path.isdir(folder_path):
        print("Your folder path is invalid. Please try again.")
        folder_path = input("Please input your folder path: ")
    return folder_path


def fetch_route_data(route_id):
    response = requests.get(HOST_NAME + route_id)
    status_code = response.status_code
    if status_code == 200:
        json_response = json.loads(response.text)
        return status_code, json_response['data']
    else:
        return status_code, None


def get_32_length_key_from_passphrase(passphrase):
    if len(passphrase) == 32:
        return passphrase
    else:
        tmp = passphrase
        key = ''
        while len(key) < 32:
            key += tmp + '-'
            tmp = tmp[::-1]
        return key[:32][::-1]


def decrypt_data(nonce, data):
    fernet = Fernet(base64.b64encode(str.encode(nonce)))
    decrypted_bytes = fernet.decrypt(str.encode(data))
    decrypted_data = decrypted_bytes.decode()
    return decrypted_data


def parse_route_data(route_data):
    tracks = []

    for track in route_data['tracks']:
        print("Start Time: {}".format(track['startTime']))
        print("End Time: {}".format(track['endTime']))
        tracks.append(Track(track['startTime'], track['endTime']))

    for item in route_data['locations']:
        location = Location(item['latitude'], item['longtitude'], item['timestamp'])
        for track in tracks:
            if track.is_in_track(location.timestamp):
                track.locations.append(location)
                break
    
    return tracks


def get_list_images(folder_path):
    list_images = []
    for dir_path, _, files in walk(folder_path):
        for file_name in files:

            try:
                full_path = path.join(dir_path, file_name)
                _ = Image.open(full_path)
                list_images.append(full_path)
            except Exception:
                continue

    return list_images


def find_qr_image_path(list_images):
    for img_path in list_images:
        if is_containing_qr_code(img_path):
            print("Image contains qr_code: {}".format(img_path))
            return img_path
    return None


def find_nearest_location_by_time(img_time, first_location, last_location):
    if last_location is None:
        return first_location

    diff_first = img_time - first_location.timestamp
    diff_last = last_location.timestamp - img_time

    if diff_first <= diff_last:
        return first_location
    else:
        return last_location


def find_image_location(tracks, img_time):
    for track in tracks:
        if track.is_in_track(img_time):

            for idx, first_location in enumerate(track.locations):
                if img_time >= first_location.timestamp:

                    last_location = None

                    if idx + 1 < len(track.locations):
                        last_location = track.locations[idx + 1]

                    return find_nearest_location_by_time(img_time, first_location, last_location)


def find_diff_time(img_path, qr_time):
    with open(img_path, 'rb') as f:
        tags = exifread.process_file(f)
        if "Image DateTime" in tags.keys():
            img_time = datetime.strptime(str(tags['Image DateTime']),"%Y:%m:%d %H:%M:%S")
            return qr_time - img_time
        else:
            print("Cannot read time of QRCode Image.")
            exit()


def write_image_exif_data(img_path, location):
    overwrite_exif_data(img_path, location.latitude, location.longtitude)


def update_images_location(tracks, list_images, diff_time):
    for img_path in list_images:
        with open(img_path, 'rb') as f:
            tags = exifread.process_file(f)

            if "Image DateTime" in tags.keys():

                img_time = datetime.strptime(str(tags['Image DateTime']),"%Y:%m:%d %H:%M:%S")

                print('Finding location for: {} ...'.format(img_path))
                
                img_location = find_image_location(tracks, img_time + diff_time)

                if img_location:
                    write_image_exif_data(img_path, img_location)
                else:
                    print('This image path is not belonged to any track: {}'.format(img_path))

            else:
                print('Cannot read datetime from: {}'.format(img_path))


def get_time_and_nonce_from_qr_data(qr_data):
    qr_data = qr_data.split('.')
    time = datetime.strptime('.'.join(qr_data[:2]), "%Y-%m-%d %H:%M:%S.%f") 
    nonce = '.'.join(qr_data[2:])
    return time, nonce


def process_data(passphrase, route_id, folder_path, qr_encrypted_data, qrcode_path, route_encrypted_data):
    try:
        key = get_32_length_key_from_passphrase(passphrase)

        list_images = get_list_images(folder_path)

        if not qrcode_path:
            qr_image_path = find_qr_image_path(list_images)
        else:
            qr_image_path = qrcode_path

        # input qr data if cannot decrypt qrdata

        qr_data = decrypt_data(key, qr_encrypted_data)
        qr_time, nonce = get_time_and_nonce_from_qr_data(qr_data)

        if qr_image_path:
            diff_time = find_diff_time(qr_image_path, qr_time)

            route_data = json.loads(decrypt_data(nonce, route_encrypted_data))

            tracks = parse_route_data(route_data)
            update_images_location(tracks, list_images, diff_time)
        else:
            print('Cannot detect which image contains QR Code.')
            print('Please use --qrcode-path argument to pass path of QR Code Image.')
            exit()
    except InvalidToken:
        print("PassphraseError: Invalid Passphrase")


def main():
    args =  parse_arguments()
    qr_encrypted_data = args.qrcode_value
    qrcode_path = args.qrcode_path

    if not qr_encrypted_data:
        print('Please inpyt qr code value.')
        exit()

    passphrase, route_id = input_passphrase_and_route_id()
    folder_path = input_folder_path()

    try:
        status_code, route_encrypted_data = fetch_route_data(route_id)

        if status_code == 404:
            print("RouteIdNotFoundError: Route Id is not exist.")
        elif status_code != 200:
            print("ServerError: Cannot fetch data from server.")
        else:
            process_data(passphrase, route_id, folder_path, qr_encrypted_data, qrcode_path, route_encrypted_data)
    except ConnectionError:
        raise ConnectionError('Cannot connect to server. Please check your connection.')
    except Exception:
        print("Unexpected Error. Please try again.")

if __name__ == '__main__':
    main()