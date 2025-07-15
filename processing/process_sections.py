#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2025, Roy Gardner and Sally Gardner'

"""

Generates segment data including SATs:

- segments_dict.json
- segment_encodings.json
- encoded_segments.json

This process DOES NOT segment constitution sections. Therefore, segment refers to a complete constitution section.

"""

from packages import *

def process(config):

    encoder = hub.load(config['nlp']['encoder_path'] + config['nlp']['encoder'])
    error_list = []

    # Use only in-force constitutions
    with open(config['constitutions']['constitutions_list'], 'r') as f:
        const_list = json.load(f)
        f.close() 
    # Build dictionary of in-force constitutions
    const_dict = {d['id']:d for d in const_list if d['in_force'] == True}

    # Key is a segment identifier, value is a text segment
    segments_dict = {}
    sat_segments_dict = {}

    xml_dir = config['constitutions']['path']
    _, _, files = next(os.walk(xml_dir))
    files = [f for f in files if not f[0] == '.']
    for i, file in enumerate(files):

        sys.stdout.write("\r" + str(i))
        sys.stdout.flush()

        constitution_id = os.path.splitext(file)[0]
        if not constitution_id in const_dict:
            continue

        xml_file = xml_dir + file
        tree = etree.parse(xml_file)

        results = []
        for type_ in config['constitutions']['element_types']:
            search_str = ".//*[@type='" + type_ + "']"
            results.extend(tree.findall(search_str))


        for elem in results:
            # Get the section ID which we are calling the segment_id because of data model conventions
            segment_id = constitution_id + '/' + elem.get('uri').split('/')[1]

            # Content contains the text
            content = elem.findall('content')
            if len(content) > 0:
                for content_elem in content:
                    if 'en' in content_elem.values():
                        text = content_elem.text
                        if text == None:
                            error_list.append((constitution_id,elem.get('uri').split('/')[1],'None'))
                            continue
                        if not type(text) == str:
                            error_list.append((constitution_id,elem.get('uri').split('/')[1],'Not a string'))
                            continue
                        else:
                            text = html.unescape(text)
                        if len(text.strip()) == 0:
                            error_list.append((constitution_id,elem.get('uri').split('/')[1],'Empty'))
                            continue
                        
                        segments_dict[segment_id] = {}
                        segments_dict[segment_id]['text'] = text.strip()


        # Process SAT
        for elem in results:
            segment_id = constitution_id + '/' + elem.get('uri').split('/')[1]
            metadata = elem.findall('metadata')
            if len(metadata) > 0:
            # Section may have topics
                metadata_elem = elem.findall('metadata')
                topics_elem = metadata_elem[0].findall('topics')
                if len(topics_elem) > 0:
                    # Check that we don't already have the topic we are adding
                    # Compile existing topics for the element
                    for topic_elem in topics_elem:
                        for topic in topic_elem:
                            topic_id = topic.text.split('/')[-1]
                            if topic_id in sat_segments_dict:
                                sat_segments_dict[topic_id].append(segment_id)
                            else:
                                sat_segments_dict[topic_id] = [segment_id]

        if i == 2:
            break

    sys.stdout.write("\r")
    sys.stdout.flush()

    # Write errors to disk
    model_filename = './error_list.json'
    with open(model_filename, 'w') as outfile:
        json.dump(error_list, outfile)
        outfile.close() 

    encoded_segments = [k for k in segments_dict.keys()]
    segments_text_list = [v['text'] for _,v in segments_dict.items()]

    print('Encoding:',len(segments_text_list))

    indices = list(range(0,len(segments_text_list)))
    split_list = np.array_split(indices,100)
    print('Split list')
    segment_encodings = []
    print('Starting split loop…')
    for i,l in enumerate(split_list):
        #print('Encoding',str(i + 1),'of 100')
        split = [segments_text_list[index] for index in list(l)]
        encodings = encoder(split)
        assert(len(encodings) == len(split))
        segment_encodings.extend(np.array(encodings).tolist())
    print('Finished split loop')
        
    return segments_dict,segment_encodings,encoded_segments,sat_segments_dict

