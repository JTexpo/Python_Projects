# Important Imports
import os
# Import Local File
import NeatAI

if __name__ == '__main__':
    # Getting the current directory path
    local_dir = os.path.dirname(__file__)
    # Grabbing the config file for neat-python to know how to build the AI
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    # running the AI
    NeatAI.run(config_path)
