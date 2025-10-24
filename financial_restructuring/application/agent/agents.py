from langchain_google_genai import ChatGoogleGenerativeAI
from financial_restructuring.domian.constants.env_constants import GEMINI_API_KEY
from .prompts import ROUTER_SYSTEM_INST, OPTIMIZER_SYSTEM_INST, WELCOME_SYSTEM_INST, FALLBACK_SYSTEM_INST, HUMANIZER_SYST_INST, EXTRACTER_SYSTEM_INST

router_agent = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    #system_instruction=ROUTER_SYSTEM_INST
)

optimizer_agent = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    #system_instruction=OPTIMIZER_SYSTEM_INST
)

welcome_agent = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    #system_instruction=WELCOME_SYSTEM_INST
)

fallback_agent = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    #system_instruction=FALLBACK_SYSTEM_INST
)

humanizer_agent = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    #system_instruction=HUMANIZER_SYST_INST
)

extracter_agent = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0,
    #system_instruction=EXTRACTER_SYSTEM_INST
)