from enum import Enum

BANK_OFFER = [
  {
    "offer_id": "OF-CONSO-24M",
    "product_types_eligible": ["card", "personal"],
    "max_consolidated_balance": 50000,
    "new_rate_pct": 19.9,
    "max_term_months": 24,
    "conditions": "No mora >30 días al momento de la solicitud"
  },
  {
    "offer_id": "OF-CONSO-36M",
    "product_types_eligible": ["card", "personal", "micro"],
    "max_consolidated_balance": 75000,
    "new_rate_pct": 17.5,
    "max_term_months": 36,
    "conditions": "Score > 650 y sin mora activa"
  }
]

class OpenAiModels(str, Enum):
  GPT_MINI = "gpt-4o-mini"

DEFAULT_EXPIRATION_TIME = 1000