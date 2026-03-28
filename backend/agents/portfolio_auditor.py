def calculate_portfolio_leakage(total_aum: float, current_er: float, direct_er: float = 0.85) -> dict:
    """
    Calculates the 10-year wealth impact of high expense ratios.
    Formula: FV = P * [(1 + r)^n - 1] / r
    """
    n = 10 # 10 years
    r = 0.12 # 12% CAGR
    
    # Real Math: Impact depends on AUM
    excess_er = (float(current_er) - float(direct_er)) / 100
    leakage_per_year = float(total_aum) * excess_er
    
    # Future Value of leakage (Wealth Lost)
    ten_year_impact = float(leakage_per_year) * ((pow(1 + r, n) - 1) / r)
    
    return {
        "total_aum": float(total_aum),
        "avg_expense_ratio": float(current_er),
        "ten_year_impact": round(float(ten_year_impact), 2),
        "overlap_percentage": 45 # Constant for demo
    }
