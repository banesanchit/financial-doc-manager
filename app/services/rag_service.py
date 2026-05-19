import pdfplumber

from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)

from langchain.text_splitter import (
    RecursiveCharacterTextSplitter
)

from qdrant_client import QdrantClient

from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct
)

import uuid

# EMBEDDING MODEL

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# RERANKER MODEL

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

# QDRANT VECTOR DB

qdrant = QdrantClient(":memory:")

COLLECTION_NAME = "financial_documents"

qdrant.recreate_collection(

    collection_name=COLLECTION_NAME,

    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

# PDF TEXT EXTRACTION

def extract_text_from_pdf(pdf_path):

    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:

                full_text += text + "\n"

    return full_text

# TEXT CHUNKING

def chunk_text(text):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    return chunks

# STORE EMBEDDINGS

def store_embeddings(document_id, text):

    chunks = chunk_text(text)

    points = []

    for chunk in chunks:

        embedding = model.encode(chunk).tolist()

        point = PointStruct(

            id=str(uuid.uuid4()),

            vector=embedding,

            payload={

                "document_id": document_id,

                "text": chunk
            }
        )

        points.append(point)

    qdrant.upsert(

        collection_name=COLLECTION_NAME,

        points=points
    )

# SEMANTIC SEARCH + RERANKING

def semantic_search(query):

    # QUERY EMBEDDING

    query_embedding = model.encode(
        query
    ).tolist()

    # VECTOR SEARCH

    search_result = qdrant.search(

        collection_name=COLLECTION_NAME,

        query_vector=query_embedding,

        limit=20
    )

    # PREPARE QUERY-CHUNK PAIRS

    pairs = []

    for result in search_result:

        pairs.append([

            query,

            result.payload["text"]
        ])

    # RERANKING SCORES

    scores = reranker.predict(pairs)

    reranked_results = []

    for score, result in zip(
        scores,
        search_result
    ):

        reranked_results.append({

            "score": float(score),

            "document_id": result.payload[
                "document_id"
            ],

            "text": result.payload["text"]
        })

    # SORT BY BEST SCORE

    reranked_results = sorted(

        reranked_results,

        key=lambda x: x["score"],

        reverse=True
    )

    # TOP 5 BEST RESULTS

    top_results = reranked_results[:5]

    return top_results