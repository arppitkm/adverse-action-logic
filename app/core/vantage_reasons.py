"""
Vantage Score Reason Code Lookup.

Maps Vantage score reason codes (integers 4–97) to human-readable
descriptions.

Extracted from the LendAPI MRS_30 module (get_vantage_reasons.py).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union


# Full mapping of Vantage score reason codes to descriptions
VANTAGE_REASON_MAP: Dict[int, str] = {
    97: "Too few accounts",
    96: "Too few open accounts",
    95: "No negative reason code",
    94: "No negative reason code",
    93: "Not enough balance paid down over time on first mortgage accounts",
    92: "Delinquent or derogatory first mortgage",
    91: "Balances on delinquent or derogatory revolving accounts are too high",
    90: "No open revolving accounts in your credit file",
    89: "No negative reason code",
    88: "Bankruptcy",
    87: "Unpaid collections",
    86: "Derogatory public records",
    85: "Too many inquiries",
    84: "Number of inquiries was a factor in determining the score",
    83: "No negative reason code",
    82: "Lack of recently reported student loans",
    81: "Not enough balance paid down over time on student loans",
    80: "Delinquent or derogatory student loan",
    79: "No negative reason code",
    78: "Lack of auto account information",
    77: "No open auto accounts in your credit file",
    76: "Delinquent or derogatory status on auto accounts is too recent",
    75: "Payments on auto accounts less than scheduled amount",
    74: "Balances on auto accounts are too high compared with loan amounts",
    73: "Delinquent or derogatory auto account",
    72: "Too few auto accounts paid as agreed",
    71: "Not enough balance paid down over time on auto accounts",
    70: "Too high proportion of auto accounts are delinquent or derogatory",
    69: "Too high proportion of balances from loans not secured by real estate",
    68: "Lack of real estate secured loan information",
    67: "No open real estate secured loans in your credit file",
    66: "Delinquent or derogatory status on real estate loans is too recent",
    65: "Oldest real estate secured loan was opened too recently",
    64: "Not enough balance paid down over time on real estate secured loans",
    63: "Delinquent or derogatory real estate secured loan",
    62: "Lack of first mortgage account information",
    61: "No open first mortgage accounts in your credit file",
    60: "Total delinquent or derogatory balances on real estate loans too high",
    59: "Balances on retail cards are too high compared with credit limits",
    58: "Lack of installment account information",
    57: "No open installment accounts in your credit file",
    56: "Lack of recently reported installment accounts",
    55: "Lack of recently reported auto accounts",
    54: "Delinquent or derogatory status on installment accounts is too recent",
    53: "Not enough balance paid down over time on installment accounts",
    52: "Delinquent or derogatory installment account",
    51: "Too few installment accounts recently paid as agreed",
    50: "Balances on personal installment accts too high compared to loan amts",
    49: "Not enough balance paid down over time on revolving accounts",
    48: "Lack of retail account information",
    47: "No open retail accounts in your credit file",
    46: "Oldest revolving account was opened too recently",
    45: "Not enough balance paid down over time on retail accounts",
    44: "Balances on revolving accts are too high compared with credit limits",
    43: "Too many revolving accounts with high balance compared to credit limit",
    42: "Total credit limits on open revolving accounts are too low",
    41: "Average time since revolving accounts opened is too recent",
    40: "Too many delinquent or derogatory revolving accounts",
    39: "Balances on delinquent or derogatory bankcards are too high",
    38: "Lack of bankcard account information",
    37: "No open bankcards in your credit file",
    36: "Lack of recently reported revolving accounts",
    35: "Lack of revolving account information",
    34: "Most recently opened revolving account is too new",
    33: "Not enough balance paid down over time on bankcards",
    32: "Oldest bankcard was opened too recently",
    31: "Not enough available credit on revolving accounts",
    30: "Too few open revolving accounts",
    29: "Balances on bankcards are too high compared with credit limits",
    28: "Average credit limit on open bankcards is too low",
    27: "Delinquent or derogatory status on revolving accounts is too recent",
    26: "Balances on bankcards are too high",
    25: "Too high proportion of balances from bankcards",
    24: "Too many bankcards with high balance compared to credit limit",
    23: "Too high proportion of bankcards recently opened",
    22: "Too few bankcards with high credit limit",
    21: "Too many bankcards with a high balance",
    20: "Delinquent or derogatory bankcard",
    19: "No negative reason code",
    18: "Lack of account information",
    17: "No open accounts in your credit file",
    16: "Total of credit limits and loan amounts is too low",
    15: "Lack of recently reported accounts",
    14: "Too high proportion of accounts recently opened",
    13: "Balances on delinquent or derogatory accounts are too high",
    12: "Delinquent or derogatory status on accounts is too recent",
    11: "Oldest account was opened too recently",
    10: "Too few accounts paid as agreed",
    9: "Delinquent or derogatory account",
    8: "Too few accounts recently paid as agreed",
    7: "Too many delinquent or derogatory accounts",
    6: "Too many accounts recently opened",
    5: "Too many recent delinquencies",
    4: "Balances on accts too high compared to credit limits and loan amounts",
}


def _parse_vantage_code(code: Any) -> Optional[int]:
    """
    Parse a vantage code to integer, handling leading zeros.

    Examples:
        "00090" -> 90
        "00012" -> 12
        90 -> 90
        "" -> None
        None -> None
    """
    if code is None:
        return None

    if isinstance(code, int):
        return code

    if isinstance(code, str):
        code_str = code.strip()
        if not code_str:
            return None
        try:
            # int() automatically strips leading zeros from strings
            return int(code_str)
        except ValueError:
            return None

    try:
        return int(code)
    except (ValueError, TypeError):
        return None


def get_vantage_reasons(
    codes: List[Union[int, str]],
    *,
    max_items: int = 5,
) -> Dict[str, Any]:
    """
    Resolve a list of Vantage score reason codes to descriptions.

    Accepts a list of integers or strings (including leading-zero strings
    like "00090"). Returns a dict with numbered fields, strictly preserving
    input order. Maximum of ``max_items`` items.

    Args:
        codes: List of reason codes (int or string).
        max_items: Maximum number of items to return (default 5).

    Returns:
        Dict with keys like:
            vantage_score_code_1, vantage_score_description_1,
            vantage_score_code_2, vantage_score_description_2,
            ...
    """
    results: Dict[str, Any] = {}

    for idx, raw_code in enumerate(codes[:max_items], start=1):
        code = _parse_vantage_code(raw_code)

        if code is not None:
            description = VANTAGE_REASON_MAP.get(code, f"Unknown Code: {code}")
            results[f"vantage_score_code_{idx}"] = code
            results[f"vantage_score_description_{idx}"] = description
        else:
            # Handle empty or invalid codes
            results[f"vantage_score_code_{idx}"] = None
            results[f"vantage_score_description_{idx}"] = None

    return results
