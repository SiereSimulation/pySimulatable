import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import EnvironmentLoader
import json

def test_environment_loader_ctor():
    env = EnvironmentLoader.EnvironmentLoader()

def test_environment_loader_load():
    env = EnvironmentLoader.EnvironmentLoader()
    # json.
    env.load("example-env.json")