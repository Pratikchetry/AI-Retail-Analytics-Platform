"""
Phase 6 — Formal Agent Evaluation using RAGAS
Evaluates Context Precision, Context Recall, and Faithfulness.
Uses Groq (Llama 3.3) as the RAGAS judge LLM instead of OpenAI.
"""
import os
from ragas import evaluate
from ragas.metrics import context_precision, context_recall, faithfulness
from datasets import Dataset
from openai import OpenAI
from src.utils.logger import get_logger
from src.langgraph.graph import run_agent

log = get_logger(__name__)

# 1. Configure RAGAS to use Groq instead of OpenAI using the new llm_factory
groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# RAGAS v0.4+ uses llm_factory
try:
    from ragas.llms import llm_factory
    ragas_judge = llm_factory(model="openai/gpt-oss-120b", client=groq_client)
except ImportError:
    # Fallback for slightly older 0.4.x versions
    from ragas.llms.base import LangchainLLMWrapper
    from langchain_openai import ChatOpenAI
    groq_llm = ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),
        model="openai/gpt-oss-120b",
        temperature=0
    )
    ragas_judge = LangchainLLMWrapper(llm=groq_llm)

# A small golden dataset of test questions
test_cases = [
    {"question": "What is the total revenue?", "ground_truth": "£20,476,634.02"},
    {"question": "Which customer segment generates most revenue?", "ground_truth": "Potential Loyalists"},
    {"question": "What month is operationally critical?", "ground_truth": "November"},
    {"question": "What is the only true Superstar product?", "ground_truth": "WHITE HANGING HEART T-LIGHT HOLDER"},
    {"question": "Why did YoY show negative growth?", "ground_truth": "It is a partial year artifact due to December 2011 ending early."}
]

def run_ragas_evaluation():
    eval_data = []
    
    print("Running LangGraph Agent for test cases...", flush=True)
    for case in test_cases:
        # Run your LangGraph agent
        result = run_agent(case["question"])
        
        # RAGAS expects: question, answer, contexts, ground_truth
        eval_data.append({
            "question": case["question"],
            "answer": result.get("answer", ""),
            "contexts": [result.get("evidence", "")], # Using your reasoning evidence as context
            "ground_truth": case["ground_truth"]
        })
    
    # Convert to HuggingFace Dataset (RAGAS requirement)
    dataset = Dataset.from_list(eval_data)
    
    # Run RAGAS evaluation, explicitly passing our Groq judge
    print("\nRunning RAGAS evaluation metrics (using Groq)...", flush=True)
    scores = evaluate(
        dataset, 
        metrics=[context_precision, context_recall, faithfulness],
        llm=ragas_judge
    )
    
    # RAGAS v0.4+ returns a dataset of lists. We need to safely extract and average them.
    if hasattr(scores, 'to_pandas'):
        # If it's a HuggingFace Dataset
        df = scores.to_pandas()
        cp = df['context_precision'].mean()
        cr = df['context_recall'].mean()
        fa = df['faithfulness'].mean()
    else:
        # If it's a standard dictionary of lists
        cp = sum(scores['context_precision']) / len(scores['context_precision'])
        cr = sum(scores['context_recall']) / len(scores['context_recall'])
        fa = sum(scores['faithfulness']) / len(scores['faithfulness'])
    
    print("\n" + "="*50, flush=True)
    print("📊 RAGAS EVALUATION RESULTS", flush=True)
    print("="*50, flush=True)
    print(f"Context Precision: {cp:.2f}", flush=True)
    print(f"Context Recall:    {cr:.2f}", flush=True)
    print(f"Faithfulness:      {fa:.2f}", flush=True)
    print("="*50 + "\n", flush=True)

if __name__ == "__main__":
    run_ragas_evaluation()