import random
from llm.preset import *
from llm.filter import filter


history=[]
def maincode6(most_relevant_configs,self_desc,prompt="None"):
    
    global history
    configs=get_configs(most_relevant_configs)
    
    prompt_sys=f"""You are a helpful assistant that infers the hyperparameters
    and their search ranges for hyperparameter optimization
    in machine learning task.
    You can use the format:[value1,value2,value3,...,] to
    represent a discrete search range.
    Your answer must be in a strict JSON format:
    {{"hyperparameter name":"search range"}}.
    Here are some comments to help you understand the
    parameters better:
    {self_desc}
    Here are some things you need to focus on:
    1).If the values in the search space are of type INT or
    FLOAT, then the search space needs to have at least 3
    values.
    2).The search ranges should refer to the original value
    of the config. The search ranges should include the
    original value of the config.
    3).You should not output the hyperparameters don’t
    need to optimize.
    4).You cannot forge parameters that are not in the
    configuration file.
    5).If the "checkpoint name" is in config, only the
    "loss weight" is taken.
    Given the config as follow:
    {configs}
    if using the information provided you can't infer the search ranges for hyperparameter optimization, please estimate the search range based on the hyperparameter name and  general search ranges as a starting point.
    Your answer:
    """
    
    try:
        '''if(random.randint(1,2)>1):
            response=get_completion1(prompt)
            return response
        else:'''
        response,history=get_completion(prompt_sys,prompt,history)
        response=filter(response)
        prompt2=f"""
        the hyperparameters
        and their search ranges for hyperparameter optimization
        in machine learning task are the contents delimited by triple backticks, 
        pleasee only explain it briefly and easy to understand for greenhands without other contents
        '''{response}'''
         """
        response2=filter(get_completion(prompt2))
       
        return response,response2
    except Exception as e:
        error_info=(type(e), str(e))
        prompt1_1=f"""contents delimited by triple backticks are the output errors for analyzing modalities of cifar-10,you have several tasks, first, apologize for generating errors.
        second,trying to explain why errors occurred by analyzing the output
        , if the output is not completed , your response should be disconnect from gpt-4.
            '''{error_info}'''
        """
        response1=get_completion(prompt1_1)
    
        return response1,None








