def calculate_tax_liability(salary: float, hra: float = 0.0, section_80c: float = 0.0) -> dict:
    """
    Calculates tax liability based on current Indian Income Tax laws (Old vs. New Regime).
    Returns the most optimal regime with the associated metrics.
    """
    
    # --- New Regime Calculation ---
    # Standard Deduction is ₹75,000 for New Regime
    std_deduction_new = 75000.0
    taxable_income_new = max(0.0, salary - std_deduction_new)
    
    tax_new = 0.0
    if taxable_income_new <= 700000.0:
        # Full Rebate u/s 87A if taxable income is <= 7 Lakhs
        tax_new = 0.0
    else:
        if taxable_income_new > 300000.0:
            tax_new += min(taxable_income_new - 300000.0, 400000.0) * 0.05
        if taxable_income_new > 700000.0:
            tax_new += min(taxable_income_new - 700000.0, 300000.0) * 0.10
        if taxable_income_new > 1000000.0:
            tax_new += min(taxable_income_new - 1000000.0, 200000.0) * 0.15
        if taxable_income_new > 1200000.0:
            tax_new += min(taxable_income_new - 1200000.0, 300000.0) * 0.20
        if taxable_income_new > 1500000.0:
            tax_new += (taxable_income_new - 1500000.0) * 0.30
            
    # Add 4% Health and Education Cess
    tax_new *= 1.04
    
    
    # --- Old Regime Calculation ---
    # Standard Deduction is ₹50,000 for Old Regime
    std_deduction_old = 50000.0
    # Cap 80C deduction at 1.5 Lakhs
    capped_80c = min(section_80c, 150000.0)
    taxable_income_old = max(0.0, salary - std_deduction_old - hra - capped_80c)
    
    tax_old = 0.0
    if taxable_income_old <= 500000.0:
        # Full Rebate u/s 87A if taxable income is <= 5 Lakhs
        tax_old = 0.0
    else:
        if taxable_income_old > 250000.0:
            tax_old += min(taxable_income_old - 250000.0, 250000.0) * 0.05
        if taxable_income_old > 500000.0:
            tax_old += min(taxable_income_old - 500000.0, 500000.0) * 0.20
        if taxable_income_old > 1000000.0:
            tax_old += (taxable_income_old - 1000000.0) * 0.30
            
    # Add 4% Health and Education Cess
    tax_old *= 1.04
    
    
    # --- Determine the Optimal Regime ---
    if tax_new < tax_old:
        optimal_regime = "New Regime"
    elif old_tax_better := (tax_old < tax_new):
        optimal_regime = "Old Regime"
    else:
        optimal_regime = "Equal (New Regime is often preferred for less paperwork)"
        
    tax_savings = abs(tax_old - tax_new)
    
    return {
        "salary_input": salary,
        "old_regime_tax": round(tax_old, 2),
        "new_regime_tax": round(tax_new, 2),
        "optimal_regime": optimal_regime,
        "tax_savings": round(tax_savings, 2)
    }

if __name__ == "__main__":
    # Test case simulating a salary of 20L with some common deductions
    result = calculate_tax_liability(salary=2000000, hra=250000, section_80c=150000)
    print("Tax Calculation Summary:", result)
