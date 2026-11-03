# Copyright 2026 Biricon IT Services e.u
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.exceptions import RedirectWarning
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPartnerArchiveUsers(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env["res.partner"].create({"name": "Testfirma GmbH", "is_company": True})
        cls.contact = cls.env["res.partner"].create({"name": "Max Muster", "parent_id": cls.company.id})
        cls.portal_group = cls.env.ref("base.group_portal")
        cls.portal_user = cls.env["res.users"].with_context(no_reset_password=True).create({
            "name": "Max Muster", "login": "max.muster@example.com",
            "partner_id": cls.contact.id, "group_ids": [(6, 0, [cls.portal_group.id])],
        })

    def test_wizard_returned_when_portal_users_exist(self):
        action = self.company.action_archive()
        self.assertEqual(action.get("res_model"), "partner.archive.users.wizard")
        # Der Web-Client wertet die Aktion ohne weitere Aufbereitung aus und verlangt "views"
        self.assertEqual(action.get("views"), [(False, "form")])
        wizard = self.env["partner.archive.users.wizard"].browse(action["res_id"])
        self.assertEqual(wizard.partner_ids, self.company)
        self.assertEqual(wizard.user_ids, self.portal_user)
        self.assertTrue(self.company.active, "Nichts darf vor der Bestätigung archiviert werden")
        self.assertTrue(self.portal_user.active)

    def test_confirm_archives_users_and_company(self):
        action = self.company.action_archive()
        wizard = self.env["partner.archive.users.wizard"].browse(action["res_id"])
        wizard.action_confirm()
        self.assertFalse(self.portal_user.with_context(active_test=False).active)
        self.assertFalse(self.company.with_context(active_test=False).active)
        self.assertTrue(self.contact.active, "Ansprechpartner selbst bleibt unverändert")

    def test_no_wizard_without_users(self):
        other = self.env["res.partner"].create({"name": "Ohne Benutzer", "is_company": True})
        self.assertIsNone(other.action_archive())
        self.assertFalse(other.with_context(active_test=False).active)

    def test_internal_user_still_blocked(self):
        internal_partner = self.env["res.partner"].create({"name": "Intern", "parent_id": self.company.id})
        self.env["res.users"].with_context(no_reset_password=True).create({
            "name": "Intern", "login": "intern@example.com", "partner_id": internal_partner.id,
            "group_ids": [(6, 0, [self.env.ref("base.group_user").id])],
        })
        # Der interne Benutzer haengt am Ansprechpartner: Archivieren des Ansprechpartners
        # bleibt wie in Odoo verboten, der Assistent fasst interne Benutzer nicht an.
        with self.assertRaises(RedirectWarning):
            internal_partner.action_archive()
        self.assertTrue(internal_partner.active)
