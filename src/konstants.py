from typing import Dict


VALID_ACCESS_TOKEN_IDS = 'VALID_ACCESS_TOKEN_IDS'


USER_ROLE: Dict[str, int] = {
    'ANONYMOUS': -1,
    'NORMAL': 1,
    'INTERN': 3,
    'SUPPORT': 5,
    'MOD': 7,
    'ADMIN': 9
}
