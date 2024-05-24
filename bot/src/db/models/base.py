from sqlalchemy.orm import declarative_base, DeclarativeMeta

# Base = declarative_base()

class MyBaseClass(object):
    async def update(self, **kwargs):
        for key, val in kwargs.items():
            if hasattr(self, key) and val:
                setattr(self, key, val)

Base = declarative_base(cls=MyBaseClass, metaclass=DeclarativeMeta)