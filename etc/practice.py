#!/usr/bin/env python

rdr-mpc.py - A MPC server for the Distant Reader

# Eric Lease Morgan <eric_morgan@infomotions.com>
# (c) Infomotions, LLC; distributed under a GNU Public License

# April 27, 2026 - was kinda independently started on my own from the command line


# initialize
from mcp.server.fastmcp import FastMCP
import sqlite3
import json
import ollama
from pathlib import Path
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#mcp = FastMCP("distant-reader-ollama", version="1.0.0")
mcp = FastMCP("distant-reader-ollama")

class DistantReaderOllamaService:
    def __init__(self, carrels_base_path: str = "/path/to/carrels"):
        self.carrels_base_path = Path(carrels_base_path)
        self.ollama_client = ollama.Client()
        
    def get_carrel_db(self, carrel_name: str) -> sqlite3.Connection:
        """Get SQLite connection for a specific carrel"""
        carrel_path = self.carrels_base_path / carrel_name / "study-carrel.db"
        if not carrel_path.exists():
            raise FileNotFoundError(f"Carrel database not found: {carrel_path}")
        return sqlite3.connect(carrel_path)
    
    def query_ollama(self, prompt: str, model: str = "llama3") -> str:
        """Query Ollama with a prompt"""
        try:
            response = self.ollama_client.chat(model=model, messages=[
                {"role": "user", "content": prompt}
            ])
            return response['message']['content']
        except Exception as e:
            logger.error(f"Ollama query failed: {e}")
            return f"Error querying Ollama: {e}"

# Initialize the service
service = DistantReaderOllamaService()


##################

@mcp.tool()
def semantic_search(carrel_name: str, query: str, limit: int = 10) -> str:
    """Perform semantic search across carrel content using Ollama"""
    # First get relevant content from carrel
    carrel = service.get_carrel_db(carrel_name)
    cursor = carrel.cursor()
    
    # Simple keyword search to get initial results
    cursor.execute("""
        SELECT id, txt, title FROM txt 
        WHERE txt LIKE ? LIMIT 20
    """, (f"%{query}%",))
    results = cursor.fetchall()
    
    if not results:
        return "No results found for your query"
    
    # Use Ollama to rank and summarize results
    context = "\n".join([f"Document {title}: {text[:500]}..." for id, text, title in results])
    
    ollama_prompt = f"""
    Based on the following documents, answer this query: "{query}"
    
    Documents:
    {context}
    
    Please provide:
    1. A concise answer to the query
    2. Which documents are most relevant and why
    3. Key insights from the relevant documents
    
    Return your response in JSON format.
    """
    
    return service.query_ollama(ollama_prompt)

@mcp.tool()
def analyze_entities_with_llm(carrel_name: str, entity_type: str = "all") -> str:
    """Extract and analyze entities using Ollama"""
    carrel = service.get_carrel_db(carrel_name)
    cursor = carrel.cursor()
    
    # Get entities from database
    if entity_type == "all":
        cursor.execute("""
            SELECT entity, type, COUNT(*) as frequency
            FROM ent GROUP BY entity, type ORDER BY frequency DESC LIMIT 50
        """)
    else:
        cursor.execute("""
            SELECT entity, COUNT(*) as frequency
            FROM ent WHERE type = ? GROUP BY entity ORDER BY frequency DESC LIMIT 50
        """, (entity_type,))
    
    entities = cursor.fetchall()
    
    # Analyze with Ollama
    entities_text = "\n".join([f"{entity} ({type}): {freq} occurrences" 
                             for entity, type, freq in entities])
    
    ollama_prompt = f"""
    Analyze these entities from a document collection:
    
    {entities_text}
    
    Provide:
    1. Main themes and topics in this collection
    2. Most significant entities and their relationships
    3. Any interesting patterns or insights
    4. Potential research questions this data suggests
    
    Return your analysis in structured JSON format.
    """
    
    return service.query_ollama(ollama_prompt)

########################

@mcp.tool()
def generate_research_summary(carrel_name: str, research_question: str) -> str:
    """Generate a research summary using carrel content and Ollama"""
    carrel = service.get_carrel_db(carrel_name)
    cursor = carrel.cursor()
    
    # Get relevant content
    cursor.execute("""
        SELECT txt, title FROM txt 
        WHERE txt LIKE ? LIMIT 15
    """, (f"%{research_question}%",))
    relevant_docs = cursor.fetchall()
    
    # Get key entities
    cursor.execute("""
        SELECT entity, type, COUNT(*) as freq
        FROM ent GROUP BY entity, type ORDER BY freq DESC LIMIT 20
    """)
    key_entities = cursor.fetchall()
    
    # Prepare context for Ollama
    context = f"Research Question: {research_question}\n\n"
    context += "Relevant Documents:\n"
    for text, title in relevant_docs:
        context += f"- {title}: {text[:300]}...\n"
    
    context += "\nKey Entities:\n"
    for entity, type, freq in key_entities:
        context += f"- {entity} ({type}): {freq}x\n"
    
    ollama_prompt = f"""
    Based on this research context:
    
    {context}
    
    Please generate a comprehensive research summary that includes:
    1. Executive summary answering the research question
    2. Key findings and evidence from the documents
    3. Important entities and their significance
    4. Limitations and gaps in the current data
    5. Suggestions for further research
    
    Format your response as a well-structured research report.
    """
    
    return service.query_ollama(ollama_prompt)

@mcp.tool()
def compare_carrels_llm(carrel1: str, carrel2: str, aspect: str = "themes") -> str:
    """Compare two carrels using Ollama analysis"""
    def get_carrel_summary(carrel_name):
        carrel = service.get_carrel_db(carrel_name)
        cursor = carrel.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM txt")
        doc_count = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT entity, type, COUNT(*) as freq
            FROM ent GROUP BY entity, type ORDER BY freq DESC LIMIT 10
        """)
        top_entities = cursor.fetchall()
        
        cursor.execute("""
            SELECT gram, COUNT(*) as freq
            FROM wrd WHERE LENGTH(gram) BETWEEN 2 AND 4
            ORDER BY freq DESC LIMIT 15
        """)
        top_ngrams = cursor.fetchall()
        
        return {
            "doc_count": doc_count,
            "top_entities": top_entities,
            "top_ngrams": top_ngrams
        }
    
    summary1 = get_carrel_summary(carrel1)
    summary2 = get_carrel_summary(carrel2)
    
    ollama_prompt = f"""
    Compare these two document collections:
    
    Collection 1: {carrel1}
    - Documents: {summary1['doc_count']}
    - Top Entities: {summary1['top_entities']}
    - Top Phrases: {summary1['top_ngrams']}
    
    Collection 2: {carrel2}
    - Documents: {summary2['doc_count']}
    - Top Entities: {summary2['top_entities']}
    - Top Phrases: {summary2['top_ngrams']}
    
    Analyze their similarities and differences in terms of:
    1. Main themes and topics
    2. Writing style and terminology
    3. Key entities and concepts
    4. Potential relationships between the collections
    
    Provide a detailed comparative analysis.
    """
    
    return service.query_ollama(ollama_prompt)


##########################

@mcp.resource("distant-reader://carrels/{carrel_name}/statistics")
def get_carrel_statistics(carrel_name: str) -> str:
    """Get comprehensive statistics about a carrel"""
    try:
        carrel = service.get_carrel_db(carrel_name)
        cursor = carrel.cursor()
        
        stats = {}
        
        # Document count
        cursor.execute("SELECT COUNT(*) FROM txt")
        stats['document_count'] = cursor.fetchone()[0]
        
        # Word count
        cursor.execute("SELECT SUM(LENGTH(txt) - LENGTH(REPLACE(txt, ' ', '')) + 1) FROM txt")
        stats['word_count'] = cursor.fetchone()[0]
        
        # Entity statistics
        cursor.execute("SELECT type, COUNT(*) FROM ent GROUP BY type")
        stats['entities_by_type'] = dict(cursor.fetchall())
        
        # N-gram statistics
        cursor.execute("SELECT LENGTH(gram), COUNT(*) FROM wrd GROUP BY LENGTH(gram)")
        stats['ngrams_by_length'] = dict(cursor.fetchall())
        
        return json.dumps(stats, indent=2)
        
    except Exception as e:
        return f"Error retrieving statistics: {e}"

'''@mcp.resource("distant-reader://carrels/{carrel_name}/top_entities")
def get_top_entities(carrel_name: str, limit: int = 20) -> str:
    """Get top entities from a carrel"""
    try:
        carrel = service.get_carrel_db(carrel_name)
        cursor = carrel.cursor()
        
        cursor.execute("""
            SELECT entity, type, COUNT(*) as frequency
            FROM ent GROUP BY entity, type ORDER BY frequency DESC LIMIT ?
        """, (limit,))
        
        results = []
        for entity, type, freq in cursor.fetchall():
            results.append({
                "entity": entity,
                "type": type,
                "frequency": freq
            })
        
        return json.dumps(results, indent=2)
        
    except Exception as e:
        return f"Error retrieving entities: {e}"
'''

###########################

@mcp.prompt()
def research_analysis_template(carrel_name: str, research_topic: str) -> str:
    """Template for comprehensive research analysis"""
    return f"""
    Conduct a comprehensive analysis of the research topic "{research_topic}"
    using the study carrel "{carrel_name}".
    
    Please use the available tools to:
    1. Search for relevant documents about {research_topic}
    2. Extract key entities and concepts
    3. Analyze the content with Ollama
    4. Generate a structured research report
    
    The report should include:
    - Executive summary
    - Key findings with supporting evidence
    - Important entities and their relationships
    - Conclusions and recommendations
    - Suggestions for further research
    """

@mcp.prompt()
def literature_review_template(carrel_name: str, topic: str) -> str:
    """Template for literature review generation"""
    return f"""
    Generate a literature review on "{topic}" using the study carrel "{carrel_name}".
    
    Steps to follow:
    1. Search for relevant documents about {topic}
    2. Identify key authors, concepts, and methodologies
    3. Analyze trends and patterns in the literature
    4. Identify gaps and controversies
    5. Synthesize the findings into a coherent review
    
    The literature review should be structured with:
    - Introduction and background
    - Thematic organization of existing research
    - Critical analysis of methodologies and findings
    - Identification of research gaps
    - Conclusion and future directions
    """

###########################

# Configuration
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    CARRELS_BASE_PATH = os.getenv('CARRELS_BASE_PATH', '/path/to/carrels')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')

# Update service initialization
service = DistantReaderOllamaService(Config.CARRELS_BASE_PATH)

# Main execution
if __name__ == "__main__":
    # For local development with stdio
    #mcp.run(transport="stdio")
    
    # For production with HTTP
    mcp.run(transport="streamable-http")


