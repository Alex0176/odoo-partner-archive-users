# Copyright 2026 Biricon IT Services e.u
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models


class PartnerArchiveUsersWizard(models.TransientModel):
    _name = "partner.archive.users.wizard"
    _description = "Archive Company with Portal Users"

    partner_ids = fields.Many2many(
        "res.partner", "partner_archive_users_wizard_partner_rel",
        string="Contacts", required=True, readonly=True)
    user_ids = fields.Many2many(
        "res.users", "partner_archive_users_wizard_user_rel",
        string="Active portal users", readonly=True)
    partner_names = fields.Char(compute="_compute_names")
    user_count = fields.Integer(compute="_compute_names")

    @api.depends("partner_ids", "user_ids")
    def _compute_names(self):
        for wizard in self:
            wizard.partner_names = ", ".join(wizard.partner_ids.mapped("display_name"))
            wizard.user_count = len(wizard.user_ids)

    def _action_open(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Archive company?"),
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "views": [(False, "form")],
            "target": "new",
        }

    def action_confirm(self):
        self.ensure_one()
        self.partner_ids.with_context(archive_linked_users=True).action_archive()
        return {"type": "ir.actions.act_window_close"}
