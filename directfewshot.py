import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=0.7)

score_prompt = PromptTemplate(
    input_variables=["headline", "article"],
    template="""
    Analyze the potential impact of a news article on a company's stock price using the following examples as a guide:

    
    Example 1:
    Headline: "Tech Innovations Inc. Unveils Next-Generation AI Chip"
    Article: Tech Innovations Inc. announced a groundbreaking AI chip that enhances computing speeds drastically, positioning the company years ahead of competitors.
    Impact Score: +0.967  # Highly Positive

    Example 2:
    Headline: "Global Pharma Co Reaches Settlement in High-Profile Lawsuit"
    Article: Global Pharma Co has settled a lawsuit that alleged harmful side effects of one of its best-selling drugs, removing significant legal uncertainties.
    Impact Score: -0.753  # Highly Negative

    Example 3:
    Headline: "AutoDrive Vehicles Faces Massive Recall Over Safety Concerns"
    Article: AutoDrive Vehicles is recalling 1 million units due to a critical flaw in brake systems, potentially damaging brand reputation severely.
    Impact Score: -0.812  # Highly Negative

    Example 4:
    Headline: "GreenTech Solutions Secures $500 Million Contract"
    Article: GreenTech Solutions has won a substantial contract to outfit several cities with green technology, ensuring revenue growth for the next five years.
    Impact Score: +0.841  # Highly Positive

    Example 5:
    Headline: "DataSecure Inc. Reports Modest Quarterly Earnings Growth"
    Article: DataSecure Inc. reported a slight increase in earnings this quarter, meeting but not exceeding market expectations.
    Impact Score: +0.304  # Neutral Positive

    Example 6:
    Headline: "MediCare Health Faces Regulatory Scrutiny Over Billing Practices"
    Article: MediCare Health is under investigation for potential overbilling Medicare, creating uncertainty around its future earnings.
    Impact Score: -0.247  # Neutral Negative

    Your Article:
    Headline: "{headline}"
    Article: "{article}"

    Evaluate the article and headline and generate a numeric score for its impact on the stock market based on the following scale:
    - Highly Positive: 0.7 to 1
    - Positive: 0.5 to 0.699
    - Neutral Positive: 0.1 to 0.499
    - Neutral: -0.1 to 0.1 
    - Neutral Negative: -0.499 to -0.1
    - Negative: -0.5 to -0.699
    - Highly Negative: -0.7 to -1
    The scores should follow a normal distribution similar to the bell curve, with significant deviations from the center. Ensure the values have three significant figures. Avoid clustering scores too closely around the center.
    you need to be more confident, do not rely on 0.4-0.7 be bold, be strong and think. don't fall into repetition
    don't be afraid to be strongly negative or positive, or even strongly neutral
    Only provide the numeric score as a sole float with no other characters except the sign, period, and integers that make the number.
    """,
)

score_chain = LLMChain(llm=llm, prompt=score_prompt)

def Di(headline, article):
    result = score_chain.invoke({"headline": headline, "article": article})
    print("Direct score:", float(result['text']))
