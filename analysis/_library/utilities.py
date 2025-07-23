#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2023-2024, Roy and Sally Gardner'

from packages import *

def initialise(exclusion_list=[]):
    model_path = '../model/'
    print('Initialisation started…')

    model_dict = do_load(model_path,exclusion_list=exclusion_list,verbose=False)

    print('Finished initialisation.')
    return model_dict

def do_load(model_path,exclusion_list=[],verbose=True):
    if verbose:
        print('Loading model…')
    model_dict = {}

    _, _, files = next(os.walk(model_path))
    files = [f for f in files if f.endswith('.json') and not f in exclusion_list]
    for file in files:
        model_name = os.path.splitext(file)[0]
        with open(model_path + file, 'r', encoding='utf-8') as f:
            model_dict[model_name] = json.load(f)
            f.close() 

    if verbose:
        print('Finished loading model.')
    return model_dict


