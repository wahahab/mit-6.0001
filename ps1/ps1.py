# -*- coding: utf-8 -*-
import math
from util import number_of_month 

if __name__ == '__main__':
    month_passed = 0 
    current_savings = 0
    portion_down_payment = .25
    r = .04
    annual_salary = float(input('Enter your annual salary: '))
    portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
    total_cost = float(input('Enter the cost of your dream home: '))
    print 'Number of months:', int(number_of_month(portion_down_payment,
        total_cost, current_savings, annual_salary, portion_saved, r))
    
