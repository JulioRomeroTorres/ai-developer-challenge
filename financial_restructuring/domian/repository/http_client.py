import requests
import google.oauth2.id_token
import google.auth.transport.requests  
import time
from financial_restructuring.domian.constants.domain_constants import DEFAULT_EXPIRATION_TIME
from typing import Dict, Any, TypeVar, Type, Optional, Union

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

GenericJsonReponse = Dict[str, Any]
UnionModelJsonResponse = Union[GenericJsonReponse,T]

class HttpClient():
    def __init__(self, 
                    base_url: str,
                    expiration_token_time: int = DEFAULT_EXPIRATION_TIME):
        
        super().__init__()
        self.base_url = base_url
        self.token = None
        self.token_expiry = 0
        self.expiration_token_time = expiration_token_time
    
    def _get_bearer_token(self): 
        request = google.auth.transport.requests.Request()
        target_audience = self.base_url
        id_token = google.oauth2.id_token.fetch_id_token(request, target_audience)
        return id_token
    
    def get_access_token(self):
        if self.token is None or time.time() > self.token_expiry:
            self.token = self._get_bearer_token()
            self.token_expiry = time.time() + self.expiration_token_time
        
        return self.token
    
    def _get_headers(self):

        return {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }

    def valid_http_response(self, response):
        if response.status_code < 400:
            return response.json()
        
        response.raise_for_status()

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)

        return self.valid_http_response(response)


    def post(self, endpoint, data=None, json=None, files=None, model_response: Optional[Type[T]] = None) -> UnionModelJsonResponse:
        url = f"{self.base_url}/{endpoint}"
            
        response = requests.post(
            url,  
            data=data, 
            json=json, 
            files=files)

        valid_json_response = self.valid_http_response(response)
        self.logger.log_text(f"valid_json_response {valid_json_response}")
        if model_response is not None:
            return model_response(**valid_json_response)
        return valid_json_response
    
    
    def _dict_to_model(json_response: Dict[str, Any], pydantic_model: Type[T]) -> T:
        return pydantic_model(**json_response)