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