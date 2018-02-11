#import sys
#import csv

class Calculator(object):
    
    def __init__(self):
        self.__insurance__ = self.read_cfg()
        self.__employees__ = self.read_user_data()


    def read_cfg(self):
        ''' read insurance ratio from configuration file in format {:.2f}
        '''
        sum = 0.0
        with open('test.cfg','r') as file:
            for line in file.readlines():
                value = float(line.split('=')[1])
                sum += value
            print('Total insurance ratio: {:.2f}'.format(sum))
        return sum

    def read_user_data(self):
        '''read employees original salary data
        '''
        employees = []
        with open('user.csv','r') as file:
            for line in file.readlines():
                jodID,salary = line.split(',')
                salary = float(salary)*(1.0-self.__insurance__)
                employees.append({'jobid':jodID,'salary':salary})
        return employees
    
    def write_data(self):
        '''write data into file
        '''
        with open('salary.csv','a+') as file:
            for data in self.__employees__:
                file.write(data['jobid']+','+'{:.2f}'.format(data['salary'])+'\n')
        print("write data success.")

if __name__ == '__main__':
    calc = Calculator()
    calc.write_data()