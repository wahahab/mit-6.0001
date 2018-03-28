# -*- coding: utf-8 -*-
import math

from util import number_of_month

if __name__ == '__main__':
    number_of_steps = 0
    month_passed = 0 
    current_savings = 0
    portion_down_payment = .25
    r = .04
    total_cost = 1000000
    semi_annual_raise = .07
    annual_salary = float(input('Enter the starting salary: '))
    portion_saved = float(input('Best savings rate: '))
    total_cost = float(input('Enter the cost of your dream home: '))
    semi_annual_raise = float(input('Enter the semi­annual raise, as a decimal: '))
    print 'Number of months:', int(number_of_month(portion_down_payment, total_cost,
        current_savings, annual_salary, portion_saved, r, semi_annual_raise))
    
