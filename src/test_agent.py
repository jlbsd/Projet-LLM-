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

    # Recherche sémantique
    query_result = index.query(
        data=question,
        include_metadata=True,
        include_data=True,
        include_vectors=False,
        top_k=3,
    )

    # Concaténer les données trouvées
    output= " "
    for i in query_result :
        output += i.data + "\n" 
    return output.strip()

# 3. Création de l'agent
agent = Agent(
    name="Jade",
    instructions="Répond en français avec des émojis",   # Style modifiable
    model="gpt-4.1-nano",
    tools=[recuperer_information],
)


# 4. Interface de dialogue  
def poser_question(question: str):
    """ Envoie la question à l'agent et renvoie unniquement la réponse finale """
    result = Runner.run_sync(agent, question)
    return result.final_output




