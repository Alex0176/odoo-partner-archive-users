# Firma archivieren samt Portalbenutzern

Odoo-19-Modul `partner_archive_users`: Beim Archivieren einer Firma mit
aktiven Portalbenutzern erscheint statt der Odoo-Fehlermeldung eine
Rückfrage. Mit **Ja** werden die Portalbenutzer und die Firma in einem
Schritt archiviert.

## Problem

Odoo verweigert das Archivieren eines Kontakts, solange ein aktiver
Benutzer daran hängt:

> Sie können keine Kontakte archivieren, die mit einem aktiven Benutzer
> verknüpft sind. Archivieren Sie zuerst den zugehörigen Benutzer.

Bei einer Kundenfirma mit mehreren Portalzugängen heißt das: jeden
Benutzer einzeln suchen und archivieren, dann die Firma.

## Lösung

Das Modul erweitert `res.partner.action_archive` (das ist der Weg über
**Aktion → Archivieren** in Formular und Liste):

1. Hängen an den gewählten Kontakten oder an den Ansprechpartnern der
   gewählten Firmen aktive **Portal- oder öffentliche Benutzer**, öffnet
   sich ein Dialog: *Soll die Firma wirklich archiviert werden? Es sind
   noch aktive Benutzer im System.* Der Dialog listet die Benutzer mit
   Anmeldename und Kontakt.
2. **Ja, Firma und Benutzer archivieren** archiviert zuerst die Benutzer,
   dann die gewählten Kontakte. **Abbrechen** ändert nichts.
3. Gibt es keine solchen Benutzer, verhält sich Odoo wie bisher.

Was das Modul bewusst nicht tut:

- **Interne Benutzer** (Mitarbeiter, `share = False`) werden nie über
  diesen Weg archiviert. Hängt ein interner Benutzer an einem Kontakt,
  bleibt die Odoo-Fehlermeldung bestehen.
- Die **Ansprechpartner** der Firma bleiben als Kontakte aktiv; nur ihre
  Portalzugänge werden archiviert. Das entspricht dem Odoo-Standard, der
  beim Archivieren einer Firma die Unterkontakte ebenfalls nicht anfasst.
- Direkte Schreibzugriffe `write({'active': False})` (Import, Skripte)
  laufen unverändert in die Odoo-Prüfung.

## Installation

```
git clone https://github.com/Alex0176/odoo-partner-archive-users.git
ln -s /pfad/odoo-partner-archive-users/partner_archive_users /pfad/addons/
odoo-bin -c odoo.conf -d <db> -i partner_archive_users --stop-after-init
```

Abhängigkeiten: `base`, `contacts`. Keine neuen Felder an bestehenden
Modellen, nur ein Assistent (`partner.archive.users.wizard`).

## Tests

```
odoo-bin -c odoo.conf -d <testdb> -u partner_archive_users --test-tags /partner_archive_users --stop-after-init
```

Vier Tests: Dialog erscheint nur bei Portalbenutzern, Bestätigung
archiviert Benutzer und Firma, ohne Benutzer kein Dialog, interne
Benutzer bleiben gesperrt.

## Lizenz

AGPL-3.0 or later. Copyright 2026 Biricon IT Services e.u.
