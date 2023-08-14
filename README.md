<p align="center">
  <img src="https://github.com/RedRyan5154/panik-core/blob/master/panik_engine/asstes/logo.png?raw=true" alt="Panik-Core's logo"/>
</p>

# Welcome to the Panik-Engine

THE python game engine

The panik-engine was built around the excelent pygame-ce library. It provides a simple yer powerful set of tools to make game development fast and simple.

---

# A minimal window
```python
import panik_engine as pk


class Game:
    def __init__(self):
        self.win = pk.Window(1080, 720, "My Window")
        self.win.showfps = True

    def run(self):
        run = 1

        while run:
            dt = self.win.tick(0)

            for event in pk.Events.get():
                if (
                    event.type == pk.QUIT
                    or event.type == pk.KEY_PRESSED
                    and event.key == pk.kQ
                ):
                    run = 0

            self.win.render()


if __name__ == "__main__":
    game = Game()
    game.run()

```
