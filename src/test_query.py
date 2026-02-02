from upstash_vector import Index
import os
from dotenv import load_dotenv

# 1. Chargement de la configuration (.env)
load_dotenv()


# 2. Connexion à l'index Upstash
index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"), 
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)

# 3. Execution d'une requête exemple
# Pour vérifier que l'indexation fonctione
query_result = index.query(
    data="Quelles langues parles-tu ?",
    include_metadata=True,
    include_data=True,
    include_vectors=False,
    top_k=3,
)

# 4. Print le resultat
for result in query_result:
    print("Score:", result.score)
    print("ID:", result.id)
    print("Vector:", result.vector)
    print("Metadata:", result.metadata)
    print("Data:", result.data)
    print("-----"*50)