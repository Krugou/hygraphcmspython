"""
Hygraph CMS Client for interacting with Hygraph Content API
"""
import requests
from typing import Dict, List, Any, Optional


class HygraphClient:
    """Client for interacting with Hygraph CMS API"""
    
    def __init__(self, endpoint: str, token: str):
        """
        Initialize Hygraph client
        
        Args:
            endpoint: Hygraph API endpoint URL
            token: API authentication token
        """
        self.endpoint = endpoint
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    
    def execute_query(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Execute a GraphQL query
        
        Args:
            query: GraphQL query string
            variables: Optional variables for the query
            
        Returns:
            API response data
        """
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
            
        response = requests.post(
            self.endpoint,
            json=payload,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_all_content(self, model_name: str) -> List[Dict[str, Any]]:
        """
        Get all content for a specific model
        
        Args:
            model_name: Name of the content model (e.g., 'translations', 'posts')
            
        Returns:
            List of content items
        """
        query = f"""
        query {{
            {model_name}s {{
                id
                ... on Node {{
                    id
                }}
            }}
        }}
        """
        
        try:
            result = self.execute_query(query)
            return result.get("data", {}).get(f"{model_name}s", [])
        except Exception as e:
            raise Exception(f"Error fetching content: {str(e)}")
    
    def get_translations(self) -> List[Dict[str, Any]]:
        """
        Get all translations from the CMS
        
        Returns:
            List of translation items
        """
        query = """
        query {
            translations {
                id
                key
                value
                locale
                createdAt
                updatedAt
            }
        }
        """
        
        try:
            result = self.execute_query(query)
            return result.get("data", {}).get("translations", [])
        except Exception as e:
            raise Exception(f"Error fetching translations: {str(e)}")
    
    def create_translation(self, key: str, value: str, locale: str) -> Dict[str, Any]:
        """
        Create a new translation
        
        Args:
            key: Translation key
            value: Translation value
            locale: Locale code (e.g., 'en', 'fi')
            
        Returns:
            Created translation data
        """
        mutation = """
        mutation CreateTranslation($key: String!, $value: String!, $locale: String!) {
            createTranslation(data: {key: $key, value: $value, locale: $locale}) {
                id
                key
                value
                locale
            }
        }
        """
        
        variables = {
            "key": key,
            "value": value,
            "locale": locale
        }
        
        try:
            result = self.execute_query(mutation, variables)
            return result.get("data", {}).get("createTranslation", {})
        except Exception as e:
            raise Exception(f"Error creating translation: {str(e)}")
    
    def publish_translation(self, translation_id: str) -> Dict[str, Any]:
        """
        Publish a translation
        
        Args:
            translation_id: ID of the translation to publish
            
        Returns:
            Published translation data
        """
        mutation = """
        mutation PublishTranslation($id: ID!) {
            publishTranslation(where: {id: $id}, to: PUBLISHED) {
                id
            }
        }
        """
        
        variables = {"id": translation_id}
        
        try:
            result = self.execute_query(mutation, variables)
            return result.get("data", {}).get("publishTranslation", {})
        except Exception as e:
            raise Exception(f"Error publishing translation: {str(e)}")
    
    def introspect_schema(self) -> Dict[str, Any]:
        """
        Introspect the GraphQL schema to discover available models
        
        Returns:
            Schema information
        """
        query = """
        query {
            __schema {
                types {
                    name
                    kind
                    fields {
                        name
                        type {
                            name
                            kind
                        }
                    }
                }
            }
        }
        """
        
        try:
            result = self.execute_query(query)
            return result.get("data", {}).get("__schema", {})
        except Exception as e:
            raise Exception(f"Error introspecting schema: {str(e)}")
