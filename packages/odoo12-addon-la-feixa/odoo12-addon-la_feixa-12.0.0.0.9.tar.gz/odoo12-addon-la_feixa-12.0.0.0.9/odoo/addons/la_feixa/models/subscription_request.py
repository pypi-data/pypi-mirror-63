# -*- coding: utf-8 -*-
from odoo import fields, models


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'

    voluntary_contribution = fields.Monetary(
        string='Voluntary contribution',
        currency_field="company_currency_id",
        help="Voluntary contribution made by the cooperator while buying a share."
    )
    unit_composition = fields.Integer(
        string='Unit composition',
        help="How many people compose the consumption unit."
    )
    join_commission = fields.Selection(
        selection = [
            ('botiga', _('Tasques de botiga: atenció als socis, neteja, omplir prestatgeries, etc.')),
            ('local', _('Comissió de local i manteniment')),
            ('comptabilitat', _('Comissió de comptabilitat')),
            ('juridica', _('Comissió jurídica')),
            ('productes', _('Comissió de productes i proveïdores')),
            ('comunicacio_ext', _('Comissió de comunicació externa')),
            ('comunicacio_int', _('Comissió de comunicació interna')),
            ('informatica', _('Comissió informàtica')),
            ('benvinguda', _('Comissió de benvinguda i participació')),
            ('activitats', _('Comissió d’activitats'))
        ],
        help = 'Which commissions people would like to join.',
        string = 'Join commission'
    )
