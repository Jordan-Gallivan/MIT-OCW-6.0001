#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 07:02:48 2021

@author: jordangallivan
"""

total_cost = float(0)           # cost of dream house
portion_down_payment = 0.25     # cost needed for a down payment 
r = 0.04                          # annual return
monthly_return = r/12
current_savings = float(0)        # amount in savings
annual_salary = float(0)          # annual salary
portion_saved = float(0)          # percentage of salary saved monthly
n = int(1)                        # number of months

annual_salary = float(input("Please enter your annual salary: "))
portion_saved = float(input("Please enter the portion of your salary you wish to save (as a decimal): "))
total_cost = float(input("What is the cost of your dream home? "))
semi_annual_raise = float(input("Please enter your semi-annual raise (decimal): "))

monthly_salary = annual_salary/12
down_payment = total_cost*portion_down_payment

# iterate until down payment is reached
while current_savings < down_payment:
    current_savings = current_savings + current_savings*monthly_return + (monthly_salary*portion_saved)


    if (n%6)==0:
        annual_salary = annual_salary + annual_salary*semi_annual_raise
        monthly_salary = annual_salary/12
    n = n+1    
        
print("It will take "+str(n-1)+" months to save for your dream home")  
 