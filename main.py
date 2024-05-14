import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI language model with chat model and optimum temperature
llm = ChatOpenAI(api_key=openai_api_key, model="gpt-4", temperature=0.3)

# Define prompt templates for each step
thought_prompt = PromptTemplate(
    input_variables=["headline", "article"],
    template="""
    Headline: {headline}
    Article: {article}
    Generate the top 5 initial thoughts based on the news article.
    """,
)

branch_prompt = PromptTemplate(
    input_variables=["thought"],
    template="""
    Thought: {thought}
    Generate further insights and explanations for this thought.
    """,
)

score_prompt = PromptTemplate(
    input_variables=["thought", "explanation"],
    template="""
    Thought: {thought}
    Explanation: {explanation}
    Evaluate the explanation and generate a numeric score(with three s.f. ) for its impact on the stock market based on the following scale:
    - Highly Positive (0.7 to 1)
    - Positive (0.5 to 0.699)
    - Neutral Positive (0.1 to 0.499)
    - Neutral (-0.1 to 0.1) (ignored)
    - Neutral Negative (-0.499 to -0.1)
    - Negative (-0.5 to -0.699)
    - Highly Negative (-0.7 to -1)
    Only provide the score.
    """,
)

final_prediction_prompt = PromptTemplate(
    input_variables=["thoughts", "branches", "scores"],
    template="""
    Thoughts: {thoughts}
    Branches: {branches}
    Scores: {scores}
    Aggregate the insights and provide a final prediction based on the best paths or indicate if there are too many conflicting insights.
    - If the scores are mostly in one direction (positive or negative), provide a detailed score.
    - If there are many conflicting scores, provide a score of 0 indicating confusion.
    Only provide the final score.
    """,
)

# Create the conversation chains with the prompt templates
thought_chain = LLMChain(llm=llm, prompt=thought_prompt)
branch_chain = LLMChain(llm=llm, prompt=branch_prompt)
score_chain = LLMChain(llm=llm, prompt=score_prompt)
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
    # Convert score to float and ignore if it's in the neutral range
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
                score = float(score)
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
    # Step 1: Generate Top 5 Initial Thoughts
    thoughts = generate_thoughts(headline, article)
    
    all_branches = []
    all_scores = []
    
    # Step 2 and Step 3: Branch Out and Score Each Thought
    for thought in thoughts:
        branches = branch_out_thoughts(thought)
        all_branches.append(branches)
        
        scores = []
        for branch in branches:
            score = score_thought(thought, branch)
            scores.append(score)
        
        all_scores.append(scores)
    
    # Step 4: Aggregate Insights and Provide Final Prediction
    prediction = final_prediction(thoughts, all_branches, all_scores)
    
    return prediction

# Example usage
headline = "XYZ Corporation Reports Breakthrough in Battery Technology"
article = """
XYZ Corporation has announced a significant breakthrough in battery technology that could revolutionize the electric vehicle market. The new technology promises to increase battery efficiency by 50%, reduce charging time by half, and extend the overall lifespan of the batteries. This innovation is expected to give XYZ Corporation a competitive edge in the rapidly growing electric vehicle industry.
"""
result = analyze_article(headline, article)
print(result)

