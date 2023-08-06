#-*-coding:utf-8-*-
import colander
import deform

from endi.forms import (
    range_validator,
    deferred_default_year,
    year_filter_node,
)
from endi.forms.widgets import CleanMappingWidget
from endi.forms.tasks.lists import PeriodSchema, AmountRangeSchema
from endi.forms.lists import BaseListsSchema
from endi.models.task.invoice import get_invoice_years


def get_list_schema():
    """
    Build a form schema used to list history entries
    """
    schema = BaseListsSchema().clone()
    del schema['search']

    node = colander.SchemaNode(
        colander.String(),
        name='official_number',
        title=u"Numéro de facture",
        missing=colander.drop
    )
    schema.insert(0, node)
    node = colander.SchemaNode(
        colander.Integer(),
        name='invoice_id',
        title="",
        widget=deform.widget.HiddenWidget(),
        missing=colander.drop
    )
    schema.insert(0, node)

    node = PeriodSchema(
        name="period",
        title="",
        validator=colander.Function(
            range_validator,
            msg=u"La date de début doit précéder la date de début"
        ),
        widget=CleanMappingWidget(),
        missing=colander.drop,
    )
    node['start'].title = u"Enregistré entre le"
    schema.insert(0, node)
    node = AmountRangeSchema(
        name='amount',
        title="",
        validator=colander.Function(
            range_validator,
            msg=u"Le montant de départ doit être inférieur ou égale "
            u"à celui de la fin"
        ),
        widget=CleanMappingWidget(),
        missing=colander.drop,
    )
    node['start'].title = u"Montant entre"
    schema.insert(0, node)

    node = colander.SchemaNode(
        colander.String(),
        name='action_type',
        title=u"Type d'action",
        widget=deform.widget.SelectWidget(
            values=(
                ('', u'Tous'),
                ('ADD', u'Ajout'),
                ('UPDATE', u'Modification'),
                ('DELETE', u'Suppression'),
            )
        ),
        missing=colander.drop,
    )
    schema.insert(0, node)

    node = year_filter_node(
        name='year',
        title=u"Année",
        query_func=get_invoice_years,
        default=deferred_default_year,
        default_val=('', u'Tous'),
        missing=colander.drop,
    )
    schema.insert(0, node)

    return schema
