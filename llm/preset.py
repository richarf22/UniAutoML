from openai import OpenAI
import httpx

import httpx
import json
import os

def get_configs(most_relevant_cfgs):
    configs = []
    if isinstance(most_relevant_cfgs, str):
         
        try:
            with open(most_relevant_cfg, 'r', encoding='utf-8') as file:
                ext = os.path.splitext(most_relevant_cfg)[1]  # 获取文件的扩展名
                if ext == '.json':
                    config = json.load(file)  # 如果文件是 json 格式，使用 json.load 读取
                else:
                    config = file.read()  # 否则，使用 file.read 读取
                
        except IOError:
            print(f"Failed to read config from {most_relevant_cfg}")
        return config 
    else:
        for cfg_path in most_relevant_cfgs:
            try:
                with open(cfg_path, 'r', encoding='utf-8') as file:
                    ext = os.path.splitext(cfg_path)[1]  # 获取文件的扩展名
                    if ext == '.json':
                        config = json.load(file)  # 如果文件是 json 格式，使用 json.load 读取
                    else:
                        config = file.read()  # 否则，使用 file.read 读取
                    configs.append(config)
            except IOError:
                print(f"Failed to read config from {cfg_path}")
        return configs
def get_config(most_relevant_cfg):
    
    
    try:
        with open(most_relevant_cfg, 'r', encoding='utf-8') as file:
            ext = os.path.splitext(most_relevant_cfg)[1]  # 获取文件的扩展名
            if ext == '.json':
                config = json.load(file)  # 如果文件是 json 格式，使用 json.load 读取
            else:
                config = file.read()  # 否则，使用 file.read 读取
            
    except IOError:
        print(f"Failed to read config from {most_relevant_cfg}")
    return config
client = OpenAI(
        
        base_url="https://oneapi.xty.app/v1", 
        api_key="sk-AH4m6lHFMNIClaHX5c30102c86E84b478eB7CaF10e47C568",
        
        http_client=httpx.Client(
            base_url="https://oneapi.xty.app/v1",
            follow_redirects=True,

        )
        
        
    )


def get_completion(prompt_0,prompt_1="None",messages=None):
    if messages is None:
        messages = []   
        messages.append({"role": "system", "content": prompt_0})
        messages.append({"role": "user", "content": prompt_1})
        response=completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
            
            
    )
        messages.clear()
        messages=None
        return response.choices[0].message.content
    else :
        messages = []   
        messages.append({"role": "system", "content": prompt_0})
        messages.append({"role": "user", "content": prompt_1})
        response=completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0,
            
            
    )
        messages.append({"role": "assistant", "content": response.choices[0].message.content})

    
        return response.choices[0].message.content,messages
def get_completion1():
    
    raise ValueError("invalid input")



