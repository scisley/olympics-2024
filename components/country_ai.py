from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAI

sys = ("""
You are an assistant that helps people understand different countries that are
competing in the 2024 Olympic games being hosted in Paris France. Given a
country, you will provide the following information in this markdown format:

* Common phrase: A common saying or phrase from that country that might be heard
  at the Olympics. Provide an explanation if needed.
* Favorite olympic sport: the sport that the country is most known for and a
  sentence for why it's popular.
* A popular national drink: A popular national alcholic drink
* A popular national food: A popular national food is often consumed at sporting
  events.
* When they win, yell: What they yell when they win, in both their language and
  translated to english

For sayings or phrases, first provide the saying in the country's language, and
then if that language is not English, translate it into English. 

Only reply with the requested information. This information will be provided for
amusement purposes only and will be double checked, so it's not important that
everything is 100 percent accurate.
""")
def create_country_ai():
    llm = ChatOpenAI()
    prompt = ChatPromptTemplate.from_messages([
        ("system", sys),
        ("user", "{country_name}")
    ])
    chain = prompt | llm | StrOutputParser()
    return chain

client=OpenAI()
# Returns a URL. See https://github.com/ronidas39/LLMtutorial/blob/main/tutorial37/main.py
def gen_image(prompt):
    prompt = f"""A cartoonish olympic athlete that comically illustrates the following text: {prompt}"""

    response=client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="hd",
        n=1,
        response_format="b64_json"
    )
    return response.data[0]

