# -*- coding: utf-8 -*-
"""
Specific session stuff used to store the payment history logs
"""
import logging

from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base

logger = logging.getLogger(__name__)
ModelBase = declarative_base()


def includeme(config):
    """
    Pyramid Include's mechanism
    Setup the library specific session
    """
    logger.debug("Setting up database configuration for endi_payment")
    settings = config.get_settings()

    if 'endi_payment_db.url' in settings:
        # On a une connexion particulière pour l'édition des journaux
        prefix = 'endi_payment_db.'
        endi_payment_engine = engine_from_config(settings, prefix=prefix)
        from endi_base.models.base import DBBASE, DBSESSION
        DBSESSION.configure(
            binds={ModelBase: endi_payment_engine, DBBASE: DBSESSION.bind}
        )
        # Le bind a déjà été setté avant et il prend le dessus sur binds
        DBSESSION.bind = None

    else:
        # On utilise l'engine sqlalchemy par défaut (celui d'endi)
        # Pas besoin de spécifier le bind qui est le même qu'avant
        endi_payment_engine = engine_from_config(settings)

    from endi_payment.models import EndiPaymentHistory  # NOQA
    ModelBase.metadata.bind = endi_payment_engine
    ModelBase.metadata.create_all(endi_payment_engine)
    return True
