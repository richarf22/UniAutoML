import gradio as gr

from llm.llm2 import maincode2

from llm.llm1 import maincode 
import json
with open('cifar-10-batches-py/data_batch_1') as f:
      data_desc = f.read()
prompt1=input
prompt=[prompt1]  




def predict1(prompt[0]):
    for index in range(2):
        
        history=state.get("output","")
        if index == 0:
            response,explain=maincode(prompt[0])
            return history,response+'\n'+explain,{"output": response}
        else:
            response2=json.loads(maincode2(user_request))
            return history,response2["name"]+'\n'+response["reason"],{"output": reesponse2}
gr.Interface(
    fn=predict1,
    title=title,
    description=description,
    examples=examples,
    inputs=["text","text","state"],
    outputs=["text","chatbot","state"],
    theme="finlaymacklon/boxy_violet",
).launch()
