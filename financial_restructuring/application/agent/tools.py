from langchain_core.tools import tool
from typing import Dict, Any
from financial_restructuring.domian.repository.http_client import HttpClient
from financial_restructuring.domian.constants.env_constants import BASE_BACKEND_URL

JsonResponse = Dict[str, Any]

#@tool
def get_user_information(user_id: str) -> JsonResponse:
    """
    Tool encargada de la obtención de la información credicticia del usuario
    """
    try:
        user_id = user_id.strip()
        print("User ID", user_id)
        response = HttpClient(BASE_BACKEND_URL).get(f"api/financial-restructuring/user/{user_id}/")
        print("Response Get User", response)
        return response
    
    except Exception as error:
        return {"error": f"Error al obtener información del usuarios {error}"}

def get_users() -> JsonResponse:
    """
    Tool encargada de la obtención de la información credicticia del usuario
    """
    try:

        response = HttpClient(BASE_BACKEND_URL).get(f"api/financial-restructuring/users/")
        print("Response Get User", response)
        return response
    
    except Exception as error:
        return {"error": f"Error al obtener información del usuarios {error}"}

#@tool
def generate_optimized_plan(financial_user_information: JsonResponse) -> JsonResponse:
    """
    Tool encargada de generar un plan optimizada según la información del usuario
    """
    try:
        response = HttpClient(BASE_BACKEND_URL).post(f"api/financial-restructuring/optimizer/", json=financial_user_information)
        return response
    except Exception as error:
        return {"error": f"Error al generar el plan óptimo {error}"}    

tools = [get_user_information, generate_optimized_plan]
#tool_map = {tool.name: tool for tool in tools}