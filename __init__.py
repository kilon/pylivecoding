import importlib,pdb,sys,traceback

class LiveObject:
    instances=[]

    def __init__(self):
            self.__class__.instances.append(self)


class LiveEnvironment(LiveObject):
    instances = []
    def __init__(self):
        super().__init__()
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

    def store_old_live_classes(self):
        live_classes = {}
        for module in self.live_modules:
            live_module_name_list = [mod for mod in sys.modules.keys() if module in mod]
            live_module_name = live_module_name_list[0]
            live_classes[module] = []
            if hasattr(sys.modules[live_module_name],"live_environment"):
                sys.modules[live_module_name].live_environment.update()
            for old_obj in sys.modules[live_module_name].__dict__.values():
                if old_obj.__class__.__name__ == 'type' and hasattr(old_obj.__class__,"instances"):
                    live_classes[module].append(old_obj)
        self._live_classes = live_classes
        return live_classes

    def update(self):
        self.store_old_live_classes()
        for live_module in self.live_classes: #the name of the module is used as a key for the dict that stores all
            # live classes
            live_module_name_list = [mod for mod in sys.modules.keys() if  live_module in mod]
            live_module_name = live_module_name_list[0]
            #pdb.set_trace()
            new_live_class = 0
            live_classes_ids = [id(cl) for cl in self.live_classes[live_module]]
            importlib.reload(sys.modules[live_module_name])
            live_classes_ids = [id(cl) for cl in self.live_classes[live_module]]

            for live_class in self.live_classes[live_module]:
                new_live_class = eval("sys.modules[live_module_name]." + live_class.__name__)

                for live_instance in live_class.instances:
                    backup_instances = live_instance.__class__.instances
                    live_instance.__class__ = new_live_class
                    live_instance.__class__.instances = backup_instances
                    live_instance = 0