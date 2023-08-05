from spintop.generators import Generator

from spintop.models import (
    TestRecordSummary, 
    FeatureRecord, 
    SpintopTestRecord
)

from ..logs import _logger

logger = _logger('persistence')


class MissingMapper(Exception):
    def __init__(self, cls):
        super().__init__("Mapper for class {!r} is mandatory.".format(cls))

class NoMapperForObject(Exception):
    def __init__(self, obj, mappers):
        super(NoMapperForObject, self).__init__(
            'There are no known mapper able to interact with obj {!r} of class {}. Declared mappers are: {}'.format(
                obj,
                obj.__class__,
                [cls.__name__ for cls in mappers]
            )
        )
        
class DuplicateMapperClassName(Exception):
    def __init__(self, objcls):
        super(DuplicateMapperClassName, self).__init__(
            'The name of the class {} is duplicate. The class name linked to a mapper must be unique.'.format(
                objcls,
            )
        )

class PersistenceFacade(object):
    logger = logger
    def create(self, records):
        raise NotImplementedError()
        
    def retrieve(self, query, deserialize=True):
        """Generator."""
        raise NotImplementedError()
        
    def update(self, records, upsert=False):
        raise NotImplementedError()
    
    def delete(self, match_query):
        raise NotImplementedError()
    
    def create_records_generator(self):
        return PersistenceGenerator(self)
        
def create_mapper_name_index(mappers):
    mappers_name_index = {}
    for mapped_cls, mapper in mappers.items():
        name = mapped_cls.__name__
        if name in mappers_name_index:
            raise DuplicateMapperClassName(mapped_cls)
        mappers_name_index[name] = mapper
    return mappers_name_index
    
class PersistenceGenerator(Generator):
    def __init__(self, facade):
        super().__init__()
        self.facade = facade
    
    def __call__(self, *args, **kwargs):
        return self.facade.retrieve(*args, **kwargs)

class Mapper(object):
    def init(self):
        pass