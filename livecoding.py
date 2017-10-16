import importlib,pdb,sys,traceback
from IPython import embed as e

class LiveEnviroment:
    def __init__(self):
        self.live_modules=[]
        self._live_classes={}


    def register_module(self,name):
        if name in self.live_modules:
            raise ValueError("Error: a module with same name already registered")
        else:
            self.live_modules.append(name)

    @property
    def live_classes(self):
        return self._live_classes

    def update_live_classes(self):
        live_classes = {}
        for module in self.live_modules:
            live_classes[module] = []
            for old_obj in sys.modules[module].__dict__.values():
                if old_obj.__class__.__name__ == 'type':
                    live_classes[module].append(old_obj)
        self._live_classes = live_classes
        return live_classes

    def update(self):
        self.update_live_classes()
        for live_module in self.live_classes:
            #pdb.set_trace()
            new_live_class = 0
            live_classes_ids = [id(cl) for cl in self.live_classes[live_module]]
            importlib.reload(sys.modules[live_module])
            live_classes_ids = [id(cl) for cl in self.live_classes[live_module]]

            for live_class in self.live_classes[live_module]:
                new_live_class = eval("sys.modules[live_module]." + live_class.__name__)

                for live_instance in live_class.instances:
                    backup_instances = live_instance.__class__.instances
                    live_instance.__class__ = new_live_class
                    live_instance.__class__.instances = backup_instances
                    live_instance = 0

class LiveObject:
    instances=[]
    def __init__(self):
        if self.__class__.instances is []:
            self.__class__.instances.append(self)
        else:
            self.__class__.instances=[self]
