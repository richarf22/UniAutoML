from llm.llm2 import maincode2
from llm.llm3 import maincode3
from llm.llm4 import maincode4
from llm.llm1 import maincode 
import json

prompt1='''now,please analyze  the modalities of cifar-10 {data_desc} whose path is at cifar-10-batches-py/data_batch_1 '''
response,explain=maincode(prompt1)
print(response,explain)
user_request='''the dataset is cifar-10 and its modality is {response0}'''

response2=json.loads(maincode2(user_request,response))
print(response2["name"],response["reason"])