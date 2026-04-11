import unittest
import os
import sys

# Thêm thư mục gốc vào path để import các module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.manager import Manager
from models.developer import Developer
from services.company import Company

class TestHRAdvanced(unittest.TestCase):
    def setUp(self):
        self.company = Company("Advanced Test")
        self.m1 = Manager("M01", "Alice", 40, 5000000, 5)
        self.d1 = Developer("D01", "Bob", 30, 3000000, "Python")
        self.company.add_employee(self.m1)
        self.company.add_employee(self.d1)

    def test_salary_reduction(self):
        # Alice salary: 5,000,000. Reduce by 1,000,000
        self.company.decrease_salary("M01", 1000000)
        self.assertEqual(self.m1.base_salary, 4000000)

    def test_salary_reduction_limit(self):
        # Alice salary: 5,000,000. Reduce by 4,500,000 -> 500,000 (Invalid < 1M)
        with self.assertRaises(ValueError):
            self.company.decrease_salary("M01", 4500000)

    def test_project_sorting(self):
        self.d1.add_project("Project Alpha")
        self.d1.add_project("Project Beta")
        self.m1.add_project("Project Gamma")
        
        sorted_emps = self.company.get_employees_sorted_by_projects()
        self.assertEqual(sorted_emps[0].emp_id, "D01") # Bob has 2, Alice has 1

    def test_find_by_project(self):
        self.d1.add_project("AI Module")
        self.m1.add_project("AI Module")
        
        participants = self.company.get_employees_by_project("AI Module")
        self.assertEqual(len(participants), 2)

    def test_termination_compensation(self):
        # Alice (Manager): Team size 5, score 0.
        # Salary = 5M + 5*5M + 0 = 30,000,000
        # Compensation = 2 * 30M = 60,000,000
        comp = self.company.terminate_employee("M01")
        self.assertEqual(comp, 60000000.0)
        self.assertEqual(len(self.company.get_all_employees()), 1)

if __name__ == "__main__":
    unittest.main()
