def number_of_month(portion_down_payment, total_cost, current_savings,
    annual_salary, portion_saved, r, semi_annual_raise=0.0):
    """
    Return number of month to save down payment
    """
    month_passed = 0
    remain_payment = portion_down_payment * total_cost
    while current_savings < remain_payment:
        month_passed += 1
        current_savings += (annual_salary * portion_saved / 12. + current_savings
                * r / 12.)
        if month_passed % 6 == 0:
            annual_salary *= 1 + semi_annual_raise
    return int(month_passed)
    
