# helpers/vector_search.py

import os
import logging
from neo4j import GraphDatabase
from helpers.embed_text import embed_text

# Configure logging to show debug messages
logging.basicConfig(level=logging.INFO)

# Neo4j connection parameters
# TODO this needs moving to a database connector, this is repeated endlessly.
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j-db-container")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


def fetch_similar_chunks(tx, query_embedding, top_n, document_id=0):
    """
    Runs a Cypher query to compute cosine similarity between the query embedding
    and each Chunk node's stored vector.
    If document_id is provided, restricts chunks to those with matching document_id.
    """
    cypher_query = (
        """
    WITH $query_embedding AS query
    MATCH (c:Chunk)
    WHERE c.vector IS NOT NULL
    """
        + (
            """
    AND c.document_id = $document_id
    """
            if document_id != 0
            else ""
        )
        + """
    WITH c, gds.similarity.cosine(query, c.vector) AS similarity
    ORDER BY similarity DESC
    LIMIT $top_n
    OPTIONAL MATCH (c)-[:BELONGS_TO]->(cu:CorporateUnderstanding)
    OPTIONAL MATCH path = (cu)-[:CONNECTED_TO*0..]->(related:CorporateUnderstanding)
    RETURN c, similarity, collect(DISTINCT cu) AS directly_linked,
           collect(DISTINCT related) AS full_cukg;
    """
    )

    logging.debug("Executing Cypher Query:\n%s", cypher_query)

    result = tx.run(
        cypher_query,
        query_embedding=query_embedding,
        top_n=top_n,
        document_id=document_id,
    )

    results = []
    for record in result:
        chunk_node = record["c"]
        similarity = record["similarity"]

        directly_linked = (
            [
                {"id": entity.id, "properties": dict(entity)}
                for entity in record["directly_linked"]
            ]
            if record["directly_linked"]
            else []
        )

        full_cukg = (
            [
                {"id": entity.id, "properties": dict(entity)}
                for entity in record["full_cukg"]
            ]
            if record["full_cukg"]
            else []
        )

        results.append(
            {
                "id": chunk_node.id,
                "properties": dict(chunk_node),
                "similarity": similarity,
                "directly_linked": directly_linked,
                "full_cukg": full_cukg,
            }
        )

    logging.debug("Database response: %s", results)

    return results


def vector_search(query: str, top_n: int = 5, document_id: int = 0):
    """
    Computes the embedding for the provided query and retrieves the top_n similar chunks from Neo4j.
    """
    logging.debug("Received query: %s", query)

    query_embedding = embed_text(query[0])
    logging.debug("Computed query embedding: %s", query_embedding[0])

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    try:
        with driver.session() as session:
            results = session.read_transaction(
                fetch_similar_chunks, query_embedding[0], top_n, document_id
            )
        return results
    finally:
        driver.close()
