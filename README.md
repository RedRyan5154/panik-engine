<p align="center">
  <img src="https://github.com/RedRyan5154/panik-core/blob/master/asstes/logo.png?raw=true" alt="Panik-Core's logo"/>
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
import panik_core

window = panik_core.Window("My test window", 600, 400)  # create a window
window.showfps = True


def main():
    run = 1
    while run:
        window.tick(30)  # clock at 30 FPS
        for event in panik_core.Events.get():
            if event.type == panik_core.QUIT:
                run = 0
                panik_core.quit()

        window.render()


if __name__ == "__main__":
    main()

```
