import importlib,pdb,sys,traceback,inspect

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
        print("start storing old live classes............")
        for module in self.live_modules:
            live_module_name_list = [mod for mod in sys.modules.keys() if  mod.endswith(module)]
            live_module_name = live_module_name_list[0]
            live_classes[module] = []
            print("\nchecking module: ", live_module_name)
            for mod in live_module_name_list:

                if hasattr(sys.modules[mod],"live_environment"):
                    #print("updating module",mod)
                    sys.modules[mod].live_environment.update()
            for old_obj in sys.modules[live_module_name].__dict__.values():
                #print("checking  {} for class definitions using value ".format(live_module_name,old_obj))
                if inspect.isclass(old_obj) and hasattr(old_obj,"instances"):
                    live_classes[module].append(old_obj)
                    print("appended {} to the list with type {}".format(old_obj, type(old_obj)))
        self._live_classes = live_classes
        print("\n live_classes : {} \n".format(self._live_classes))
        return live_classes

    def update(self):
        print("\n***** START CODE RELOAD ******\n")
        self.store_old_live_classes()
        for live_module in self.live_classes: #the name of the module is used as a key for the dict that stores all
            print("iterating through ",live_module)
            # live classes

            live_module_name_list = [mod for mod in sys.modules.keys() if  mod.endswith(live_module)]
            live_module_name = live_module_name_list[0]
            #print("code reload for module: ", live_module_name)

            live_classes_ids = [id(cl) for cl in self.live_classes[live_module]]
            #print("code reload for module: ", live_module_name)

            importlib.reload(sys.modules[live_module_name])
            live_classes_ids = [id(cl) for cl in self.live_classes[live_module]]

            #if live_module == "cyclops.morpheas":
                #pdb.set_trace()
            for live_class in self.live_classes[live_module]:
                print("iterate class : {} with instances: {}".format(live_class,live_class.instances))
                new_live_class = eval("sys.modules[live_module_name]." + live_class.__name__)

                for live_instance in live_class.instances:
                    print("iterate instance :",live_instance)
                    backup_instances = live_instance.__class__.instances
                    live_instance.__class__ = new_live_class
                    print("reloading instance \n instance : {} id: {} \n old class: {} id: {} \n new class : {} id: {"
                          "} \n"
                          "".format(live_instance,id(live_instance),live_class,id(live_class),new_live_class,id(new_live_class)))
                    live_instance.__class__.instances = backup_instances
        print("\n**********END CODE RELOAD************\n")