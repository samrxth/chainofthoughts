import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=0.7)

sentiment_prompt = PromptTemplate(
    input_variables=["headline", "article"],
    template="""
    Evaluate whether the sentiment expressed in the following article is generally positive or negative:

    Headline: "{headline}"
    Article: "{article}"

    Output either "positive" or "negative" based on the overall sentiment of the content.
    """
)
sentiment_chain = LLMChain(llm=llm, prompt=sentiment_prompt)

def is_positive(headline, article):
    return ("positive" in sentiment_chain.invoke({"headline": headline, "article": article})["text"].lower())

insights_prompt = PromptTemplate(
    input_variables=["headline", "article", "sentiment"],
    template="""
    Given that the overall sentiment is "{sentiment}", identify the insights in the following article and explain why these insights would affect the market:

    Headline: "{headline}"
    Article: "{article}"

    List the insights and provide explanations for their potential market impact.
    """
)
insights_chain = LLMChain(llm=llm, prompt=insights_prompt)

def extract_insights(headline, article, sentiment):
    return insights_chain.invoke({"headline": headline, "article": article, "sentiment": sentiment})

score_prompt = PromptTemplate(
    input_variables=["headline", "article", "insights"],
    template="""
    Based on the following insights and the overall content of the article, score the potential impact on the stock market:

    Headline: "{headline}"
    Article: "{article}"
    Insights: "{insights}"

    Evaluate the insights and generate a numeric score for its impact on the stock market based on the following scale:
    - Highly Positive: 0.7 to 1
    - Positive: 0.5 to 0.699
    - Neutral Positive: 0.1 to 0.499
    - Neutral: -0.1 to 0.1 
    - Neutral Negative: -0.499 to -0.1
    - Negative: -0.5 to -0.699
    - Highly Negative: -0.7 to -1
    
    Example 1:
    Insight: "Nvidia's continued leadership in AI and the anticipation of new AI products at the upcoming GTC are expected to boost investor enthusiasm and could lead to a notable increase in Nvidia’s stock price."
    Score: +0.917

    Example 2:
    Insight: "META faces increased regulatory scrutiny over its data handling and privacy practices, which could result in stringent compliance costs and reduce user engagement, impacting ad revenues and posing a substantial threat to META's core business model."
    Score: -0.783

    Example 3:
    Insight: "Laser Photonics Corporate is making steady progress in its operational strategies, which reassures existing investors of stability but is unlikely to draw significant new investment or substantially impact the stock price in the short term."
    Score: +0.057

    The scores should follow a normal distribution similar to the bell curve, with significant deviations from the center. Ensure the values have three significant figures. Avoid clustering scores too closely around the center.
    You need to be more confident, do not rely on 0.4-0.7 be bold, be strong and think. Don't fall into repetition or take too safe a stance.
    Don't be afraid to be strongly negative or positive, or even strongly neutral.
    Only provide the numeric score with no other characters except the sign, period, and integers that make the number.
    Ensure the values have three significant figures with NO TRAILING ZEROES.
    """
)
score_chain = LLMChain(llm=llm, prompt=score_prompt)

def score_article(headline, article, insights):
    return score_chain.invoke({"headline": headline, "article": article, "insights": insights})

def CoT(headline, article):
    sentiment = "positive" if is_positive(headline, article) else "negative"
    insights = extract_insights(headline, article, sentiment)
    score = score_article(headline, article, insights['text'])
    print("CoT score:", score['text'])
    return score['text']
