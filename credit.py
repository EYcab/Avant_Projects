__author__ = 'Chenxi'
from abc import abstractmethod
import sys
#The below is a abstract base class for apr and credit_limit
#therefore,apr and credit_limit must have value to run the program
#Yet,they could be and have to be defined in a child class
class Base():
    @abstractmethod
    def apr(self):
        pass
    @abstractmethod
    def credit_limit(self):
        pass
#main_factors inherits from the base class and define its 2 key factors
class main_factors(Base, object):
    def __init__(self, apr, credit_limit):
        self._apr = apr
        self._credit_limit = credit_limit
        super(main_factors, self).__init__()
    @property
    def apr(self):
        return self._apr
    # sets apr
    # returns: self
    @apr.setter
    def apr(self,value= None):
        self._apr = value

    # returns: credit limit
    @property
    def credit_limit(self):
        return self._credit_limit

    # sets credit limit
    # returns: self
    @credit_limit.setter
    def credit_limit(self, value=None):
        self._credit_limit = value
#credit_line(a child class of main_factors) has the below methods:
#first_transaction: for the first transaction calculation which starts when principal is loaded from 0 to positive
#transaction_in_period: for the non-first transaction where exclude the above scenario and only accountable for activity in 30 dates period
#over_thirty_dates_cal: accounting for the activities lasting more than 30 dates between transactions or principal outstanding exceeding the period
#end_period_cal: concluding all the billing amount in the end of each period
#action_management: manage the logic of actions for the above methods activities
#operation: read in a data frame and proceed with outcomes for transaction at each point in time
class credit_line(main_factors):
    def __init__(self, apr, credit_limit):
        self._apr = apr
        self._credit_limit = credit_limit
        # print "through here"
        super(credit_line, self).__init__(self._apr, self._credit_limit)
        self._interest = 0
        self._principal = 0
        self._credit_Bal = credit_limit
        self._interest_incurred = 0

    def first_transaction(self,first_date,amount,action_type):
        self._interest = 0
        self._principal += amount
        self._credit_Bal = self._credit_Bal - amount
        self._first_date = first_date -1
        self._last_date = self._first_date
        self._count_dates = 0
        #print "principal:",self._principal
    def transaction_in_period(self,current_date,amount,action_type):
        """
        :type self: for the non-first transaction where exclude the above scenario and only accountable for activity in  30 dates period
        Both payments and withdrawals
        """
        #Here better call over_thirty_dates_cal()
        #print "Hello",self._credit_Bal, action_type, self._credit_limit,self._principal,self._period
        #self._period is used for dates principals is outstanding in the nearest 2 transactions
        period = self._period%30
        if self._credit_Bal >= 0 and action_type == ('w' or 'W'):
            #print "amount after a withdrawal:",amount
            if self._credit_Bal > amount:
                self._interest += self._principal * self._apr * period/365
                self._principal += amount
                self._credit_Bal = self._credit_Bal - amount
                #print "principal after the withdrawal",self._principal
            else:
                print "You cannot borrow more than the current credit limit!Or there is something wrong with the input"
                exit()
        elif self._credit_Bal < self._credit_limit and action_type == ('p' or 'P'):
            if self._principal >= amount:
                self._interest += self._principal * self._apr * period/ 365
                self._principal = self._principal - amount
                self._credit_Bal = self._credit_Bal + amount
                #print "p", self._principal,"******",self._credit_Bal,"-----",period
                if self._principal == 0:
                    self._count_dates = 0
                    self._interest = 0
            else:
                print "You should not pay back more than you should! or there is something wrong with the input"
                sys.exit()
        # else:
        #     print "Error"
        #     exit()
        return self._principal, self._credit_Bal, self._interest_incurred
    #over_thirty_dates_cal: accounting for the activities
    # lasting more than 30 dates between transactions or principal outstanding exceeding the period
    def over_thirty_dates_cal(self):
        if self._count_dates > 30:
            # print "the latest 2 transaction period over 30 dates is:", self._count_dates
            # print "last_date,first_date",self._last_date,self._first_date

            #the below is used for getting the time gap in the last 30 dates period
            ex_period = self._last_date - self._first_date
            date_effective = ex_period%30
            if date_effective < 30:
                self.end_period_cal(date_effective,30)
            #the below is used to adjust the calculated starting date in a 30 dates interest billing period
            while self._count_dates > 30:
                self._count_dates = self._count_dates - 30
                self._last_date = self._first_date + 30
                #print "here is the count_dates-----,go", self._count_dates

                #if self.count_dates is still larger than 30 in truncation
                #we conclude a new period interest billing
                if int(self._count_dates)/30 >0:
                    self.end_period_cal(0,30)
            self._period = self._current_date - self._last_date
        return self._interest,self._interest_incurred,self._principal,self._credit_Bal
    #end_period_cal: concluding all the billing amount in the end of each period
    def end_period_cal(self,first_period,end_date):
        self._interest += self._principal * self._apr * (end_date - first_period) / 365
        self._interest_incurred += self._interest
        # print "Interest_outstanding: ", self._interest_incurred
        self._interest = 0
        self._credit_Bal = self._credit_limit - (self._principal + self._interest_incurred)
        return self._interest
    #action_management: manage the logic of actions for the above methods activities
    def action_management(self,current_date,amount,action_type):
        #the mutual exclusive 'if' logic splitting 2 scenarios principal >0 and principal ==0
        if self._principal == 0 and action_type == ('w' or 'W'):
            self.first_transaction(first_date=current_date,amount=amount,action_type=action_type)
        elif self._principal > 0:
            self._current_date = current_date
            # print "current_date,last_date,count_dates",self._current_date,self._last_date, self._count_dates
            self._period = self._current_date - self._last_date
            self._count_dates += self._period
            # print "count_dates", self._count_dates
            if self._count_dates > 30:
                self.over_thirty_dates_cal()
                self.transaction_in_period(current_date=current_date,amount=amount,action_type=action_type)
            elif self._count_dates<=30:
                self.transaction_in_period(current_date=current_date,amount=amount,action_type=action_type)
            self._last_date = self._current_date
        else:
            "Error,Principal can not be negative!"
        return self._principal, self._credit_Bal,self._interest_incurred
    #operation to get data to process
    def operation(self,df):
        # xls_file = pd.ExcelFile(url)
        # df = xls_file.parse(1)

        #dataframe iteration
        for index,row in df.iterrows():
            self.action_management(row['date'],row['amount'],row['action_type'])
        return self._principal, self._credit_Bal,self._interest_incurred

