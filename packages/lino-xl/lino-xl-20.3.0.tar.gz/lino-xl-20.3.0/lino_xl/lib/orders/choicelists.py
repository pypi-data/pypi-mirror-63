# -*- coding: UTF-8 -*-
# Copyright 2019-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino_xl.lib.ledger.choicelists import VoucherStates
from lino.api import dd


class OrderStates(VoucherStates):
    pass

add = OrderStates.add_item
add('10', _("Waiting"), 'draft', is_editable=True)
add('20', _("Active"), 'active', is_editable=True)
add('30', _("Urgent"), 'urgent', is_editable=True)
add('40', _("Done"), 'registered')
add('50', _("Cancelled"), 'cancelled')
