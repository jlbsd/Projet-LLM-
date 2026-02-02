import os
import glob
from dotenv import load_dotenv
from upstash_vector import Index

# 1. Chargement des variables d'environnement (.env)
load_dotenv()

# 2. Connexion à l'index Upstash Vector
# Les identifiants sont récupérés depuis le fichier .env
index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL"), 
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN")
)

# 3. Fonction de découpage des markdown en 'morceaux' (chunks)
def chunk_markdown(content, chunk_size=500):
    """
    Découpe le contenu Markdown en morceaux (chunks)[cite: 62].
    Ici, on utilise une logique simple par paragraphe ou par taille.
    """
    # Une approche simple consiste à diviser par sections (titres ##)
    sections = content.split("\n## ")
    chunks = []
    
    for i, section in enumerate(sections):
        if i == 0:
            chunks.append(section.strip())
        else:
            chunks.append(f"## {section.strip()}")
    return chunks

# 4. Ingestion des fichiers Markdown et upsert dans l'index 
def ingest_data():
    # Chemin vers votre dossier de données
    data_path = "Data/*.md"            #Modifier si la structure du fichier change
    files = glob.glob(data_path)
    
    if not files:
        print("Aucun fichier Markdown trouvé dans le dossier 'data/'.")
        return

    print(f"Début de l'indexation de {len(files)} fichiers...")

    for file_path in files:
        file_name = os.path.basename(file_path)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Étape de découpage (Chunking) [cite: 33, 59]
        chunks = chunk_markdown(content)
        
        # boucle pour parcourir la liste
        for idx, chunk in enumerate(chunks, start = 1):
            print(chunk)
            print("----" * 10)

            res = index.upsert(
                vectors=[
                    {
                        "id": f"{file_name}-{idx}",   # ID unique : nom + numéro du chunk
                        "data": chunk,
                        "metadata": {"Name": file_name, "chunk_index": idx}
                    }
                ]
            )

    print("Indexation terminée avec succès !")

if __name__ == "__main__":
    ingest_data()