from financial_restructuring.domian.constants.domain_constants import BANK_OFFER
from typing import Dict, List, Any, Optional
import math

class FinancialOptimizer:
    def __init__(self, 
            monthly_income_avg,
            income_variability_pct,
            essential_expenses_avg,
            loans, cards, payment_histories,
            credit_score_history
            ):
        self.monthly_income_avg = monthly_income_avg
        self.income_variability_pct = income_variability_pct
        self.essential_expenses_avg = essential_expenses_avg
        self.loans = loans
        self.cards = cards
        self.payment_histories = payment_histories  
        self.credit_score_history = credit_score_history     
        pass

    def optimize_customer(self) -> Dict[str, Any]:
        """
        Cálculo determinista de escenarios financieros para restructuración de deuda.
        """

        offers = BANK_OFFER

        income = self.monthly_income_avg
        essential_expenses = self.essential_expenses_avg
        income_var_pct = self.income_variability_pct

        buffer = essential_expenses * (1 + income_var_pct / 100)
        available_payment = income - buffer

        if available_payment <= 0:
            raise  ValueError("Cliente sin capacidad de pago")

        credit_score = self.credit_score_history[-1]["credit_score"] if self.credit_score_history else 600

        debts = []

        for loan in self.loans:
            min_payment = self.amortized_payment(
                loan["principal"],
                loan["annual_rate_pct"],
                loan["remaining_term_months"]
            )
            debts.append({
                "type": "loan",
                "initial_principal": loan["principal"],
                "principal": loan["principal"],
                "rate_annual": loan["annual_rate_pct"],
                "min_payment": min_payment,
                "days_past_due": loan.get("days_past_due", 0)
            })

        for card in self.cards:
            min_payment = max(card["balance"] * (card["min_payment_pct"] / 100), 10)
            debts.append({
                "type": "card",
                "initial_principal": card["balance"],
                "principal": card["balance"],
                "rate_annual": card["annual_rate_pct"],
                "min_payment": min_payment,
                "days_past_due": card.get("days_past_due", 0)
            })

        scenario_minimum = self.simulate_minimum([d.copy() for d in debts])
        scenario_optimized = self.simulate_optimized([d.copy() for d in debts], available_payment)
        scenario_consolidation = self.evaluate_consolidation([d.copy() for d in debts], offers, credit_score, available_payment)

        comparisons = self.compare_scenarios(scenario_minimum, scenario_optimized, scenario_consolidation)

        return {
            "minimum_payment_plan": scenario_minimum,
            "optimized_plan": scenario_optimized,
            "consolidation_plan": scenario_consolidation,
            "comparisons": comparisons
        }

    def amortized_payment(self, P: float, annual_rate: float, months: int) -> float:
        """Cálculo de cuota fija (sistema francés)"""
        if months <= 0:
            return P
        r = annual_rate / 12 / 100
        if r == 0:
            return P / months
        return P * (r / (1 - (1 + r) ** -months))


    def simulate_minimum(self, debts: List[Dict[str, Any]]) -> Dict[str, Any]:
        months, total_interest = 0, 0
        active = True

        while active and months < 600:
            active = False
            for d in debts:
                if d["principal"] > 0:
                    r = d["rate_annual"] / 12 / 100
                    interest = d["principal"] * r
                    pay = min(d["min_payment"], d["principal"] + interest)
                    d["principal"] = d["principal"] + interest - pay
                    total_interest += interest
                    if d["principal"] > 0:
                        active = True
            months += 1

        total_payment = sum(d["initial_principal"] for d in debts) + total_interest
        return {"months": months, "total_interest": total_interest, "total_payment": total_payment}


    def simulate_optimized(self, debts: List[Dict[str, Any]], available_payment: float) -> Dict[str, Any]:
        months, total_interest = 0, 0
        debts.sort(key=lambda x: x["rate_annual"], reverse=True)

        while sum(d["principal"] for d in debts) > 0 and months < 600:
            base_payment = sum(d["min_payment"] for d in debts if d["principal"] > 0)
            extra = max(0, available_payment - base_payment)

            for i, d in enumerate(debts):
                if d["principal"] <= 0:
                    continue
                r = d["rate_annual"] / 12 / 100
                interest = d["principal"] * r
                payment = d["min_payment"]
                if i == 0 and extra > 0:
                    payment += extra
                payment = min(payment, d["principal"] + interest)
                d["principal"] = d["principal"] + interest - payment
                total_interest += interest
            months += 1

        total_payment = sum(d["initial_principal"] for d in debts) + total_interest
        return {"months": months, "total_interest": total_interest, "total_payment": total_payment}


    def evaluate_consolidation(
        self,
        debts: List[Dict[str, Any]],
        offers: List[Dict[str, Any]],
        credit_score: float,
        available_payment: float
    ) -> Dict[str, Any]:
        total_balance = sum(d["principal"] for d in debts if d["type"] in ["card", "loan"])
        if total_balance == 0:
            return {"eligible": False}

        best_offer: Optional[Dict[str, Any]] = None
        for offer in offers:
            if (total_balance <= offer["max_consolidated_balance"]
                    and self.check_conditions(offer.get("conditions", ""), credit_score, debts)):
                if not best_offer or offer["new_rate_pct"] < best_offer["new_rate_pct"]:
                    best_offer = offer

        if not best_offer:
            return {"eligible": False}

        r = best_offer["new_rate_pct"] / 12 / 100
        N = best_offer["max_term_months"]
        P = total_balance
        payment = self.amortized_payment(P, best_offer["new_rate_pct"], N)
        total_payment = payment * N
        total_interest = total_payment - P

        return {
            "eligible": True,
            "offer_id": best_offer["offer_id"],
            "months": N,
            "monthly_payment": payment,
            "total_interest": total_interest,
            "total_payment": total_payment
        }


    def check_conditions(self, conditions: str, credit_score: float, debts: List[Dict[str, Any]]) -> bool:
        if "Score > 650" in conditions and credit_score <= 650:
            return False
        if "sin mora" in conditions and any(d["days_past_due"] > 30 for d in debts):
            return False
        return True


    def compare_scenarios(self, s_min: Dict[str, Any], s_opt: Dict[str, Any], s_con: Dict[str, Any]) -> Dict[str, Any]:
        def calc_diff(a, b):
            return round(a - b, 2), round(((a - b) / a * 100) if a else 0, 2)

        res = {}

        if s_opt and "total_payment" in s_opt:
            abs_save, pct_save = calc_diff(s_min["total_payment"], s_opt["total_payment"])
            res["optimized_vs_minimum"] = {
                "months_diff": s_min["months"] - s_opt["months"],
                "absolute_savings": abs_save,
                "percent_savings": pct_save
            }

        if s_con.get("eligible"):
            abs_save, pct_save = calc_diff(s_min["total_payment"], s_con["total_payment"])
            res["consolidated_vs_minimum"] = {
                "months_diff": s_min["months"] - s_con["months"],
                "absolute_savings": abs_save,
                "percent_savings": pct_save
            }

        # Comparar Consolidado vs Optimizado
        if s_con.get("eligible"):
            abs_save, pct_save = calc_diff(s_opt["total_payment"], s_con["total_payment"])
            res["consolidated_vs_optimized"] = {
                "months_diff": s_opt["months"] - s_con["months"],
                "absolute_savings": abs_save,
                "percent_savings": pct_save
            }

        return res
