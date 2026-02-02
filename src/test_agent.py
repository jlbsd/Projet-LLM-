from agents import Agent, function_tool, Runner
from dotenv import load_dotenv
from upstash_vector import Index
import os

# 1. Chargement de la configuration
load_dotenv()

# 2. Connexion Agent ↔ Vecteurs (RAG)
@function_tool
def recuperer_information(question: str) -> str:
    """Permet de requêter un index avec une question pour récupérer des informations."""
    
    index = Index(
        url=os.getenv("UPSTASH_VECTOR_REST_URL"), 
        token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
    )

    # Execute the query
    query_result = index.query(
        data=question,
        include_metadata=True,
        include_data=True,
        include_vectors=False,
        top_k=3,
    )

    # Concaténer les informations data
    output= " "
    for i in query_result :
        output += i.data + "\n" 
    return output.strip()

# 3. Création de l'agent
agent = Agent(
    name="Jade",
    instructions="Répond en français avec des émojis",   #A modifier si on veut un style différent !
    model="gpt-4.1-nano",
    tools=[recuperer_information],
)


# 4. Interface de dialogue  
def poser_question(question: str):
    result = Runner.run_sync(agent, question)
    return result.final_output




