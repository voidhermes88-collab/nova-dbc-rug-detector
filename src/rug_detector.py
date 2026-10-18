"""
Nova Rug Detector - MVP v0.1
Solana Meteora DBC -> DAMM v2
Lord: Norbert Csanya
"""

from dataclasses import dataclass
from typing import List

@dataclass
class PoolState:
    mint: str
    top_10_holders_pct: float
    dev_holding_pct: float
    lp_locked: bool
    bundled_wallet_count: int
    sniper_pct_first_3_blocks: float
    has_freeze_authority: bool
    wash_trading_score: float  # 0-1

def calculate_rug_score(pool: PoolState) -> dict:
    score = 100
    reasons = []

    if pool.top_10_holders_pct > 50:
        score -= 30
        reasons.append(f"Top 10 holders {pool.top_10_holders_pct:.1f}% > 50% (-30)")

    if pool.dev_holding_pct > 15:
        score -= 25
        reasons.append(f"Dev holding {pool.dev_holding_pct:.1f}% > 15% after migrate (-25)")

    if pool.bundled_wallet_count >= 5:
        score -= 20
        reasons.append(f"Bundled wallets: {pool.bundled_wallet_count} (-20)")

    if not pool.lp_locked:
        score -= 20
        reasons.append("LP not locked/burned in DAMM v2 (-20)")

    if pool.sniper_pct_first_3_blocks > 30:
        score -= 15
        reasons.append(f"Snipers {pool.sniper_pct_first_3_blocks:.1f}% in first 3 blocks (-15)")

    if pool.has_freeze_authority:
        score -= 20
        reasons.append("Freeze authority still active (-20)")

    if pool.wash_trading_score > 0.7:
        score -= 10
        reasons.append(f"Wash trading detected {pool.wash_trading_score:.2f} (-10)")

    score = max(0, min(100, score))

    if score <= 30:
        risk = "HIGH"
    elif score <= 69:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "mint": pool.mint,
        "score": score,
        "risk": risk,
        "reasons": reasons
    }

# Példa
if __name__ == "__main__":
    example = PoolState(
        mint="NovaTest123...",
        top_10_holders_pct=62.5,
        dev_holding_pct=18.0,
        lp_locked=False,
        bundled_wallet_count=7,
        sniper_pct_first_3_blocks=35.2,
        has_freeze_authority=True,
        wash_trading_score=0.8
    )
    print(calculate_rug_score(example))
