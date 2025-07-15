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

import process_sections
import process_ontologies

def main(config):

    segments_dict,segment_encodings,encoded_segments,sat_segments_dict = config['constitutions']['function'].process(config)
    model_path = config['constitutions']['model_path']
    model_filename = model_path + 'segments_dict.json'
    with open(model_filename, 'w') as f:
        json.dump(segments_dict, f)
        f.close()
    model_filename = model_path + 'segment_encodings.json'
    with open(model_filename, 'w') as f:
        json.dump(segment_encodings, f)
        f.close()
    model_filename = model_path + 'encoded_segments.json'
    with open(model_filename, 'w') as f:
        json.dump(encoded_segments, f)
        f.close()
    model_filename = model_path + 'sat_segments_dict.json'
    with open(model_filename, 'w') as f:
        json.dump(sat_segments_dict, f)
        f.close()
    print('Finished processing constitutions')


    #config['ontologies']['function'].process(config)


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
    # Location of our text sections in constitution XML files
    config['constitutions']['element_types'] = ['body','list']

    config['ontologies'] = {} 
    config['ontologies']['function'] = process_ontologies
    config['ontologies']['model_path'] = '../model/'
    config['ontologies']['path'] = '../data/ontologies/'
    config['ontologies']['reference_ontology'] = ['CCP-FACET']
    config['ontologies']['ontology_files'] = ['CCP-FACET/ontology.csv','IDEA-GLO/ontology.csv','NC-DCC/ontology.csv']
    config['ontologies']['fields'] = ['key','label','description']

    main(config)
