import openai
from Translator.AbstractTranslator import *
from Config import config
class OpenAiTranslator(AbstractTranslator):
    def __init__(self):
        super().__init__()
        openai.api_key = config.get("OpenAISetting", "OpenAIKEY")
        self.content = config.get("OpenAISetting", "OpenAIContentStart")
        self.model = config.get("OpenAISetting", "OpenAImodel")
        self.role = config.get("OpenAISetting", "OpenAIrole")
        self.top_p = float(config.get("OpenAISetting", "OpenAItop_p"))
        self.temperature = float(config.get("OpenAISetting", "OpenAItemperature"))
        self.presence_penalty = float(config.get("OpenAISetting", "OpenAIpresence_penalty"))
        self.frequency_penalty = float(config.get("OpenAISetting", "OpenAIfrequency_penalty"))
    def translate(self, word):
        content = f'{self.content}{word}'
        print(content)
        try:
            response = openai.ChatCompletion.create(
                  model=self.model, 
                  messages=[{"role": self.role, "content": content}],
                  top_p=self.top_p,
                  temperature=self.temperature,
                  presence_penalty=self.presence_penalty,
                  frequency_penalty=self.frequency_penalty
                )
        except Exception as e:
            print('simi except', e)
            return 'error'
        if response and response.choices:
            translated_text = response.get("choices")[0].get("message").get("content")
            print("结果:", response)
            print("结果:", translated_text)
            return translated_text
        else:
            print("Request failed.")
            return 'error'
    def translate111(self, word):
        prompt = f'{word}{self.prompt}'
        print(prompt)
        response = openai.Completion.create(
            model = "text-davinci-003",
            prompt = prompt,
            temperature = 0,
            max_tokens = 100
            )
        if response and response.choices:
            translated_text = response.get("choices")[0].get("text")
            print("结果:", response)
            print("结果:", translated_text)
            return translated_text
        else:
            print("Request failed.")
            return 'error'

if __name__ == "__main__":
    sentnece = f'「あぁっ♥　いいっ♥　%ANAME(MASTER)%のピストン、とってもいいわぁ♥」'
    openAiTranslator = OpenAiTranslator()
    
    openAiTranslator.translate(word=sentnece)
