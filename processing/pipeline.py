#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2025, Roy Gardner and Sally Gardner'


"""

Takes a reference corpus (in our case CCP) and some ontologies.

For each ontology generates a topic-segment similarity matrix.

"""
from packages import *
from nlp import *

import process_sections
import process_ontologies

def main(config):

    #config['constitutions']['function'].process(config)
    config['ontologies']['function'].process(config)


if __name__ == '__main__':

    # Data processing configurations
    config = {}
    config['nlp'] = {}
    config['nlp']['encoder_path'] = '../'
    config['nlp']['encoder'] = 'use_ml_3'

    config['constitutions'] = {} 
    config['constitutions']['function'] = process_sections
    config['constitutions']['model_path'] = '../model/'
    config['constitutions']['path'] = '../data/constitutions/constitutions_xml/'
    config['constitutions']['constitutions_list'] = '../data/constitutions/const_list.json'
    # Location of text sections in constitution XML files
    config['constitutions']['element_types'] = ['body','list']

    config['ontologies'] = {} 
    config['ontologies']['function'] = process_ontologies
    config['ontologies']['model_path'] = '../model/'
    config['ontologies']['path'] = '../data/ontologies/'
    config['ontologies']['ontology_files'] = ['CCP-FACET/ontology.csv','IDEA-GLO/ontology.csv','NC-DCC/ontology.csv']

    main(config)
