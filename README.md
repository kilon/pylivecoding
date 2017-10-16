
# pylivecoding
Pylivecoding is a live coding environment implementation inspired by Smalltalk

Essentially this library reloads modules and updates all live instances of classes defined in those modules to the latest code of the class definition without losing anny of the data. This way you can change code in your favorite code editor and IDE and immediately see the results without any delays. 

# How to use

Pylivecoding is an extremely small library and its functionality is super simple. 
First of course you import the single module pylovecoding.py to your project. 
```python
import livecoding
```
Then you create a new instance of the LiveEnviroment. 
LiveEnviroment is basically the class that handles live coding, keeping track of live objects and updating them.
