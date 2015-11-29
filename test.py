__author__ = 'Chenxi'
# !/usr/bin/python
from credit import *
import unittest
import pandas as pd

CREDIT_LIMIT = 1000000
APR = 0.35

def new_credit_line():
    d = credit_line(APR,CREDIT_LIMIT)
    return d

class test_operation:
    def __init__(self,url,sheet_number):
        self._principal=0
        self._credit_Bal=0
        self._interest_cached=0
        self._interest_incurred=0
        self._url = url
        self._sheet_num =sheet_number
    def check_cases(self):
        """
        :rtype : object
        """
        credit=new_credit_line()
        xls_file = pd.ExcelFile(self._url)
        df = xls_file.parse(self._sheet_num)
        tail = df.tail(1)
        principal,credit_Bal,interest_incurred = credit.operation(df)
        arr_comp = [round(principal,2),round(credit_Bal,2),round(interest_incurred,2)]
        test_principal,test_credit_bal,test_interest_outstanding = round(float(tail['principal']),2),round(float(tail['Credit_Bal']),2),round(float(tail['interest_due']),2)
        arr_actual_result= [test_principal,test_credit_bal,test_interest_outstanding]
        return arr_comp,arr_actual_result
    def check_processes(self):
        credit=new_credit_line()
        xls_file = pd.ExcelFile(self._url)
        df = xls_file.parse(self._sheet_num)
        size = len(df.index)
        list_tested = []
        list_result = []
        for j in range(size):
            _principal,_credit_bal,interest_outstanding = credit.action_management(df['date'][j],df['amount'][j],df['action_type'][j])
            list_tested.append((j,round(_principal),round(_credit_bal),round(interest_outstanding)))
            list_result.append((j,round(float(df['principal'][j])),round(float(df['Credit_Bal'][j])),round(float(df['interest_due'][j]))))
        return list_tested,list_result

class test_equality(unittest.TestCase):
    """
    Test examples from the excels file:basic_case1 and basic_case2
    """
    def setUp(self):
        pass
    # this test cases is to calculate only 1 straight month's record with principal outstanding
    def test_comp_result1(self):
        url = "C://Users//Chenxi//Desktop//Avant_Project//data//basic_case1.xlsx"
        t1=test_operation(url,0)
        _arr_comp,_arr_actual_result = t1.check_cases()
        self.assertEqual(_arr_comp,_arr_actual_result)
    # this test case has a date 1 and date 30,yet anytime during date 30 has not charged interest yet as described
    def test_comp_result2(self):
        url = "C://Users//Chenxi//Desktop//Avant_Project//data//basic_case1.xlsx"
        t1=test_operation(url,1)
        _arr_comp,_arr_actual_result = t1.check_cases()
        self.assertEqual(_arr_comp,_arr_actual_result)
    # this test case designed to test accumulated interest with a principal across multiple 30 dates periods
    def test_comp_result3(self):
        url = "C://Users//Chenxi//Desktop//Avant_Project//data//basic_case1.xlsx"
        t1=test_operation(url,2)
        _arr_comp,_arr_actual_result = t1.check_cases()
        self.assertEqual(_arr_comp,_arr_actual_result)
    # this test case is similar to the test case provided in the requirement sheet,multiple transactions in 1 period
    def test_comp_result4(self):
        url = "C://Users//Chenxi//Desktop//Avant_Project//data//basic_case2.xlsx"
        t1=test_operation(url,0)
        _arr_comp,_arr_actual_result = t1.check_cases()
        self.assertEqual(_arr_comp,_arr_actual_result)
    # this test case is similar to the last test case yet the last payment is 66 days aways which involves one transaction in multiple periods
    def test_comp_result5(self):
        url = "C://Users//Chenxi//Desktop//Avant_Project//data//basic_case2.xlsx"
        t1=test_operation(url,1)
        _arr_comp,_arr_actual_result = t1.check_cases()
        self.assertEqual(_arr_comp,_arr_actual_result)
    # this test case is similar to test_comp_result4, yet the last payment is within the 30 dates period and pay back in full on principal
    def test_comp_result6(self):
        url = "C://Users//Chenxi//Desktop//Avant_Project//data//basic_case2.xlsx"
        t1=test_operation(url,2)
        _arr_comp,_arr_actual_result = t1.check_cases()
        self.assertEqual(_arr_comp,_arr_actual_result)
    # this test case is similar to test_comp_result4, yet the last payment is in the 2nd payment period
    def test_comp_result7(self):
        url = "C://Users//Chenxi//Desktop//Avant_Project//data//basic_case2.xlsx"
        t1=test_operation(url,3)
        _arr_comp,_arr_actual_result = t1.check_cases()
        self.assertEqual(_arr_comp,_arr_actual_result)
    # this test case is built up on test_comp_result4, yet it has 7 records lasting for 92 dates with 3 records in the 2nd period
    def test_comp_result8(self):
        url = "C://Users//Chenxi//Desktop//Avant_Project//data//basic_case2.xlsx"
        t1=test_operation(url,4)
        _arr_comp,_arr_actual_result = t1.check_cases()
        self.assertEqual(_arr_comp,_arr_actual_result)
    #this test is based on the same data set as the last one,yet it keeps track of all 7 transaction records:
    # principal,credit_bal,interest_outstanding
    def test_comp_check(self):
        url = "C://Users//Chenxi//Desktop//Avant_Project//data//basic_case2.xlsx"
        t1=test_operation(url,4)
        _arr_comp,_arr_actual_result = t1.check_processes()
        self.assertEqual(_arr_comp,_arr_actual_result)

if __name__ == "__main__":
    unittest.main()
