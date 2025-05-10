# signals.py
from sqlalchemy.event import listens_for

from flask_app.game.currency.models import Currency
from flask_app.user.models import User


@listens_for(User, "after_insert")
def create_currency(mapper, connection, target):
    raise NotImplementedError("Need to use servuces")
    # new_currency = Currency(user_id=target.id)
    ## db.session.add(new_currency)
    ## db.session.commit()
    # return new_currency
