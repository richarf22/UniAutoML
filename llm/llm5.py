import random
from llm.preset import *
from llm.filter import filter

history=[]

def maincode5(most_relevant_configs,prompt="None"):
    global history
    configs=get_configs(most_relevant_configs)
    
    prompt_sys=f"""You are a helpful assistant that adds descriptions for
    the parameters in the training config for machine
    learning task.
    Your answer must be in a strict JSON format without any other content.:
    {{"hyperparameter_name":"descriptions"}}.
    You should not mention the specific values in config
    in the description.
    Given the model configs as follow: {configs}
    Your answer:
    """
    
    try:
        '''if(random.randint(1,2)>1):
            response=get_completion1(prompt)
            return response
        else:'''
        response,history=get_completion(prompt_sys,prompt,history)
        response=filter(response)
        
        return response
    except Exception as e:
        error_info=(type(e), str(e))
        prompt1_1=f"""contents delimited by triple backticks are the output errors for analyzing modalities of cifar-10,you have several tasks, first, apologize for generating errors.
        second,trying to explain why errors occurred by analyzing the output
        , if the output is not completed , your response should be disconnect from gpt-4.
            '''{error_info}'''
        """
        response1=filter(get_completion(prompt1_1))
    
        return response1








