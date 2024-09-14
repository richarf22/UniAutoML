import random
from llm.preset import *
from llm.filter import filter
import json
import glob
history = []
def maincode3(modality_config,prompt="None"):
    global history
    
    modality=modality_config.keys()

    semantic_seg_img_cfg = "None"
    if "semantic_seg_img" in modality_config:
        semantic_seg_img_cfg = get_configs(modality_config["semantic_seg_img"])
    image_cfg = "None"
    if "image" in modality_config:
        image_cfg = get_configs(modality_config["image"])
    import os


# 指定文件夹路径
    folder_path = 'C:\\Users\\Richard\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\autogluon\\multimodal\\data'
    file_paths = []
    if 'image' in modality_config:
        file_paths.append(f"{folder_path}\\process_image.py")
    if 'document' in modality_config:
        file_paths.append(f"{folder_path}\\process_document.py")
    if 'numerical' in modality_config:
        file_paths.append(f"{folder_path}\\process_numerical.py")
    if 'categorical' in modality_config:
        file_paths.append(f"{folder_path}\\process_categorical.py")
    
    file_paths.append(f"{folder_path}\\process_label.py")
    if 'ner' in modality_config:
        file_paths.append(f"{folder_path}\\process_ner.py")
    if 'text' in modality_config:
        file_paths.append(f"{folder_path}\\process_text.py")
    if 'semantic_seg_img' in modality_config:
        file_paths.append(f"{folder_path}\\process_semantic_seg_img.py")

    
   

    # 创建一个列表来存储文件内容
    data_processor= []

    # 遍历所有文件路径，读取每个文件
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取文件内容并添加到列表中
            data_processor.append(file.read())

# 现在，files 列表中的每个元素都是一个文件的内容
    prompt_sys=f"""You are a helpful assistant that writes data processors
        code to load different types of data for multimodal
        Auto-Machine learning task.
        Since different types of models need different data
        preprocessing, you task is to writes a function to return
        the corresponding data processors based on models’
        config.
        Specifically, you do not need to define a data processor
        for the fusion model. 
        your out put must be in a strict dict format without any other contenxts:
        {{"data_processor_codes": "codes","reason":"reason for chosing the data processor"}}.
        Atteonion, the key of the dict must  only be "data_processor_codes" and "reason"
        the value of "data_processor_codes" in the dictionary must follow the 5 rules: 1. I will give you an example of the function, you should only write code that can be excuted and not change the fucntion name and variable name that I define  
         2. modify the code based on my example, you should modify depending on the dataset modality{modality}, only the modality occurred should be processed.
        
        3. you also need to load the training data into each processor, the full dataset is stored in a global variable named '''dataset''', however, for each processor it only receives specific data type eg: for NumericProcessor, it only receives numeric. Thus you should extract the specific data for each processor from the dataset.
        4. the label data processor
        is also required to provide label data for each model.
        
        
        5.you do not need to write the code for excuting the processor function, only the code for defining the processor function is required.
        The example code is:
        '''
        
        from autogluon.multimodal.data import process_numerical
        from autogluon.multimodal.data import process_categorical
        from autogluon.multimodal.data import process_document
        from autogluon.multimodal.data import process_image
        from autogluon.multimodal.data import process_label
        from autogluon.multimodal.data import process_ner
        from autogluon.multimodal.data import process_text
        from autogluon.multimodal.data import process_semantic_seg_img
        #you should only import the library which will be used in your code
        
        Def processor(modality):
            # Do not change the fucntion name and variable name that I define      
            # since you have judged which processors to use, you do not need to write a if sentence to judge the modality   
                processed_data=[]#here you only need to store the processed data.
                #here you need to instantiate the numeric processor object based on the __init__ function of NumericalProcessor class in {data_processor}
                #the instantiated object should be named as "numerical_processor"
                # example of instantiating the object: numerical_processor=process_numerical.NumericalProcessor(model=numerical_model,requires_column_info=False)  
                numerical_features = {{}} #here when you write the code ,you only need to use one pair of curly braces for{{}}
                for column, column_type in modality.items():
                if column_type == "numerical":
                    numerical_features[column] = dataset[column]
                processed_data.append(numeric_processor(numerical_features, feature_modalities=modality, is_training=True)) 
                #I have given you one example, you should finish the code based on the example.
                # when you are dealing with train_transforms and val_transforms, the variable name should be based on the modality. eg: when instantiate the image_processor, train_transforms =val_transforms,you should base on the configs {image_cfg} and your knowledge
                # if you have to deal with semantic_seg_img, the img_transforms and gt_transforms should be assigned based on the configs {semantic_seg_img_cfg} and your knowledge
                return processed_data
                '''
        
       
         
        Your answer:
        """
    

    try:
        '''if(random.randint(1,2)>1):
            response=get_completion1(prompt)
            return response
        else:'''
        response,history=get_completion(prompt_sys,prompt,history)
        response=filter(response)
        f"""dictionary=json.loads(response)
       
        code=dictionary["data_processor_codes"]
        response2=dictionary["reason"]
        response2+='''\nThe stage for writing data processors code to load different types of data for multimodal Auto-Machine learning task is completed.the next stage is to write the Deep learning model code, if you have instructions, please provide them. If not, simply press enter to continue.'''
        """
        return (response, None)
    except Exception as e:
        error_info=(type(e), str(e))
        prompt1_1=f"""contents delimited by triple backticks are the output errors for writing data processors code to load different types of data for multimodal Auto-Machine learning task ,you have several tasks, first, apologize for generating errors.
        second,trying to explain why errors occurred by analyzing the output
        , if the output is not completed , your response should be disconnect from gpt-4.
            '''{error_info}'''
        """
        response1=filter( get_completion(prompt1_1))

        return response1,error_info