
# pylivecoding
Pylivecoding is a live coding environment implementation inspired by Smalltalk

Essentially this library reloads modules and updates all live instances of classes defined in those modules to the latest code of the class definition without losing any of the data/state. This way you can change code in your favorite code editor and IDE and immediately see the results without any delays. 

# How to use

Pylivecoding is an extremely small library and its functionality is super simple. 
First of course you import the single module pylovecoding.py to your project. 
```python
import livecoding
```
Then you create a new instance of the LiveEnviroment. 
```python
live_env = livecoding.LiveEnviroment()
```
LiveEnviroment is basically the class that handles live coding, keeping track of live objects and updating them. In order to do that it needs the modules where you will be live coding. 
```python
live_env.live_modules = ['cyclops.morpheas','cyclops.cyclopsMorphs','cyclops.booleanOperations']
```
In order for your modules to be reloaded and the live instances to be updated you have to issue the update command
```python
 live_env.update()
 ```
 All this should be coded in a module that won't be used for live coding. Also the update and general live coding makes sense for code that repeats so its better put this update inside a loop of some sort. 
 
 Your modules can be any kind of Python modules as long as they follow the following conditions
 - they will not use any ```python from module import *```. Currently this kind of import is not supported and will create side effects so avoid it use the usual ```python import mypackage.mymodule.mysubmodule```. You are allowed however to do this ```python import mypckage.mymodule.mysubmodule as mdl```
 - All the classes will have to be either a) subclasses of livecoding.LiveObject or b) do what LiveObject does, define a class variable named "instances" and in the __init__ add the instance to the variable 
 so (a) will look like this
 ```python
 import pylivecoding
 
 class MyClass(livecoding.LiveObject):
   instances = []
   
   def __init__(self):
     super().__init__()
 ```
 or (b) will look like this
 ```python
 class MyClass:
   instances = []
   
   def __init__(self):
     instances.append(self)
 ```
 Thats all you have to do and you can code as you awlays code following whatever style you want. 
 # Debugging live coding 
 Traditional debugging compared to live code debugging is like fire compared to nucleal power. Because not only you see the problems in your source code you can change the live code while still the debugger is stepping through your code. This allows coding Smalltalk style. In Smalltalk some coders code entirely inside the debugger , they make intential mistakes under the safety that they can correct their errors with no delays at all because there is no need to restard the debugger and each new error triggers the debugger again.When the error is fixed via live coding , the breakpoint can be removed and the debugger instructed to continue execution like nothing happened. 
 
 Fortunately python does provide such functionality through the use of post mortem debugging. Essentially it means that in the case of error the debugger triggers using the line that triggered the error as a temporary breakpoint. The code is the following
 
 ```python
 try:
  live_env.update()
  execute_my_code()
except Exception as inst:
  
  type, value, tb = sys.exc_info()
  traceback.print_exc()
  pdb.post_mortem(tb)
 ```
 
 As you can see we have here a usual exception handling code, inside the try we first live update our code to make sure it updated to the latest source code and execute our code , if an error occur or anyting else, it is stored and printed and then the debugger is triggered , hitting c inside pdb will continue execution first statement being updating to live code. 
 
The assumption here is that all this runs inside a loop of some sort so you can actually see the results of the updated code. Obviously if it is not and this is the last line of code , the application will just end  end execution after the debugger was instructed to continue with the "c" command ;) 

 # Future plans
 The library is far from finished. The Smalltalk enviroment comes with a wealth of conveniences and automations and a very powerful IDE. Generally Python is powerful enough to do those things and there are good enough IDEs out there but I will be replication some of the ideas. So to do list is the following
 
 - Make the library smart enough to detect changes inside modules and automatically update the live code/state
 - lift the restriction on imports
 - automatically wrap classes to track their instances
 - make the module list optional 
 


