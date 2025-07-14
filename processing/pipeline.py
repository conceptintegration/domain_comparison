#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2025, Roy Gardner and Sally Gardner'


"""
Currently working with data model with segments encoded by USE_ML_3.

Takes a reference corpus (in our case CCP) and some ontologies.

For each ontology generates a topic-segment similarity matrix.

"""
from packages import *
from nlp import *

import process_ontologies

def main(config):

    for config_name,config_values in config.items():
        if config_values['run'] == True:
            print()
            print(config_name)
            config_values['function'].process(config_values)

if __name__ == '__main__':

    # Data processing configurations
    config = {}
    config['ccp_reference'] = {} 
    config['ccp_reference']['run'] = True
    config['ccp_reference']['function'] = process_ontologies
    config['ccp_reference']['encoder'] = {}
    config['ccp_reference']['encoder']['path'] = '../'
    config['ccp_reference']['encoder']['model'] = 'use_ml_3'
    config['ccp_reference']['model_path'] = '../model/'
    config['ccp_reference']['data_path'] = '../data/'
    config['ccp_reference']['ontology_files'] = ['CCP-FACET/ontology.csv','IDEA-GLO/ontology.csv','NC-DCC/ontology.csv']
    config['ccp_reference']['fields'] = ['key','label','description']

    main(config)
