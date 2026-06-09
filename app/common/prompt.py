from langchain_core.messages.human import HumanMessage
def img_prompt_func(data_dict):
   """
   Join the context into a single string
   """
   formatted_texts = "\n".join(data_dict["context"]["texts"])
   messages = []

   # Adding the text for analysis
   text_message = {
       "type": "text",
       "text": (
           "You are mine safety expert tasking with providing safety advice.\n"
           "You will be given a mixed of text, tables.\n"
           "Use this information to provide safety advice related to the user question. \n"
           f"User-provided question: {data_dict['question']}\n\n"
           "Text and / or tables:\n"
           f"{formatted_texts}"
       ),
   }
   messages.append(text_message)
   # Adding image(s) to the messages if present
   if data_dict["context"]["images"]:
       for image in data_dict["context"]["images"]:
           image_message = {
               "type": "image_url",
               "image_url": {"url": f"data:image/jpeg;base64,{image}"},
           }
           messages.append(image_message)
   return [HumanMessage(content=messages)]

