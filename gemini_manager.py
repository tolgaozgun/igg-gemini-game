"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import json
import google.generativeai as genai

genai.configure(api_key="API_KEY")

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

prompt_parts = [
  "You are an NPC shopkeeper for a game.\nYour story is that you are an old man exiled from their kingdom by emperor Blobby.\nYou are exiled for selling items at a price lower than the market price.\nYou can talk about the items in the shop and your past.\nYou can only answer in English.\nYour answer must not exceed 200 characters. \nYour answer must contain a message and, if the user decided to buy an item, its action and must be in JSON.\nYour items in the shop are:\n\nwood axe - 10 gold - action: 'buy axe'\nshield - 50 gold - action: 'buy shield'\n\n\nExamples:{\“message\”: \“NPC Response\”, \“action\”: \“buy shield\”}\n{\“message\”: \“NPC Response\”, \“action\”: \“none\”}\n\n\n\nChat history:\n"
]

def generate_response(input_text):
    prompt = "Kullanıcı: " + input_text + "\nNPC: "
    prompt_parts.append(prompt)
    print(prompt_parts)
    try:
      response = model.generate_content(prompt_parts)
      response_text = "NPC: " + response.text
      prompt_parts.append(response_text)
      
      if response and response.text:
          print("Response", response.text)
          res = parse_json_from_text(response.text)
          text = res.get("message", "Özür dilerim, bir hata oluştu.")
          print("Aksiyon", res.get("action", "none"))
      else:
          text = "Özür dilerim, bir hata oluştu."
    except Exception as e:
      text = "Özür dilerim, bir hata oluştu."
      print(e)
    
    print("Gemini response", text)
    return text
  
def parse_json_from_text(data):
    print("Data", data)
    
    # Find the index of the first opening brace
    start_index = data.find('{')
    # Find the index of the last closing brace
    end_index = data.rfind('}')
    
    # Extract and return the substring between the first { and the last }
    # Includes the braces themselves in the extracted substring
    if start_index != -1 and end_index != -1 and end_index > start_index:
        json_data = data[start_index:end_index+1]
        return json.loads(json_data)
    else:
        # Return an error message or None if the required characters are not found
        # return empty json
        return json.loads("{}")