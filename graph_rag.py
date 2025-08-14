"""
GraphRAG Implementation for UAT Testing
======================================

Local GraphRAG implementation that works entirely within the CDSW environment
without external API calls. Uses ChromaDB for vector storage and NetworkX for
knowledge graph construction.
"""

import re
import hashlib
import json
from typing import List, Dict, Any, Tuple
import networkx as nx
from collections import defaultdict

class LocalEmbeddingGenerator:
    """Generate simple embeddings locally without external APIs"""
    
    def generate_embedding(self, text: str, dimensions: int = 384) -> List[float]:
        """Generate a simple hash-based embedding for local use"""
        # Create a hash of the text
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        # Convert hash to numeric embedding
        embedding = []
        for i in range(0, min(len(text_hash), dimensions * 2), 2):
            hex_pair = text_hash[i:i+2]
            embedding.append(float(int(hex_pair, 16)) / 255.0)
        
        # Pad to required dimensions
        while len(embedding) < dimensions:
            embedding.append(0.0)
        
        return embedding[:dimensions]

class GraphRAGProcessor:
    """Process UAT test data using GraphRAG techniques"""
    
    def __init__(self):
        self.knowledge_graph = nx.Graph()
        self.embedding_generator = LocalEmbeddingGenerator()
        
        # UAT-specific entity patterns
        self.entity_patterns = {
            'user_roles': r'(?i)\b(?:user|admin|manager|customer|client|tester|developer|analyst)\b',
            'functional_areas': r'(?i)\b(?:login|authentication|payment|reporting|dashboard|search|filter|export|import|notification|alert)\b',
            'test_types': r'(?i)\b(?:functional|regression|integration|unit|performance|security|usability|acceptance)\b',
            'test_scenarios': r'(?i)\b(?:happy path|error handling|boundary|edge case|negative|positive)\b',
            'expected_outcomes': r'(?i)\b(?:success|fail|error|redirect|display|show|hide|enable|disable)\b',
            'ui_elements': r'(?i)\b(?:button|form|field|dropdown|checkbox|radio|table|chart|graph|menu)\b',
            'data_types': r'(?i)\b(?:string|int|integer|float|boolean|date|email|phone|address)\b'
        }
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract UAT-related entities from text"""
        entities = {}
        for category, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities[category] = list(set(matches))  # Remove duplicates
        return entities
    
    def build_knowledge_graph(self, documents: List[Dict[str, Any]]) -> nx.Graph:
        """Build knowledge graph from UAT documents"""
        self.knowledge_graph = nx.Graph()
        
        for doc in documents:
            doc_id = doc.get('id', '')
            content = doc.get('content', '')
            metadata = doc.get('metadata', {})
            
            # Extract entities
            entities = self.extract_entities(content)
            
            # Add document node
            self.knowledge_graph.add_node(f"doc_{doc_id}", type="document", content=content, metadata=metadata)
            
            # Add entity nodes and connect to document
            for category, entity_list in entities.items():
                for entity in entity_list:
                    entity_id = f"{category}:{entity}"
                    if not self.knowledge_graph.has_node(entity_id):
                        self.knowledge_graph.add_node(entity_id, type="entity", category=category)
                    # Connect entity to document
                    self.knowledge_graph.add_edge(entity_id, f"doc_{doc_id}", relationship="mentions")
            
            # Connect related entities within the same document
            all_entities = []
            for entity_list in entities.values():
                all_entities.extend(entity_list)
            
            for i, entity1 in enumerate(all_entities):
                for entity2 in all_entities[i+1:]:
                    if self.knowledge_graph.has_edge(f"entity:{entity1}", f"entity:{entity2}"):
                        # Increment weight if edge exists
                        self.knowledge_graph[f"entity:{entity1}"][f"entity:{entity2}"]['weight'] += 1
                    else:
                        # Create new edge
                        self.knowledge_graph.add_edge(f"entity:{entity1}", f"entity:{entity2}", weight=1)
        
        return self.knowledge_graph
    
    def find_related_documents(self, query: str, documents: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """Find documents related to query using simple text matching"""
        query_entities = self.extract_entities(query)
        query_entity_set = set()
        for entities in query_entities.values():
            query_entity_set.update(entities)
        
        # Score documents based on entity overlap
        doc_scores = []
        for doc in documents:
            content = doc.get('content', '')
            doc_entities = self.extract_entities(content)
            doc_entity_set = set()
            for entities in doc_entities.values():
                doc_entity_set.update(entities)
            
            # Calculate overlap score
            overlap = len(query_entity_set.intersection(doc_entity_set))
            doc_scores.append((doc, overlap))
        
        # Sort by score and return top_k
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        return [doc for doc, score in doc_scores[:top_k] if score > 0]
    
    def generate_test_cases(self, user_story: str, similar_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate test cases based on user story and similar historical cases"""
        test_cases = []
        
        # Extract entities from user story
        entities = self.extract_entities(user_story)
        
        # Create basic test cases from entities
        if entities.get('functional_areas'):
            for area in entities['functional_areas']:
                # Happy path test case
                test_cases.append({
                    'id': f"TC_{len(test_cases)+1:03d}",
                    'type': 'Functional',
                    'scenario': f'Happy path for {area}',
                    'description': f'Verify that {area} works correctly under normal conditions',
                    'steps': [
                        f'Navigate to {area} section',
                        'Perform standard operation',
                        'Verify successful outcome'
                    ],
                    'expected_result': f'{area} functions as expected without errors'
                })
                
                # Error handling test case
                test_cases.append({
                    'id': f"TC_{len(test_cases)+1:03d}",
                    'type': 'Error Handling',
                    'scenario': f'Error handling for {area}',
                    'description': f'Verify that {area} handles errors gracefully',
                    'steps': [
                        f'Navigate to {area} section',
                        'Perform invalid operation',
                        'Verify appropriate error message'
                    ],
                    'expected_result': f'{area} displays meaningful error message and does not crash'
                })
        
        # Enhance with similar cases
        for case in similar_cases:
            case_content = case.get('content', '')
            case_metadata = case.get('metadata', {})
            
            # If similar case has test cases, adapt them
            if 'test_cases' in case_metadata:
                for existing_case in case_metadata['test_cases']:
                    # Adapt existing test case to current user story
                    adapted_case = existing_case.copy()
                    adapted_case['id'] = f"TC_{len(test_cases)+1:03d}"
                    adapted_case['description'] = f"Adapted from historical case: {adapted_case.get('description', '')}"
                    test_cases.append(adapted_case)
        
        return test_cases
    
    def identify_test_variables(self, test_cases: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Identify and categorize test variables from test cases"""
        variables = defaultdict(list)
        
        for case in test_cases:
            # Extract variables from steps
            steps = case.get('steps', [])
            for step in steps:
                # Look for data types in steps
                if re.search(self.entity_patterns['data_types'], step, re.IGNORECASE):
                    variables['input_data'].extend(re.findall(self.entity_patterns['data_types'], step, re.IGNORECASE))
                
                # Look for UI elements
                if re.search(self.entity_patterns['ui_elements'], step, re.IGNORECASE):
                    variables['ui_elements'].extend(re.findall(self.entity_patterns['ui_elements'], step, re.IGNORECASE))
            
            # Extract from expected results
            expected = case.get('expected_result', '')
            if re.search(self.entity_patterns['expected_outcomes'], expected, re.IGNORECASE):
                variables['expected_outcomes'].extend(re.findall(self.entity_patterns['expected_outcomes'], expected, re.IGNORECASE))
        
        # Remove duplicates and return
        return {category: list(set(items)) for category, items in variables.items()}

class ChromaDBManager:
    """Manage local ChromaDB instance for UAT testing"""
    
    def __init__(self, db_path: str = "./uat_chroma_db"):
        self.db_path = db_path
        self.client = None
        self.collection = None
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize ChromaDB client and collection"""
        try:
            import chromadb
            from chromadb.config import Settings
            
            # Initialize client with persistent storage
            self.client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(
                    allow_reset=True,
                    anonymized_telemetry=False
                )
            )
            
            # Get or create collection
            try:
                self.collection = self.client.get_collection("uat_test_cases")
            except:
                self.collection = self.client.create_collection("uat_test_cases")
                
        except Exception as e:
            print(f"Warning: Could not initialize ChromaDB: {e}")
            self.client = None
            self.collection = None
    
    def add_documents(self, documents: List[Dict[str, Any]]) -> bool:
        """Add documents to ChromaDB"""
        if not self.collection:
            return False
        
        try:
            ids = []
            contents = []
            metadatas = []
            embeddings = []
            
            embedding_generator = LocalEmbeddingGenerator()
            
            for doc in documents:
                doc_id = doc.get('id', str(hash(doc.get('content', ''))))
                content = doc.get('content', '')
                metadata = doc.get('metadata', {})
                
                ids.append(doc_id)
                contents.append(content)
                metadatas.append(metadata)
                
                # Generate embedding
                embedding = embedding_generator.generate_embedding(content)
                embeddings.append(embedding)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                documents=contents,
                metadatas=metadatas,
                embeddings=embeddings
            )
            
            return True
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {e}")
            return False
    
    def query_documents(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Query documents from ChromaDB"""
        if not self.collection:
            return []
        
        try:
            embedding_generator = LocalEmbeddingGenerator()
            query_embedding = embedding_generator.generate_embedding(query_text)
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    'id': results['ids'][0][i],
                    'content': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i] if results['metadatas'][0] else {},
                    'distance': results['distances'][0][i] if results['distances'][0] else 0.0
                })
            
            return formatted_results
        except Exception as e:
            print(f"Error querying documents from ChromaDB: {e}")
            return []

# Example usage
if __name__ == "__main__":
    # Example of how to use the GraphRAG processor
    processor = GraphRAGProcessor()
    
    # Sample user story
    user_story = "As a customer, I want to login to the system so that I can access my account information"
    
    # Sample historical documents
    documents = [
        {
            'id': '1',
            'content': 'Test login functionality with valid credentials',
            'metadata': {
                'test_cases': [
                    {
                        'type': 'Functional',
                        'scenario': 'Valid login',
                        'description': 'User can login with correct username and password',
                        'steps': ['Enter valid username', 'Enter valid password', 'Click login button'],
                        'expected_result': 'User is redirected to dashboard'
                    }
                ]
            }
        }
    ]
    
    # Build knowledge graph
    graph = processor.build_knowledge_graph(documents)
    print(f"Knowledge graph built with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
    
    # Generate test cases
    similar_cases = documents  # In practice, these would come from ChromaDB
    test_cases = processor.generate_test_cases(user_story, similar_cases)
    print(f"Generated {len(test_cases)} test cases")
    
    # Identify variables
    variables = processor.identify_test_variables(test_cases)
    print(f"Identified variables: {variables}")
