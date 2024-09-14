import random
import zipfile
import os
from llm.preset import get_completion,get_completion1
import streamlit as st
import pandas as pd
import json
from llm.filter import filter
def read_unknown_file(file_path):
    try:
        return pd.read_csv(file_path)
    except pd.errors.ParserError:
        pass

    try:
        return pd.read_excel(file_path)
    except Exception:  # pd.errors.ExcelFileError in pandas>=1.2.0
        pass

    try:
        return pd.read_json(file_path)
    except pd.errors.ParserError:
        pass

    try:
        return pd.read_hdf(file_path)
    except Exception:  # pd.errors.HDF5Error in pandas>=1.2.0
        pass

    try:
        return pd.read_parquet(file_path)
    except Exception:  # pyarrow.lib.ArrowInvalid in pyarrow
        pass

    try:
        return pd.read_pickle(file_path)
    except Exception:  # pickle.UnpicklingError in pickle
        pass

    raise ValueError(f"Could not read file {file_path} with any known pandas format")


 

history = []

def maincode(prompt,zipdata,zipdataset):
    global history
    'zipdata=st.chat_input()'
    data=zipdata.replace('.zip', '')
    dataset = zipdataset.replace('.zip', '')
    with zipfile.ZipFile(zipdata, 'r') as zip_ref:
        zip_ref.extractall(data)
    dataset = read_unknown_file(f'{dataset}')
    prompt_sys=f"""You are a helpful assistant that analyze data modalities
in multimodal Auto-Machine learning task.
Your task is to analyze the data type of each column
of the pandas.DataFrame tabular data,which is the content delimited by brace {dataset}.
Your answer must be use a strict JSON format without any context:
{{"column name": "data type"}}.
You can analyze the data type based on the corresponding
column name,column data and the user
instructions, which may contain the context of
tasks/datasets, etc..
You should not omit any column of data in your answer.
In most cases, label column exist in dataset which is normally the target variable I want the model to predict or classify. 
Modality name examples: "text", "image", "audio", "video", "document", "table",  "semantic_seg_img", "ner",  "categorical", "numerical", "label".
Here are some examples for your reference:
Input: instructions:{{data1_desc}},Date:{{data1_input}}
Output: {{data1_output}}
Input: instructions:{{data2_desc}},Date:{{data2_input}}
Output: {{data2_output}}
Input: instructions:{{data3_desc}},Date:{{data3_input}}
Output: {{data3_output}}
Input: instructions:{{data0_desc}},Date:{{data0_input}}
Output:"""
    try:
        '''if(random.randint(1,2)>1):
            response=get_completion1(prompt)
            return response
        else:'''
        response,history=get_completion(prompt_sys,prompt,history)
        '''response=filter(response)
        dictionary=json.loads(response)
        values =  dictionary.values()
        unique_values_list = list(set(values))
        num=  len(list(set(values)))'''
        
        prompt2=f"""
        the modalities of  data is the content delimited by triple backticks, 
        pleasee only explain it briefly and easy to understand for greenhands without other contents
        '''{response}'''
         """
        response2=filter(get_completion(prompt2))
        response2+='\nThe stage for analyzing modalities of dataset is completed.the next stage is to choose the model for machine learning, if you have instructions, please provide them. If not, simply press enter to continue.'
        return response,response2
    except Exception as e:
        error_info=(type(e), str(e))
        prompt1_1=f"""contents delimited by triple backticks are the output errors for analyzing modalities of one dataset using gpt-4,you have several tasks, first, apologize for generating errors.
        second,trying to explain why errors occurred by analyzing the output
        , if the output is not completed , your response should be disconnect from gpt-4.
            '''{error_info}'''
        """
        response1=filter(get_completion(prompt1_1))
    
        return response1, None, None, None








