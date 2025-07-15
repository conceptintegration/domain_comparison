#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2025, Roy Gardner and Sally Gardner'


"""
"""

from packages import *
from nlp import *
from semantic import *


def process(config):
    # Encoder
    encoder = hub.load(config['nlp']['encoder_path'] + config['nlp']['encoder'])
    model_path = config['ontologies']['model_path']

    print('Loading segment encodings…')
    with open(config['constitutions']['model_path'] + 'segment_encodings.json', 'r', encoding='utf-8') as f:
        segment_encodings = json.load(f)
        f.close() 

    ontology_dict = {}
    for file in config['ontologies']['ontology_files']:
        ont_label = file.split('/')[0]
        ontology_dict[ont_label] = {}

        with open(config['ontologies']['path'] + file, encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            # Get the header row
            ontology_dict[ont_label]['header'] = next(reader)
            # Put the remaining rows into a list of lists
            ontology_dict[ont_label]['topics'] = [row for row in reader]


    for ont_label,ont_data in ontology_dict.items():
        topics_dict = {}
        topics_data = ont_data['topics']
        topics_header = ont_data['header']
        for i,row in enumerate(topics_data):
            topic_id = str(row[topics_header.index('key')]).strip()
            label = str(row[topics_header.index('label')]).strip()
            description = str(row[topics_header.index('description')]).strip()
            topics_dict[topic_id] = {}
            topics_dict[topic_id]['label'] = label
            topics_dict[topic_id]['description'] = description
            topics_dict[topic_id]['encoded_text'] = label + '. ' + description

        print('Serialising topics for ' + ont_label + '…',len(topics_dict))
        filename = model_path + ont_label + '_topics_dict.json'
        with open(filename, 'w') as f:
            json.dump(topics_dict, f)
            f.close()
        topic_encodings = encode_topics(ont_label,topics_dict,model_path,encoder,split_size=2)
        build_topic_segments_matrix(ont_label,topic_encodings,segment_encodings,model_path)
        print()

    print('Finished processing ontologies')
