# -*- coding: utf-8 -*-
# Copyright 2026 Biricon IT Services e.u
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Firma archivieren samt Portalbenutzern",
    "summary": "Rückfrage statt Fehlermeldung, wenn eine Firma mit aktiven "
               "Portalbenutzern archiviert wird; bei Ja werden die Benutzer "
               "mit archiviert.",
    "description": """
Firma archivieren samt Portalbenutzern
======================================

Odoo verweigert das Archivieren eines Kontakts, solange ein aktiver
Benutzer daran hängt. Beim Archivieren einer Firma heißt das in der
Praxis: erst alle Portalzugänge der Firma und ihrer Ansprechpartner
von Hand suchen und archivieren, dann die Firma.

Dieses Modul ersetzt die Fehlermeldung durch eine Rückfrage. Sie zeigt,
welche Portalbenutzer noch aktiv sind. Mit **Ja** werden diese Benutzer
und die Firma in einem Schritt archiviert, mit **Abbrechen** bleibt
alles wie es war.

Interne Benutzer (Mitarbeiter) werden nie über diesen Weg archiviert;
hängt ein interner Benutzer an der Firma, bleibt die Odoo-Fehlermeldung
bestehen.
    """,
    "version": "19.0.1.0.0",
    "category": "Contacts",
    "author": "Biricon IT Services e.u",
    "website": "https://www.biricon.eu/",
    "license": "AGPL-3",
    "depends": ["base", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/partner_archive_users_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
}
