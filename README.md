<p align="center">
  <img src="https://github.com/RedRyan5154/panik-core/blob/master/asstes/logo.png?raw=true" alt="Panik-Core's logo"/>
</p>

# Welcome to the Panik-Core engine

THE python graphical library

The panik-core engine was built around pygame removing small mistakes that often unexperienced pygame developers do that feed on performance.  With panik-core, you will finish your first project in no time with the help of pre-made game object classes such as Entitys with collision, Parents and its sophisticated gui widgets using pygame_gui.

---

# A minimal window
```python
import panik_core as pk


class Game:
    def __init__(self):
        self.win = pk.Window("My Window", 1080, 720)
        self.win.showfps = True

    def run(self):
        run = 1

        while run:
            self.win.tick(0)

            for event in pk.Events.get():
                if (
                    event.type == pk.QUIT
                    or event.type == pk.KEY_PRESSED
                    and event.key == pk.kQ
                ):
                    run = 0

            window.render()


if __name__ == "__main__":
    game = Game()
    game.run()

```
