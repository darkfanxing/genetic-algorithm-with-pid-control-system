import yaml


def get_config(file_path):
    with open(file_path, "r") as file_:
        return yaml.safe_load(file_)
