# -*- coding: utf-8 -*-
import math

from util import number_of_month

SCALE = 10000

if __name__ == '__main__':
    months = 0 
    current_savings = 0
    portion_down_payment = .25
    r = .04
    min_portion_saved = 0
    max_portion_saved = 10000
    best_portion_saved = 0
    semi_annual_raise = .07
    total_cost = 1000000
    it_count = 0
    start_salary = float(input('Enter the starting salary: '))
    while months != 36 and max_portion_saved > min_portion_saved + 1:
        best_portion_saved = (min_portion_saved + max_portion_saved) / 2
        months = number_of_month(portion_down_payment, total_cost, current_savings,
            start_salary, float(best_portion_saved) / SCALE, r, semi_annual_raise)
        it_count += 1
        if months > 36:
            min_portion_saved = best_portion_saved
        elif months < 36:
            max_portion_saved = best_portion_saved
    if (max_portion_saved == SCALE and min_portion_saved == SCALE - 1):
        print 'It is not possible to pay the down payment in three years.'
    else:
        print 'Best savings rate: ', float(best_portion_saved) / SCALE
        print 'Steps in bisection search: ', it_count
    
