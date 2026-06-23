from src.executor.query_executor import QueryExecutionEngine
from src.rag.embedder import LocalTextEmbedder
from src.rag.index_schemas import build_and_seed_vector_warehouse
from src.rag.retriever import MetadataGroundingRetriever

from src.llm.groq_client import GroqClient
from src.llm.prompt_templates import SQL_GENERATION_TEMPLATE


print("Loading PostgreSQL...")
executor = QueryExecutionEngine()

print("Loading Embedder...")
embedder = LocalTextEmbedder()

print("Building Chroma Index...")
vector_db = build_and_seed_vector_warehouse(
    executor,
    embedder
)

print("Loading Retriever...")
retriever = MetadataGroundingRetriever(
    vector_db,
    embedder
)

print("Loading Groq...")
groq_client = GroqClient()

user_question = "Show revenue trend for last months"

print("\nUser Question:")
print(user_question)

context = retriever.retrieve_grounding_context(
    user_question,
    top_k=2
)

print("\nRetrieved Context:")
print(context)

prompt = SQL_GENERATION_TEMPLATE.format(
    user_question=user_question,
    context=context
)

sql = groq_client.generate_response(
    prompt
)

print("\nGenerated SQL:")
print(sql)