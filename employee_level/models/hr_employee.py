from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    level_id = fields.Many2one("promotion.level", string="Levels")
    salary = fields.Float(string="Salary")
    high = fields.Boolean(default=False)


    def action_promote(self):
        levels = self.env['employee.level'].search_read([],['level', 'salary', 'highest'])
        print(levels)
        for rec in levels:
            print(rec['highest'])
            print(self.level_id.id)
            if self.level_id.id == rec['id'] and rec['highest'] == True:
                print("aaaa")
                self.high = True
                self.write({
                    'salary': rec['salary']
                })
                break
            if self.level_id.id == rec['id']:
                print("aaa")
                self.level_id = rec['id']+1
                self.write({
                    'salary': rec['salary']
                })
                break




