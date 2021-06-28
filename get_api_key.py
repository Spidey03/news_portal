
import configparser

try:
    config = configparser.ConfigParser(interpolation=None)
    config.read("config/api.ini")
except FileNotFoundError:
    print("Error!: file config/api.ini not found:/n")
except Exception as e:
    print("Error!: {}".format(e))


def get_api_key():
    try:
        api_key = config["API"]["api_key"]
        if api_key == "":
            print("Error!: api key cannot be empty")
            return
        return api_key
    except KeyError:
        print("Error!: Missing api_key field in config/api.ini")
