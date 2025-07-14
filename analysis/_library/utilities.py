#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2023-2024, Roy and Sally Gardner'

from packages import *

def initialise(exclusion_list=[]):
    model_path = '../model/'
    use_path = '../use-4/'
    encoder = hub.load(use_path)
    print('Initialisation started…')

    model_dict = do_load(model_path,exclusion_list=exclusion_list,verbose=False)

    print('Finished initialisation.')
    return encoder,model_dict


def popup(text):
    display(Javascript("alert('{}')".format(text)))


def generate_corpus_interface(choice_dict,model_dict,def_search_threshold,def_cluster_threshold):

    def apply(change):
        choice_dict['search_threshold'] = search_slider.value
        choice_dict['cluster_threshold'] = cluster_slider.value
        topic = topic_text.value
        if len(topic.strip()) == 0 or topic == None:
            alert('Please enter topic text')
            return
        choice_dict['topic'] = topic
        choice_dict['export'] = export_checkbox.value
        export_name = '' 
        if export_checkbox.value == True:
            export_name = export_filename.value
            if len(export_name.strip()) == 0 or export_name == None:
                alert('Please enter an export file name')
                return
        choice_dict['export_name'] = export_name 
        if len(choice_dict['topic']) == 0:
            alert('No topic selected.')

    search_slider = widgets.FloatSlider(
        value=def_search_threshold,
        min=0.58,
        max=1.0,
        step=0.01,
        description='Search:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.2f',
        layout=Layout(width='800px')
    )

    cluster_slider = widgets.FloatSlider(
        value=def_cluster_threshold,
        min=0.6,
        max=1.0,
        step=0.01,
        description='Cluster:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.2f',
        layout=Layout(width='800px')
    )

    topic_text = widgets.Textarea(
        layout={'width': 'initial'},
        value='',
        placeholder='Enter topic',
        description='Topic:',
        disabled=False,
        rows=4,
        continuous_update=False
    )
    export_checkbox = widgets.Checkbox(
        value=False,
        description='Export results',
        disabled=False,
        indent=True    
    )
    export_filename = widgets.Text(
        layout={'width': 'initial'},
        value='',
        placeholder='Enter file name',
        description='Export name:',
        disabled=False,
        continuous_update=False
    )

    apply_button = widgets.Button(
        description='Apply Choices',
        disabled=False,
        button_style='',
        tooltip='Click to apply choices'
    )

    print('Set thresholds:')
    display(search_slider)
    display(cluster_slider)
    display(topic_text)
    display(export_checkbox)
    display(export_filename)
    display(apply_button)

    apply_button.on_click(apply)
    out = widgets.Output()
    display(out)

def init_choice_dict():
    choice_dict = {}
    choice_dict['search_threshold'] = 0.62
    choice_dict['cluster_threshold'] = 0.7
    choice_dict['topic'] = ''
    choice_dict['export'] = False
    choice_dict['export_name'] = ''
    return choice_dict

def alert(msg):
    from IPython.display import Javascript

    def popup(text):
        display(Javascript("alert('{}')".format(text)))
    popup(msg)

def get_similarity(v,w):
    """
    Compute inverse of angular distance between to vectors v and w
    """
    return 1 - (np.arccos(1 - cosine(v,w))/np.pi)


def encode_text(text_list, encoder):
    """
    Get a list of encoding vectors for the text segments in text_list
    param text_list: A list of strings containing text to be encoded
    param encoder: The encoder, e.g. USE v4
    return A list of encoding vectors in the same order as text_list
    """
    encodings = encoder(text_list)
    return np.array(encodings).tolist()

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


