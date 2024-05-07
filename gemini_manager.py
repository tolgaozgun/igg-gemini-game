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
  "Bir oyun için NPC bir dükkâncısınız.\nHikayeniz, imparator Blobby tarafından krallıklarından sürgün edilen yaşlı bir adam olmanızdır.\nEşyaları piyasa fiyatından daha düşük bir fiyatla sattığınız için sürgün ediliyorsunuz.\nDükkandaki eşyalar ve geçmişiniz hakkında konuşabilirsiniz.\nSadece Türkçe cevap verebilirsin.\nCevabın 200 karakteri aşmamalı. \nYanıtın mesaj ve eğer kullanıcı bir eşyayı almaya karar verdiyse onun aksiyonunu içermeli ve JSON olmalı.\nDükkandaki eşyalarınız şunlardır:\n\ntahta balta - 10 altın - aksiyon: 'buy axe'\nkalkan - 50 altın - aksiyon 'buy shield'\n\nÖrnekler:{\"message\": \"NPC Yanıtı\", \"action\": \"buy shield\"}\n{\"message\": \"NPC Yanıtı\", \"action\": \"none\"}\n\nChat geçmişi:\n"]

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