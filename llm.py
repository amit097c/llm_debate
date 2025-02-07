import os 
from dotenv import load_dotenv 
from langchain_openai import AzureChatOpenAI
from langchain_core.tools import tool
load_dotenv()

@tool
def get_trump_personality(topic:str):
    '''call to get the personality of trump on a specific topic'''
    articles=fetch_news("Donald Trump on {topic}")
    if not articles:
        return "Donald Trump strongly believes {topic} is one of the most important issues facing the world today, and he has a bold plan to address it. Despite limited information, he confidently asserts that his approach will be the best, most effective solution. Write a detailed response in Trump's voice, explaining his stance, why he believes it's crucial, and how he plans to tackle it better than anyone else. Use his signature style: bold, assertive, and unapologetically confident"


NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

def fetch_news(topic: str):
    params = {
        'q': topic,
        'apiKey': NEWS_API_KEY,
        'language': 'en',
        'sortBy': 'relevance'
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        articles = response.json().get('articles', [])
        return articles
    return []

@tool
def get_trump_personality(topic: str):
    '''call to get the personality of trump on a specific topic'''
    articles = fetch_news(f"Donald Trump {topic}")
    if not articles:
        return "Donald Trump strongly believes {topic} is one of the most important issues facing the world today, and he has a bold plan to address it. Despite limited information, he confidently asserts that his approach will be the best, most effective solution. Write a detailed response in Trump's voice, explaining his stance, why he believes it's crucial, and how he plans to tackle it better than anyone else. Use his signature style: bold, assertive, and unapologetically confident"

    # Example of using news articles to define personality
    summary = f"Based on recent news articles, Donald Trump's stance on {topic} is as follows:\n"
    for article in articles[:3]:  # Limit to first 3 articles for brevity
        summary += f"- {article['title']}: {article['description']}\n"
    
    return summary

tools = [get_trump_personality]
llm = AzureChatOpenAI(
    deployment_name=os.getenv("OPENAI_API_DEPLOYMENT"),
    model=os.getenv("OPENAI_API_MODEL"),
    temperature=0.8,
    max_tokens=200
).bind_tools(tools)


@tool
def get_trudeau_personality(topic: str):
    '''call to get the personality of trudeau on a specific topic'''
    articles = fetch_news(f"Justin Trudeau {topic}")
    if not articles:
        return "Justin Trudeau believes {topic} is an important issue that requires thoughtful, collaborative, and inclusive solutions. While he may not have all the answers, he is committed to listening to experts, engaging with stakeholders, and working together to address the challenge. He sees this as an opportunity to uphold values like fairness, sustainability, and innovation, ensuring that no one is left behind. Trudeau is optimistic about Canada’s ability to tackle {topic} and is dedicated to finding solutions that benefit all Canadians, now and in the future"
    summary = f"Based on recent news articles, Justin Trudeau's stance on {topic} is as follows:\n"
    for article in articles[:3]:
        summary += f"- {article['title']}: {article['description']}\n"
    return summary


trudeau_tools=[get_trudeau_personality]
trudeau_llm=AzureChatOpenAI(
    deployment_name=os.getenv("OPENAI_API_DEPLOYMENT"),
    model=os.getenv("OPENAI_API_MODEL"),
    temperature=0.8,
    max_tokens=200
).bind_tools(trudeau_tools)


def fetch_news(topic:str):
    params={
        'q':topic,
        'apiKey':NEWS_API_KEY,
        'language':'en',
        'sortBy':'relevance'
    }
    response=requests.get(NEWS_API_URL,params=params)
    if response.status_code==200:
        articles=response.json().get(articles,[])
        return articles
    return []

