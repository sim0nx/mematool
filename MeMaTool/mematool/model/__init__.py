"""The application's model objects"""
from mematool.model.meta import Session, metadata, Base


from mematool.model.tmpmember import TmpMember
from mematool.model.member import Member
from mematool.model.payment import Payment
from mematool.model.group import Group
from mematool.model.paymentmethod import Paymentmethod
from mematool.model.domain import Domain
from mematool.model.alias import Alias


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
    meta.Base.metadata.bind = engine
