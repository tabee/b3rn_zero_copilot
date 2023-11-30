''' This file is used to load the config.toml file and return it as a dictionary. '''
import toml

def load_config():
    ''' This function loads the config.toml file and returns it as a dictionary.'''
    config = toml.load("config.toml")
    return config
