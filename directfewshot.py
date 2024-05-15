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

def analyze_article(headline, article):
    return score_chain.invoke({"headline": headline, "article": article})

headline = "RBI imposes business curbs on Kotak Bank for IT infra deficiency"
article = """
The bank has been barred from onboarding new customers through online, mobile banking channels, issuing fresh credit cards

The Reserve Bank of India (RBI) on Wednesday directed Kotak Mahindra Bank Ltd. (Kotak Bank) to cease and desist, with immediate effect, from onboarding of new customers through its online and mobile banking channels and issuing fresh credit cards. 


Kotak Bank is however allowed to continue to provide services to its existing customers, including its credit card customers.

“These actions are necessitated based on significant concerns arising out of Reserve Bank’s IT examination of the bank for the years 2022 and 2023 and the continued failure on the part of the bank to address these concerns in a comprehensive and timely manner,” the central bank said in its directive.

“Serious deficiencies and non-compliances were observed in the areas of IT inventory management, patch and change management, user access management, vendor risk management, data security and data leak prevention strategy, business continuity and disaster recovery rigour and drill, etc.,” it said. 

“For two consecutive years, the bank was assessed to be deficient in its IT risk and information security governance, contrary to requirements under regulatory guidelines,” the RBI added.

The banking regulator said during the subsequent assessments, Kotak Bank was found to be “significantly non-compliant” with the corrective action plans issued by the Reserve Bank for the years 2022 and 2023, as the compliances submitted by the bank were found to be either “inadequate, incorrect or not sustained.”

In the absence of a robust IT infrastructure and IT risk management framework, the bank’s Core Banking System (CBS) and its online and digital banking channels have suffered frequent and significant outages in the last two years, the recent one being a service disruption on April 15, 2024, resulting in serious customer inconveniences, it added. 

“The bank is found to be materially deficient in building necessary operational resilience on account of its failure to build IT systems and controls commensurate with its growth,” the regulator observed. 

‘Far from satisfactory’
The RBI said in the past two years it had been in continuous high-level engagement with the bank on all these concerns with a view to strengthening its IT resilience, but the outcomes had been far from satisfactory. 

“It is also observed that, of late, there has been rapid growth in the volume of the bank’s digital transactions, including transactions pertaining to credit cards, which is building further load on the IT systems,” the RBI said. 

Therefore, the RBI decided to place certain business restrictions on Kotak Bank in the interest of customers and to prevent any possible prolonged outage which might seriously impact not only the bank’s ability to render efficient customer service but also the financial ecosystem of digital banking and payment systems.

Kotak Bank through an external agency in a statement said, “The bank has taken measures for adoption of new technologies to strengthen its IT systems and will continue to work with the RBI to swiftly resolve balance issues at the earliest.”

“We want to reassure our existing customers of uninterrupted services, including credit card, mobile and net banking. Our branches continue to welcome and onboard new customers, providing them with all the services, apart from issuance of new credit cards.”
"""

result = analyze_article(headline, article)
print("Impact Score:", float(result['text']))
