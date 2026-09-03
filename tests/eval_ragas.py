"""
Phase 6 — Formal Agent Evaluation using RAGAS
Evaluates Context Precision, Context Recall, and Faithfulness.
"""
from ragas import evaluate
from ragas.metrics import context_precision, context_recall, faithfulness
from datasets import Dataset
from src.utils.logger import get_logger
from src.langgraph.graph import run_agent

log = get_logger(__name__)

# A small golden dataset of test questions and ground truth
test_cases = [
    {"question": "What is the total revenue?", "ground_truth": "£20,476,634.02"},
    {"question": "Which customer segment generates most revenue?", "ground_truth": "Potential Loyalists"},
    {"question": "What month is operationally critical?", "ground_truth": "November"},
    {"question": "What is the only true Superstar product?", "ground_truth": "CREAM HANGING HEART T-LIGHT HOLDER"},
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
    
    # Run RAGAS evaluation
    print("\nRunning RAGAS evaluation metrics...", flush=True)
    scores = evaluate(dataset, metrics=[context_precision, context_recall, faithfulness])
    
    print("\n" + "="*50, flush=True)
    print("📊 RAGAS EVALUATION RESULTS", flush=True)
    print("="*50, flush=True)
    print(f"Context Precision: {scores['context_precision']:.2f}", flush=True)
    print(f"Context Recall:    {scores['context_recall']:.2f}", flush=True)
    print(f"Faithfulness:      {scores['faithfulness']:.2f}", flush=True)
    print("="*50 + "\n", flush=True)

if __name__ == "__main__":
    run_ragas_evaluation()