#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2023-2024, Roy and Sally Gardner'

from packages import *

def popup(text):
    display(Javascript("alert('{}')".format(text)))

def alert(msg):
    from IPython.display import Javascript

    def popup(text):
        display(Javascript("alert('{}')".format(text)))
    popup(msg)

def discovery_interface(choice_dict,ontologies_dict,def_threshold):
    
    import re

    def sanitize_text(text,max_length=16):
        """
        Sanitise and/or truncate topic label or description.
        Returns sanitised text.
        """        
        # Limit length
        text = text[:max_length]
        # Escape HTML
        text = html.escape(text)
        # Remove any remaining problematic characters
        text = re.sub(r'[<>"\']', '',text)
        return text.strip()

    ont_list = []
    for k,v in ontologies_dict.items():
        if v['reference']:
            reference_ontology = k
            reference_ont_label = f'{k}/{v["Name"]}/{v["Organization"]}'
        else:
            ont_list.append(f'{k}/{v["Name"]}/{v["Organization"]}')
    ont_list = sorted(ont_list)
            

    def apply(change):
        choice_dict['threshold'] = threshold_slider.value
        choice_dict['reference'] = reference_ontology
        choice_dict['comparison'] = ont_select.value.split('/')[0].strip()
        choice_dict['export'] = export_checkbox.value
        export_prefix = '' 
        if export_checkbox.value == True:
            export_prefix = export_prefix_text.value
            if len(export_prefix.strip()) == 0 or export_prefix == None:
                alert('Please enter an export file prefix')
                return
        sanitised_prefix = sanitize_text(export_prefix.strip(),max_length=16)
        if sanitised_prefix != export_prefix.strip():
            alert_text = 'The export file prefix was sanitised. Please check the value: ' + sanitised_prefix
            popup(alert_text)
        choice_dict['export_prefix'] = sanitised_prefix 

    ont_select = widgets.Dropdown(
        options=ont_list,
        value=ont_list[0],
        description='Ontology:',
        disabled=False,
        layout=Layout(width='800px')
    )
    
    threshold_slider = widgets.FloatSlider(
        value=def_threshold,
        min=0.58,
        max=0.9,
        step=0.01,
        description='Threshold:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.2f',
        layout=Layout(width='800px')
    )

    export_checkbox = widgets.Checkbox(
        value=False,
        description='Export results',
        disabled=False,
        indent=True    
    )
    export_prefix_text = widgets.Text(
        layout={'width': 'initial'},
        value='',
        placeholder='Enter export file prefix (max 16 characters)',
        description='Export prefix:',
        disabled=False,
        continuous_update=False
    )

    apply_button = widgets.Button(
        description='Apply Choices',
        disabled=False,
        button_style='',
        tooltip='Click to apply choices'
    )
    reference_label = widgets.Label(
        value=f'REFERENCE ONTOLOGY: {reference_ont_label}',
    )
    comparison_label = widgets.Label(
        value='SELECT A COMPARISON ONTOLOGY:',
    )
    threshold_label = widgets.Label(
        value='SET THE SEMANTIC SIMILARITY THRESHOLD:',
    )
    
    display(reference_label)
    display(comparison_label)
    display(ont_select)
    display(threshold_label)
    display(threshold_slider)
    display(export_checkbox)
    display(export_prefix_text)
    display(apply_button)
    

    apply_button.on_click(apply)
    out = widgets.Output()
    display(out)

def init_discovery_choice_dict():
    discovery_choice_dict = {}
    discovery_choice_dict['threshold'] = 0
    discovery_choice_dict['reference'] = ''
    discovery_choice_dict['comparison'] = ''
    discovery_choice_dict['export'] = False
    discovery_choice_dict['export_prefix'] = ''
    return discovery_choice_dict


def initialise(model_path,exclusion_list=[]):
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


