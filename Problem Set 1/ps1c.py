#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 07:02:48 2021

@author: jordangallivan
"""

# constants
total_cost = 1000000.0          # cost of dream house
portion_down_payment = 0.25     # cost needed for a down payment 
r = 0.04                          # annual return
monthly_return = r/12
current_savings = 0.0       # amount in savings

# pull user input
orig_annual_salary = float(input("Please enter your annual salary: "))
annual_salary=orig_annual_salary

portion_saved = int(0)          # percentage of salary saved monthly
semi_annual_raise = 0.07
monthly_salary = annual_salary/12

down_payment = total_cost*portion_down_payment

epsilon=100
num_guess = 1

# initialize search values
low=0
high=10000
guess=(high+low)//2
portion_saved=guess/10000.0

# iterate through applying semi_annaul_raises
for n in range(0,35):
    current_savings = current_savings + current_savings*monthly_return + (monthly_salary*portion_saved)
    if ((n+1)%6)==0:
        annual_salary = annual_salary + annual_salary*semi_annual_raise
        monthly_salary = annual_salary/12

# search via bisection search
while abs(current_savings-down_payment) >= epsilon:
    if current_savings < down_payment:
        low=guess 
    else:
        high=guess
    
    guess=(high+low)//2
    current_savings = 0
    annual_salary=orig_annual_salary
    monthly_salary = annual_salary/12
    portion_saved=guess/10000.0
    
    for n in range(0,35):
        current_savings = current_savings + current_savings*monthly_return + (monthly_salary*portion_saved)
        if ((n+1)%6)==0:
            annual_salary = annual_salary + annual_salary*semi_annual_raise
            monthly_salary = annual_salary/12
    num_guess+=1
    
    if guess == 9999:
        print("It is not possible to pay the downpayment in 3 years")
        break    

if guess!=9999:    
    print("number of guesses "+str(num_guess))
    print("percent saved: "+str(portion_saved))


