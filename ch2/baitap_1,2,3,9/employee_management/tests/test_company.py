import unittest
import os
import sys

# Thêm thư mục gốc vào path để import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.manager import Manager
from models.developer import Developer
from models.intern import Intern
from services.company import Company
from exceptions.employee_exceptions import DuplicateEmployeeError, EmployeeNotFoundError

class TestCompany(unittest.TestCase):
    def setUp(self):
        self.company = Company("Test Co")
        self.m1 = Manager("M01", "Alice", 30, 2000, 5)
        self.d1 = Developer("D01", "Bob", 25, 1500, "Python")

    def test_add_employee(self):
        self.company.add_employee(self.m1)
        self.assertEqual(len(self.company.get_all_employees()), 1)
        self.assertEqual(self.company.find_employee_by_id("M01").name, "Alice")

    def test_duplicate_id(self):
        self.company.add_employee(self.m1)
        with self.assertRaises(DuplicateEmployeeError):
            self.company.add_employee(Manager("M01", "Eve", 40, 3000, 10))

    def test_remove_employee(self):
        self.company.add_employee(self.m1)
        self.company.remove_employee("M01")
        self.assertEqual(len(self.company.get_all_employees()), 0)

    def test_promote_intern_to_dev(self):
        i1 = Intern("I01", "Charlie", 21, 500, "CS")
        self.company.add_employee(i1)
        self.company.promote_employee("I01", "Developer", "Java")
        
        emp = self.company.find_employee_by_id("I01")
        self.assertIsInstance(emp, Developer)
        self.assertEqual(emp.programming_language, "Java")
        self.assertEqual(emp.name, "Charlie")

    def test_payroll_calculation(self):
        # Manager salary: 2000 + (5 * 5,000,000) + 0 = 25,002,000 (if performance is 0)
        # Wait, my formula in code: self.base_salary + allowance + performance_bonus
        # base_salary=2000, team=5, bonus=0 -> 2000 + 25M = 25,002,000
        self.company.add_employee(self.m1)
        total = self.company.calculate_total_payroll()
        self.assertEqual(total, 25002000.0)

if __name__ == "__main__":
    unittest.main()
