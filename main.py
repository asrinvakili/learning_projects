class Employee:
    def __init__(self, f_name,l_name):
        self.f_name = f_name
        self.l_name = l_name
        self.salary= 3000

    def display(self):
        print(f'one of employee is {self.f_name} {self.l_name}. her/his salary is {self.salary}.')


a= Employee('Ahmad', 'Ahmadi')
a.display()
