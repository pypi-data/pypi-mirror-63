from collections.abc import Mapping
from collections import OrderedDict
from itertools import chain, starmap

from .meta import MetaField
    
class _MetaFieldAccessor(object):
    def __init__(self, meta_field):
        self.field = meta_field

    def __call__(self, obj):
        return obj.getattr_from_field(self.field)

class _PythonAccessor(object):
    def __init__(self, accessor):
        self.accessor = accessor

    def __call__(self, obj):
        return self.accessor.__get__(obj, type(obj))

class _ValueAccessor(object):
    def __init__(self, value):
        self.value = value
    
    def __call__(self, obj):
        return self.value
    
    
class DataClassPrimitiveView(object):
    def __init__(self, key_values_mapping={}):
        self.build_accessors(key_values_mapping)
        
    def build_accessors(self, key_values_mapping):
        """ Creates a dict of callable
        """

        self._accessors_mapping = _build_accessors(key_values_mapping)
        
    def apply(self, data_obj, flatten_dict=False, attribute_error_policy='ignore'):
        result = {}
        for accessor_key, accessor_value in self._accessors_mapping.items():
            try:
                key = _apply_single_accessor(accessor_key, data_obj)
                value = _apply_single_accessor(accessor_value, data_obj)
            except AttributeError:
                if attribute_error_policy == 'ignore':
                    continue
                else:
                    raise
            
            if isinstance(key, tuple) and not flatten_dict:
                # Push value deep into a nested dictionnary
                # key = (x, y, z)
                # result.update({x: {y: {z: value}}})
                update(result, deepen_value_in_dict(key, value))
            else:
                # or keep as is (flat)
                # key = (x, y, z)
                # result[(x, y, z)] = value
                result[key] = value
            
        return result

def _build_accessors(key_values_mapping):
    flat_key_values_mapping = flatten_dict(key_values_mapping)
    return {_build_single_accessor(key): _build_single_accessor(value) for key, value in flat_key_values_mapping.items()}

def _build_single_accessor(obj):
    if isinstance(obj, tuple):
        return tuple(_build_single_accessor(subobj) for subobj in obj)
    elif isinstance(obj, MetaField):
        return _MetaFieldAccessor(obj)
    elif isinstance(obj, property):
        return _PythonAccessor(obj)
    elif callable(obj):
        return obj # Obj is an accessor
    else:
        return _ValueAccessor(obj) # Will always return obj
    
def _apply_single_accessor(accessor, obj):
    if isinstance(accessor, tuple):
        return tuple(_apply_single_accessor(subaccessor, obj) for subaccessor in accessor)
    else:
        return accessor(obj)

def default_cls_missing_view_fn(cls):
    raise NotImplementedError()

class ComplexPrimitiveView(object):
    def __init__(self, base_cls, cls_missing_view_fn=None):
        if cls_missing_view_fn is None: cls_missing_view_fn = default_cls_missing_view_fn
        
        self.base_cls = base_cls
        self.cls_missing_view_fn = cls_missing_view_fn
        self.custom_views = {}
        
    def _find_closest_parent(self, cls):
        closest_parent = None
        
        if cls in self.custom_views:
            return cls
        
        for match_cls in self.custom_views:
            possible_parent = None
            if issubclass(cls, match_cls):
                possible_parent = match_cls
            
            if possible_parent and (closest_parent is None or issubclass(possible_parent, closest_parent)):
                # possible parent is closer to cls than the previous closest parent.
                closest_parent = possible_parent
                
        return closest_parent
    
    def _find_view(self, cls):
        best_match = self._find_closest_parent(cls)
        if best_match:
            return self.custom_views[best_match]
        else:
            return self.cls_missing_view_fn(cls)
    
    def add_view(self, cls, view_mapping):
        self.custom_views[cls] = DataClassPrimitiveView(view_mapping)
        
    def apply(self, root_data_obj, flatten_dict=False, key_prefix=None):
        flatten_key_prefix = None
        if flatten_dict:
            if key_prefix is None:
                flatten_key_prefix = ()
            else:
                flatten_key_prefix = key_prefix
                
        result = self._apply_data_obj(root_data_obj, flatten_key_prefix=flatten_key_prefix)
        
        if not flatten_dict and key_prefix:
            return deepen_value_in_dict(key_prefix, result)
        else:
            return result
    
        
    
    def _apply_data_obj(self, data_obj, flatten_key_prefix=None):
        mapping = self._find_view(data_obj.__class__).apply(data_obj, flatten_dict=flatten_key_prefix is not None)
        
        flatten_key_prefix_built = _build_single_accessor(flatten_key_prefix)
        flatten_key_prefix_applied = _apply_single_accessor(flatten_key_prefix_built, data_obj)
        
        return self._apply_mapping(mapping, flatten_key_prefix=flatten_key_prefix_applied)
    
    def _apply_mapping(self, mapping, flatten_key_prefix=None):
        result = OrderedDict()
        
        for key, value in mapping.items():
            
            flat_key = None
            if flatten_key_prefix is not None:
                flat_key = join_key_prefix(flatten_key_prefix, key)
            
            discard_false_subvalue = False 
            
            if isinstance(value, self.base_cls):
                subvalue = self._apply_data_obj(value, flatten_key_prefix=flat_key)
                # If bool(subvalue) is False, then the sub-view returned an empty mapping or None. Do not consider it.
                discard_false_subvalue = True 
            elif isinstance(value, Mapping):
                subvalue = self._apply_mapping(value, flatten_key_prefix=flat_key)
                # If bool(subvalue) is False, the mapping is empty or none. Do not consider it.
                discard_false_subvalue = True 
            elif flat_key is not None:
                # limit case.
                # If flatten, we will .update the result instead of applying
                subvalue = {flat_key: value}
            else:
                subvalue = value
            
            if discard_false_subvalue and not subvalue:
                continue # discard
            
            if flat_key:
                for subkey in subvalue:
                    if subkey in result:
                        print("{} already in result.".format(subkey))
                update(result, subvalue)
            else:
                if key in result:
                    print("{} already in result.".format(key))
                update(result, {key: subvalue})
        
        return result

def join_key_prefix(key_prefix, key):
    if not isinstance(key, tuple):
        key = (key,)

    if not isinstance(key_prefix, tuple):
        key_prefix = (key_prefix,)
        
    return key_prefix + key

def deepen_value_in_dict(key_prefix, value):
    result = {}
    next_dict = result
    for key in key_prefix[:-1]:
        next_dict[key] = {}
        next_dict = next_dict[key]
    next_dict[key_prefix[-1]] = value
    
    return result

def flatten_dict(dictionary):
    """Flatten a nested dictionary structure"""

    tuplify = lambda key: key if isinstance(key, tuple) else (key,)

    def unpack(parent_key, parent_value):
        """Unpack one level of nesting in a dictionary"""
        try:
            items = parent_value.items()
        except AttributeError:
            # parent_value was not a dict, no need to flatten
            yield (parent_key, parent_value)
        else:
            for key, value in items:
                yield (parent_key + tuplify(key), value)


    # Put each key into a tuple to initiate building a tuple of subkeys
    dictionary = {tuplify(key): value for key, value in dictionary.items()}

    while True:
        # Keep unpacking the dictionary until all value's are not dictionary's
        dictionary = dict(chain.from_iterable(starmap(unpack, dictionary.items())))
        if not any(isinstance(value, dict) for value in dictionary.values()):
            break

    return dictionary

def update(d, u):
    for k, v in u.items():
        if isinstance(v, Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d