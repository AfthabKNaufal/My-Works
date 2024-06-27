from odoo import _, fields, models, Command


class SaleOrder(models.Model):
    _inherit = "sale.order"

    count_proj = fields.Integer(compute='_compute_count_project')

    def _compute_count_project(self):
        """Returns the count of the projects"""
        for rec in self:
            self.count_proj = rec.env['project.project'].search_count([(
                'name', '=', self.name)])

    def action_create_projects(self):
        """Create a new project and if a project already exists, will add
        products as the subtask of the parent task """
        project = self.env['project.project'].create({
            'name': self.name
        })

        for rec in self.order_line:
            name = "Milestone %s" % rec.milestone
            if name not in project.task_ids.mapped('name'):
                task = self.env['project.task'].create({
                    'name': "Milestone %s" % rec.milestone,
                    'project_id': project.id,
                    'child_ids': [Command.create({
                        'name': f"Milestone {rec.milestone}-"
                                f"{rec.product_template_id.name}",
                    })]

                })
                mil = self.env['project.milestone'].create({
                    'name': "Milestone %s" % rec.milestone,
                    'project_id': project.id,
                })
                task.write({
                    'milestone_id': mil.id
                })
            else:
                name = "Milestone %s" % rec.milestone
                current_task = project.task_ids.search([('name', '=', name)])
                current_task.write({
                    'child_ids': [Command.create({
                        'name': f"Milestone {rec.milestone}-"
                                f"{rec.product_template_id.name}",
                    })]
                })

    def action_view_project(self):
        """Smart tab to view the project created"""
        project = self.env['project.project'].search([('name', '=', self.name)])
        return {
            'name': _("Project"),
            'res_model': 'project.project',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'target': 'self',
            'domain': [('id', 'in', project.ids)]
        }

    def action_update_project(self):
        """Function to update the task of the project by changing the
        order line of the sale order
        - If created a new task will be added
        - If altered the changed subtask will be appended
        - If a product is removed task related to that task will be removed """
        project = self.env['project.project'].search([('name', '=', self.name)])
        # print(project.task_ids.filtered(
        # lambda task: task.display_in_project == True).mapped('name'))
        not_present_task = []
        contains = []
        for rec in project.task_ids:
            rec.write({
                'child_ids': [Command.clear()]
            })
            for record in self.order_line:
                # print("Milestone %s" % record.milestone)
                if rec.name in "Milestone %s" % record.milestone:
                    contains.append(rec)
                else:
                    if rec not in not_present_task:
                        not_present_task.append(rec)
        for records in not_present_task:
            if records not in contains:
                records.unlink()

        for rec in self.order_line:
            # print(rec.milestone)
            if ("Milestone %s" % rec.milestone
                    not in project.task_ids.mapped('name')):
                rec.env['project.task'].create({
                            'name': "Milestone %s" % rec.milestone,
                            'project_id': project.id,
                            'child_ids': [Command.create({
                                'name': f"Milestone {rec.milestone}-"
                                        f"{rec.product_template_id.name}",
                            })]
                       })
            else:
                name = "Milestone %s" % rec.milestone
                current_task = project.task_ids.search([('name', '=', name)])
                current_task.write({
                    'child_ids': [Command.create({
                        'name': f"Milestone {rec.milestone}-"
                                f"{rec.product_template_id.name}",
                    })]
                })
