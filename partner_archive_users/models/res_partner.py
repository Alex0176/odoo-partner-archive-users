# Copyright 2026 Biricon IT Services e.u
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _archive_linked_portal_users(self):
        """Aktive Portal-/öffentliche Benutzer, die an diesen Kontakten oder
        an den Ansprechpartnern dieser Firmen hängen."""
        companies = self.filtered("is_company")
        domain = [
            ("share", "=", True),
            "|",
            ("partner_id", "in", self.ids),
            ("partner_id.commercial_partner_id", "in", companies.ids),
        ]
        return self.env["res.users"].sudo().search(domain)

    def action_archive(self):
        if self.env.context.get("archive_linked_users"):
            users = self._archive_linked_portal_users()
            if users:
                users.action_archive()
            return super().action_archive()
        if not self.env.context.get("skip_archive_users_wizard"):
            active = self.filtered("active")
            users = active._archive_linked_portal_users()
            if users:
                wizard = self.env["partner.archive.users.wizard"].create({
                    "partner_ids": [(6, 0, active.ids)],
                    "user_ids": [(6, 0, users.ids)],
                })
                return wizard._action_open()
        return super().action_archive()
