import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=0.7)
llmforscore = ChatOpenAI(api_key=openai_api_key, model="gpt-4o", temperature=1.5)

thought_prompt = PromptTemplate(
    input_variables=["headline", "article"],
    template="""
    no formatting and extra text
    Headline: {headline}
    Article: {article}
    Generate the top 5 initial thoughts based on the news article.
    """,
)

branch_prompt = PromptTemplate(
    input_variables=["thought"],
    template="""
    no formatting and extra text
    Thought: {thought}
    Generate further insights and explanations for this thought.
    """,
)

score_prompt = PromptTemplate(
    input_variables=["thought", "explanation"],
    template="""
    no formatting and extra text
     your task is to analyze and predict the potential impact of this text content on the respective company's stock price. Use the following detailed guidelines to assign a value on a scale from -1 to 1, where -1 signifies a strong prediction of a decrease in stock price, 1 signifies a strong prediction of an increase in stock price, and values in between indicate varying degrees of confidence in the stock's movement direction
    Thought: {thought}
    Explanation: {explanation}
    Evaluate the explanation and generate a numeric score(with three s.f. ) for its impact on the stock market based on the following scale:
    - Highly Positive News (0.7 to 1): Significant events that will likely lead to increased revenue, market share, or competitive advantage.

    - Positive News (0.5 to 0.699): Events that are likely to have a good impact on the company's performance but are not game-changers.

    - Neutral to Slightly Positive/Negative News (0.1 to 0.499 and -0.1 to -0.499): News with uncertain impacts, speculative developments, or minor updates.

    - Negative News (-0.5 to -0.699): Events likely to negatively affect the company's performance in the short to medium term.

    - Highly Negative News (-0.7 to -1): Major events that could significantly damage the company's reputation, financial health, or market position.

    Example
    HEADLINE: XYZ Corporation Reports Breakthrough in Battery Technology
    VALUE: 0.867

    Use this approach to provide a concise and accurate prediction of how news articles might impact stock prices, utilizing the entire scale for differentiation.

    value will always be in three signficant figures!
    Avoid clustering scores too closely around the center. You can be opinionated.
    Only provide the numeric score.
    """,
)
score_prompt = PromptTemplate(
    input_variables=["thought", "explanation"],
    template="""
    no formatting and extra text
    Thought: {thought}
    Explanation: {explanation}
    Evaluate the explanation and generate a numeric score for its impact on the stock market based on the following scale:
    - Highly Positive: 0.7 to 1
    - Positive: 0.5 to 0.699
    - Neutral Positive: 0.1 to 0.499
    - Neutral: -0.1 to 0.1 (ignored)
    - Neutral Negative: -0.499 to -0.1
    - Negative: -0.5 to -0.699
    - Highly Negative: -0.7 to -1
    The scores should follow a normal distribution similar to the bell curve, with significant deviations from the center. Ensure the values have three significant figures. Avoid clustering scores too closely around the center.
    you need to be more confident, do not rely on 0.4-0.7 be bold, be strong and think. don't fall into repetition
    Only provide the numeric score with no other characters except the sign, period, and integers that make the number.
    """,
)

final_prediction_prompt = PromptTemplate(
    input_variables=["thoughts", "branches", "scores"],
    template="""
    no formatting and extra text
    Thoughts: {thoughts}
    Branches: {branches}
    Scores: {scores}
    Aggregate the insights and provide a final prediction based on the best paths or indicate if there are too many conflicting insights.
    - If the scores are mostly in one direction (positive or negative), provide a detailed score.
    - If there are many conflicting scores, provide a score of 0 indicating confusion.
    Only provide the final score.
    """,
)

thought_chain = LLMChain(llm=llm, prompt=thought_prompt)
branch_chain = LLMChain(llm=llm, prompt=branch_prompt)
score_chain = LLMChain(llm=llmforscore, prompt=score_prompt)
final_prediction_chain = LLMChain(llm=llm, prompt=final_prediction_prompt)

def generate_thoughts(headline, article):
    print("Generating Thoughts...")
    response = thought_chain.run({"headline": headline, "article": article})
    try:
        thoughts = response.strip().split('\n')
    except:
        print(response)
        return []
    return [thought.strip() for thought in thoughts if thought.strip()]

def branch_out_thoughts(thought):
    print("Branching Out Thoughts...")
    print("Thought:", thought)
    response = branch_chain.run({"thought": thought})
    try:
        branches = response.strip().split('\n')
    except:
        print(response)
        return []
    return [branch.strip() for branch in branches if branch.strip()]

def score_thought(thought, explanation):
    print("Scoring Thought...")
    print("Thought:", thought)
    print("Explanation:", explanation)

    response = score_chain.run({"thought": thought, "explanation": explanation})
    try:
        score = response.strip()
    except:
        print(response)
        return []
    try:
        score = float(score)
        if -0.1 <= score <= 0.1:
            return "ignored"
    except ValueError:
        pass
    return score

def final_prediction(thoughts, branches, scores):
    print("Final Prediction...")
    positive_scores = []
    negative_scores = []
    for score_list in scores:
        for score in score_list:
            if score != "ignored":
                try:
                    score = float(score)
                except ValueError:
                    continue
                if score > 0:
                    positive_scores.append(score)
                elif score < 0:
                    negative_scores.append(score)
    
    print("scores: ", scores)
    print("positive_scores: ", positive_scores)
    print("negative_scores: ", negative_scores)

    if (len(positive_scores) - len(negative_scores)) in range(-2,2):
        final_score = 0  # Conflicting insights
    else:
        final_score = (sum(positive_scores) + sum(negative_scores)) / (len(positive_scores) + len(negative_scores))

    return round(final_score, 3)

def analyze_article(headline, article):
    print("Analyzing Article...")
    print("Headline:", headline)
    thoughts = generate_thoughts(headline, article)
    
    all_branches = []
    all_scores = []
    
    for thought in thoughts:
        branches = branch_out_thoughts(thought)
        all_branches.append(branches)
        
        scores = []
        for branch in branches:
            score = score_thought(thought, branch)
            scores.append(score)
        
        all_scores.append(scores)
    
    prediction = final_prediction(thoughts, all_branches, all_scores)
    
    return prediction

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
print(result)

