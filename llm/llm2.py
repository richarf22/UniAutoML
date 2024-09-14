import random
from llm.preset import *
import pickle
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain.llms import OpenAI
from langchain_community.vectorstores.docarray.in_memory import DocArrayInMemorySearch
import requests
from bs4 import BeautifulSoup
import os
import httpx
from concurrent.futures import ThreadPoolExecutor

# 请求网页
url = "https://huggingface.co/models"
response = requests.get(url)

# 解析网页
soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')

# 查找所有的 tag
tags = soup.find_all('a')

# 提取 tag 的 href 属性
hrefs = [tag.get('href') for tag in tags]

# 提取等号后的部分
pipeline_tags = [href.split('=')[-1] for href in hrefs]
# 找到 "model" 的位置


# 获取 "model" 后面的十个元素

fun_index = pipeline_tags.index('image-text-to-text')
fun_index_last = pipeline_tags.index('graph-ml')

#创建openai的embeddings

openai_embeddings = OpenAIEmbeddings( base_url="https://oneapi.xty.app/v1", 
        api_key="sk-AH4m6lHFMNIClaHX5c30102c86E84b478eB7CaF10e47C568",
        http_client=httpx.Client(
            base_url="https://oneapi.xty.app/v1",
            follow_redirects=True,
        ), model="text-embedding-3-small")
#创建向量数据库
vectordb = DocArrayInMemorySearch.from_texts(
    pipeline_tags[fun_index:fun_index_last],
    embedding=openai_embeddings 
)
 
#创建检索器,让它每次只返回1条最相关的文档：search_kwargs={"k": 1}
# 另一个要比较的文本







vector_dbs = []
def check_url(url):
    flag = 1
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，这将抛出一个 HTTPError 异常
    except requests.exceptions.HTTPError as err:
        if err.response.status_code == 404:  # 如果错误是 404 错误
            flag = 0  # 将 flag 的值设置为 0
    return flag


def download_file(url, filename, newname):
    # 如果文件已经存在，就不再下载
        if os.path.exists(newname):
        
            return
        else:
            response = requests.get(url)
            response.raise_for_status()
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as f:
                f.write(response.content)
            if os.path.exists(newname):
                os.remove(filename)
            else:
                
                os.rename(filename, newname)
def process_index(index,prompt,unique):
        most_relevant_documents=[""]*len(unique)
        most_relevant_cfgs=[""]*len(unique)
        response2=[""]*len(unique)
     
        openai_retriever = vectordb.as_retriever(search_kwargs={"k": 1})
        other_text = prompt+'\n one of the modalities of the dataset is '+unique[index]
        docs=openai_retriever.get_relevant_documents(other_text)
        page_contents = [doc.page_content for doc in docs]

                # 请求网页
        url = "https://huggingface.co/models?pipeline_tag="+page_contents[0]+"&sort=trending"
        response = requests.get(url)

                # 解析网页
        soup = BeautifulSoup(response.text, 'html.parser')
                # 查找所有的 tag
        tags = soup.find_all('a')

                # 提取 tag 的 href 属性
        hrefs = [tag.get('href') for tag in tags]

                # 提取等号后的部分
        pipeline_mtags = [href.split('=')[-1] for href in hrefs]

                # 找到 "model" 的位置
        model_index = pipeline_mtags.index('model')

                # 获取 "model" 后面的十个元素
        next_ten_tags = pipeline_mtags[model_index+1:model_index+11]    

        files=[]
            
        highest_similarity = -1
        for tag in next_ten_tags:
                    

                    
                    # 用你想要下载的文件的 URL 替换这个 URL
            url = 'https://huggingface.co'+tag+'/resolve/main/README.md'
                
                    # 用你想要保存的文件名替换这个文件名
            filename = 'model_cards/README.md'
                    
            new_name = tag.replace('/', '_')

            if tag == '/inayet/autotrain-price-prediction-1331950900' :
                continue
                    # 新文件名
            new_file_name = 'model_cards/' + new_name+'.md'
                    
                    # 原文件名
            flag = check_url('https://huggingface.co'+tag+'/resolve/main/config.json')
            if flag == 0:
                continue    
            download_file(url, filename,new_file_name)
                    
                    # 读取 .md 文件
                    
            with open(new_file_name, 'rb') as f:
                content = f.read().decode('utf-8')
                '''loader = TextLoader(new_file_name, encoding='utf-8')'''
            files.extend(content)
            embed=np.array(openai_embeddings.embed_query(files[len(files)-1])).reshape(1, -1) 
            query_result = np.array(openai_embeddings.embed_query(other_text )).reshape(1, -1)
            similarities =  cosine_similarity(embed,query_result, )
                    
            if similarities[0][0] > highest_similarity:
                most_relevant_documents[index] = new_file_name
                highest_similarity = similarities[0][0]

            model_card=get_config(most_relevant_documents[index])    
            prompt2=f"""{model_card}is the model chosen for the task{other_text} which contains dataset of modality {unique[index]},please only give the reasons for chossing the model without any other context"""
            response2[index]=get_completion(prompt2)
                                    
            config_tag=tag
                    # 将 '_' 替换为 '/'
            
                
            if flag == 1:
                
                    most_relevant_cfgs[index]=config_tag
                
        return (most_relevant_documents[index],most_relevant_cfgs[index],response2)
def maincode2(prompt,unique,num):
    'try:'
    most_relevant_documents=[""]*num
    most_relevant_cfgs=[""]*num
    response2=[""]*num
        
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_index, range(num), [prompt]*num, [unique]*num))

    most_relevant_documents, most_relevant_cfgs,response2 = zip(*results)
    response2=list(response2)
    response2.append('''\nThe stage for choosing the model for machine learning is completed.the next stage is to writes data processors code to load different types of data for multimodal Auto-Machine learning task, if you have instructions, please provide them. If not, simply press enter to continue.''')
       
        
    return(most_relevant_documents,most_relevant_cfgs,response2)


        
    '''except Exception as e:
        error_info=(type(e), str(e))
        prompt1_1=f"""contents delimited by triple backticks are the output errors for choosing  model for machine learning online using gpt-4,you have several tasks, first, apologize for generating errors.
        second,trying to explain why errors occurred by analyzing the output
        , if the output is not completed , your response should be disconnect from gpt-4.
            error_info
        """
        response1=get_completion(prompt1_1)
    
        return response1,error_info,None'''









