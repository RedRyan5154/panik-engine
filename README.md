<p align="center">
  <img src="https://github.com/RedRyan5154/panik-core/blob/master/assets/panik/logo.png?raw=true" alt="Panik-Core's logo"/>
</p>

# Welcome to the Panik-Core engine

THE python graphical library

The panik-core engine was built around pygame removing small mistakes that often unexperienced pygame developers do that feed on performance.  With panik-core, you will finish your first project in no time with the help of pre-made game object classes such as Entitys with collision, Parents and its sophisticated gui widgets using pygame_gui.

---
# Installation
Using pip:
```
pip install panik-core
```

Inside Python:
```python
from panik_core import *
```
# A minimal window
```python
from panik_core import *

window = Window("A minimal window", 600, 400) # create a window
window.background = (255, 255, 255)
window.showfps = True

ev = Events() # event object

def  main():
	run = 1
	while  run:
		window.tick(30) # set fps
		events = ev.get()
		for  event  in  events:
			if  event.type == ev.QUIT:
				run = 0
		window.update() # update the window

if  __name__ == '__main__':
	main()
```
