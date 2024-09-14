import random
from llm.preset import *
from llm.filter import filter


history=[]
def maincode4(most_relevant_cfgs,quality,prompt="None"):
    
    global history
    if quality == 'medium' :
        with open('E:\\fusion_mlp.py', 'r', encoding='utf-8') as file:
        # 读取文件内容
            fusion_config = file.read() 
    if quality == 'high' : 
        with open('E:\\fusion_transformer.py', 'r', encoding='utf-8') as file:
        # 读取文件内容
            fusion_config = file.read()  
    base_configs = get_configs(most_relevant_cfgs)
    
    prompt_sys=f"""You are a helpful assistant that writes the Deep learning
    model code. You task is to only write a fusion model to fuse
    different base models' features without any explanation. Use # before every line
    except the python code. Here are some model code for you
    reference:
    from multimodal.models import CategoricalTransformer
    class CategoricalTransformer(nn.Module):
    def init (self,model config):
    ...
    from multimodal.models import NumericalTransformer
    class NumericalTransformer(nn.Module):
    def init (self,model config):
    ...
    from multimodal.models import TimmAutoModelForImagePrediction
    class TimmAutoModelForImagePrediction(nn.Module):
    def init (self,model config):
    ...
    from multimodal.models import HFAutoModelForTextPrediction
    class HFAutoModelForTextPrediction(nn.Module):
    def init (self,model config):
    ...
    Given some base models' config as follow:{base_configs};
    Give the fusion model config as follow: {fusion_config}
    You should then respond to me the code with:
    1). Fusion technique should be learnable, MLP is recommended.
    2). The fusion model structure should be defined as fusion
    model and fusion head,which output features and logits,
    respectively.
    3). Base models instance should be defined in Fusion model
    Class.You should not change the value of the output of base
    model instances.
    4). All base models have a uniform variable(
    self.out features dim) to represent the output
    features dimension.
    5). Finding the maximum dimension of all base models'
    output features, and define learnable linear layers to adapt
    all base models' output features to the maximum dimension
    as the input of fusion model. For example, if three models
    have feature dimensions are [512, 768, 64], it will linearly
    map all the features to dimension 768.
    6). Output the logits,features,loss weights of fusion model
    and base models.The return must be in a JSON format:
    {{model name:{{“logits”:...,“features”:...,“weight”:...}}}}.
    7). All the network layers and variable
    self.model name,self.loss weight should be defined in
    function init , not in function forward.
    8). Some variables are not present in each model’s config,
    you cannot use a variable that does not exist in the corresponding
    model config.
    You should only respond in the format as described below :
     
    """
    
    try:
        '''if(random.randint(1,2)>1):
            response=get_completion1(prompt)
            return response
        else:'''
        response,history=get_completion(prompt_sys,prompt,history)
        response=filter(response)
        prompt2=f"""
       the Deep learning
model code is the content delimited by triple backticks, 
        pleasee only explain it briefly and easy to understand for greenhands without other contents
        '''{response}'''
         """
        response2=filter(get_completion(prompt2))
        return (response, response2)
    except Exception as e:
        error_info=(type(e), str(e))
        prompt1_1=f"""contents delimited by triple backticks are the output errors for analyzing modalities of cifar-10,you have several tasks, first, apologize for generating errors.
        second,trying to explain why errors occurred by analyzing the output
        , if the output is not completed , your response should be disconnect from gpt-4.
            '''{error_info}'''
        """
        response1=filter(get_completion(prompt1_1))
    
        return response1,None









