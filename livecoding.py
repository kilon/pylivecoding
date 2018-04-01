
def private():
    from sys import modules
    from importlib import reload

    # this is the environment registry that tracks live modules and associate live classes
    registry = {} # { module: { name: LiveObject }
    class LiveObjectConstructor(type):
        def __new__(meta, name, bases, NS):
            live_classes = registry.setdefault( NS['__module__'], {} ) # set and/or retrieve
            old_live_class = live_classes.get( name, None ) # return if exists
            NS['__class__'] = property(lambda self: live_classes[name]) # old instance returns new class
            new_live_class = live_classes[name] = type.__new__(meta,name,bases,NS) # update on reload()
            return new_live_class

    class LiveObject(object, metaclass=LiveObjectConstructor):
        __slots__ = []

    def update_environment(): # TODO: detect updates automatically
        for live_module, live_classes in registry.items():
            mod = modules[live_module]
            reload( mod )
            moddict = mod.__dict__
            for k in live_classes: # search for removed classes
                if k not in moddict: live_classes.pop(k)
        
    return LiveObject, update_environment # make these public

LiveObject, update_env = private()
del private # prevent private access
