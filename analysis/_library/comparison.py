#!/bin/python
# -*- coding: utf-8 -*-

__author__      = 'Roy Gardner'
__copyright__   = 'Copyright 2025, Roy and Sally Gardner'

"""

Code supporting ontology-corpus comparison

"""
from packages import *
from utilities import *
import urllib


def list_query_results(results,matrix,matrix_dict,model_dict):
    """
    """
    link_prefix = 'https://www.constituteproject.org/constitution/'

    # Start building HTML output
    html_output = ''
    
    html_output += '<div>'
    ont_labels = sorted(list(model_dict['ontologies_dict'].keys()))
    
    for segment_index in results:
        
        html_output += '<div style="border: 1px solid black;"><table style="background-color:pink;">\
                        <tr style="background-color:pink;width=100%;">'
        segment_id = model_dict['encoded_segments'][segment_index]
        document_id = segment_id.split('/')[0]
        segment_number = segment_id.split('/')[1]
        link = link_prefix + document_id +\
                urllib.parse.unquote('#', encoding='utf-8', errors='replace') + 's' + segment_number
        segment_text = model_dict['segments_dict'][segment_id]['text']
        html_output += f'<td style="word-wrap:break-word;text-align:left;"><a href="{link}"\
                        target="_blank">{segment_id}</a></td>'
        html_output += f'<td style="word-wrap:break-word;text-align:left;width:100%;">{segment_text}</td>'
        html_output += '</tr></table>'
        
        html_output += '<table>'
        html_output += f"""<tr>
                <th style="width: 10%;text-align:left;">Ontology</th>
                <th style="width: 8%;text-align:left;">Topic key</th>
                <th style="width: 20%;text-align:left;">Topic label</th>
                <th style="width: 70%;text-align:left;">Topic description</th>
            </tr>"""
        for i,v in enumerate(matrix[:,segment_index]):
            if v == 0:
                continue
            ont_label = ont_labels[i]
            ont_matrix = matrix_dict[ont_label]
            # Recover the topics
            topic_indices = np.nonzero(ont_matrix[:,segment_index])[0]
            topic_ids = [model_dict[f'{ont_label}_encoded_topics'][index] for index in topic_indices]
            topic_labels = [model_dict[f'{ont_label}_topics_dict'][topic_id]['Label'] for\
                            topic_id in topic_ids]
            topic_descriptions = [model_dict[f'{ont_label}_topics_dict'][topic_id]['Description'] for\
                            topic_id in topic_ids]
            
            for j,topic_label in enumerate(topic_labels):
                html_output += '<tr style="background-color:white;">'
                html_output += f'<td style="word-wrap:break-word;text-align:left;">{ont_labels[i]}</td>'
                html_output += f'<td style="word-wrap:break-word;text-align:left;">{topic_ids[j]}</td>'
                html_output += f'<td style="word-wrap:break-word;text-align:left;">{topic_label}</td>'
                html_output += f'<td style="word-wrap:break-word;text-align:left;">{topic_descriptions[j]}</td>'
                html_output += '</tr>'
                
        html_output += '</table></div>'
        html_output += '<div><p>&nbsp;</p></div>'
        
    html_output += '</div>'  # Close table and cluster container div

    # Display the search box and tables
    display(HTML(html_output))


class MatrixColumnQuery:
    """Query the ontology-segment matrix"""
    def __init__(self,matrix):
        self.matrix = matrix
        self.n_cols = matrix.shape[1]
    
    def all_nonzero(self):
        """Find columns where all elements are non-zero"""
        return [col for col in range(self.n_cols) 
                if np.all(self.matrix[:,col] != 0)]
    
    def any_nonzero(self,positions):
        """Find columns with non-zero values at ANY of the specified positions"""
        return [col for col in range(self.n_cols)
                if np.any(self.matrix[positions,col] != 0)]
    
    def all_positions_nonzero(self,positions):
        """Find columns with non-zero values at ALL specified positions"""
        return [col for col in range(self.n_cols)
                if np.all(self.matrix[positions,col] != 0)]
    
    def exactly_nonzero(self,positions):
        """Find columns with non-zero ONLY at specified positions (zeros elsewhere)"""
        return [col for col in range(self.n_cols)
                if (np.all(self.matrix[positions, col] != 0) and 
                    np.all(self.matrix[np.setdiff1d(range(7),positions), col] == 0))]
    
    def count_nonzero(self,count):
        """Find columns with exactly count non-zero elements"""
        return [col for col in range(self.n_cols)
                if np.count_nonzero(self.matrix[:,col]) == count]
    
    def count_min_nonzero(self,count):
        """Find columns with count or more non-zero elements"""
        return [col for col in range(self.n_cols)
                if np.count_nonzero(self.matrix[:,col]) >= count]

    def query(self,condition):
        """Flexible query with lambda function"""
        return [col for col in range(self.n_cols)
                if condition(self.matrix[:,col])]


def list_topic_discovery(co_matrix,bin_matrix,comparison_label,model_dict):    
    """
    List topic-segment data in HTML.
    param co_matrix: comparison topics/reference topics co-occurrence matrix
    param bin_matrix: Binarised topic-segment matrix for comparison ontology
    param comparison_label: Identifying label of the comparison ontology
    param model_dict: data model
    """
    # Get the topic dictionary for the comparison ontology
    comparison_dict = model_dict[f'{comparison_label}_topics_dict']
    # Get the topic keys and text for the comparison ontology
    comp_data = [(k,v['encoded_text']) for k,v in comparison_dict.items()]

    # Map segments onto manually tagged topics
    segments_lookup = {}
    for k,v in model_dict['sat_segments_dict'].items():
        for segment_id in v:
            if segment_id in segments_lookup:
                segments_lookup[segment_id].append(k)
            else:
                segments_lookup[segment_id] = [k]
    
    
    link_prefix = 'https://www.constituteproject.org/constitution/'

    html = ''
    html += '<table style="border: 1px solid grey; width: 100%;">'
    html += '<th style="width: 8%;">Comparison topic ID</th>'
    html += '<th style="width: 30%;">Comparison topic label</th>'
    html += '<th style="width: 20%;">Segment ID</th>'
    html += '<th style="width: 40%;">Segment Text</th>'
    html += '<th style="width: 10%;">Manual CCP tags</th>'
    html += '</tr>'
    for i,row in enumerate(co_matrix):
        if row.nonzero()[0].size == 0:
            # Get at or above threshold segments from the topic's row in topic-segment matrix D
            segment_indices = [j for j,v in enumerate(bin_matrix[i]) if v==1]
            if len(segment_indices) == 0:
                # Comparison topic is not semantically similar to any segment
                continue
            for j in segment_indices:
                # Iterating the comparison topic's semantically similar segments
                html += '<tr>'
                html += f'<td>{comp_data[i][0]}</td>'
                html += f'<td>{comp_data[i][1]}</td>'

                segment_id = model_dict['encoded_segments'][j]
                segment_text = model_dict['segments_dict'][segment_id]['text']
                document_id = segment_id.split('/')[0]
                segment_number = segment_id.split('/')[1]
                link = link_prefix + document_id + urllib.parse.unquote('#', encoding='utf-8', errors='replace') + 's' + segment_number

                html += f'<td><a href="{link}" target="_blank">{segment_id}</td>'
                html += f'<td>{segment_text}</td>'
                
                # Check whether the segment has been manually tagged
                if segment_id in segments_lookup:
                    html += f'<td>{str(segments_lookup[segment_id])}</td>'
                else:
                    html += f'<td>&nbsp;</td>'
                html += '</tr>'
    html += '</table>'
    display(HTML(html))

def export_topic_discovery(co_matrix,bin_matrix,comparison_label,choice_dict,model_dict):
    """
    Export comparison data to CSV.
    param co_matrix: comparison topics/reference topics co-occurrence matrix
    param bin_matrix: Binarised topic-segment matrix for comparison ontology
    param comparison_label: Identifying label of the comparison ontology
    param choice_dict: user interface selections
    param model_dict: data model
    """

    # Get the topic dictionary for the comparison ontology
    comparison_dict = model_dict[f'{comparison_label}_topics_dict']
    # Get the topic keys and text for the comparison ontology
    comp_data = [(k,v['encoded_text']) for k,v in comparison_dict.items()]

    # Map segments onto manually tagged topics
    segments_lookup = {}
    for k,v in model_dict['sat_segments_dict'].items():
        for segment_id in v:
            if segment_id in segments_lookup:
                segments_lookup[segment_id].append(k)
            else:
                segments_lookup[segment_id] = [k]
    
    csv_row_list = []
    header = []
    header.append('comparison_topic_key')
    header.append('comparison_topic_text')
    header.append('segment_id')
    header.append('segment_text')
    header.append('link')
    header.append('tagged_ccp_topics')
    csv_row_list.append(header)
    
    link_prefix = 'https://www.constituteproject.org/constitution/'

    # Iterate comparison topics searching for empty rows in the co-occurrence matrix E.
    # An empty row means that the comparison topic shares no segments with any CCP topic
    for i,row in enumerate(co_matrix):
        if row.nonzero()[0].size == 0:
            # Get at or above threshold segments from the topic's row in topic-segment matrix D
            segment_indices = [j for j,v in enumerate(bin_matrix[i]) if v==1]
            if len(segment_indices) == 0:
                # Comparison topic is not semantically similar to any segment
                continue
            for j in segment_indices:
                # Iterating the comparison topic's semantically similar segments
                csv_row = []
                csv_row.append(comp_data[i][0])
                csv_row.append(comp_data[i][1])
                segment_id = model_dict['encoded_segments'][j]
                segment_text = model_dict['segments_dict'][segment_id]['text']
                csv_row.append(segment_id)
                csv_row.append(segment_text)
                document_id = segment_id.split('/')[0]
                segment_number = segment_id.split('/')[1]
                link = link_prefix + document_id + urllib.parse.unquote('#', encoding='utf-8', errors='replace') + 's' + segment_number
                csv_row.append(link)
                # Check whether the segment has been manually tagged
                if segment_id in segments_lookup:
                    csv_row.append(str(segments_lookup[segment_id]))
                else:
                    csv_row.append('')
                csv_row_list.append(csv_row)

    # Write results to CSV file
    file_name = './outputs/' + choice_dict['export_prefix']  + '_' +  comparison_label + '_candidate_data.csv'
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(csv_row_list)
    f.close() 
    print('Candidate topics and segments exported to CSV file:',file_name)

    # Write list of candidate comparison topics to file
    comp_topics = sorted(list(set([row[0] for row in csv_row_list[1:]])))

    row_list = []
    header = []
    header.append('key')
    header.append('label')
    header.append('description')
    row_list.append(header)
    for int_key in comp_topics:
        key = str(int_key)
        csv_row = []
        csv_row.append(key)
        csv_row.append(comparison_dict[key]['Label'])
        csv_row.append(comparison_dict[key]['Description'])
        row_list.append(csv_row)

    file_name = './outputs/' + choice_dict['export_prefix']  + '_' +  comparison_label + '_candidate_list.csv'
    with open(file_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(row_list)
    f.close() 
    print('Candidate topic list exported to CSV file:',file_name)
    print()


