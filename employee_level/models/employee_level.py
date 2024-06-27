from odoo import fields,models


class EmployeeLevel(models.Model):
    _name = "employee.level"

    # employee_ids = fields.One2many('hr.employee',)
    level = fields.Many2one('promotion.level',
                             string="Employee Level")
    salary = fields.Float(string="Salary")
    highest = fields.Boolean()


