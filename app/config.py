''' This file is used to load the config.toml file and return it as a dictionary. '''
import os
import toml

def _load_config():
    ''' This function loads the config.toml file and returns it as a dictionary. '''
    return toml.load("config.toml")

def set_enviroment_variables():
    ''' This function sets all the environment variables. '''
    config = _load_config()
    os.environ["OPENAI_API_KEY"] = config["keys"]["OPENAI_API_KEY"]
    os.environ["REDIS_URL"] = config["urls"]["REDIS_URL"]
