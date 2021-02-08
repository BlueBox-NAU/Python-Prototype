from pyramid.security import Allow
from pyramid.security import Everyone

class Member(object):
    __acl__ = [
        (Allow, Everyone, 'validUser'),
        (Allow, 'group:editors', 'validUser'),
        ]
