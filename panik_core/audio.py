import pygame


class Audio:
    def __init__(self):
        self.volume = 100

    def startAudio(self, path, volume=100, loop=-1):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume / 100)
        pygame.mixer.music.play(loop)

    def setVolume(self, volume):
        pygame.mixer.music.set_volume(volume / 100)

    def increaseVol(self, v):
        self.setVolume(min(255, pygame.mixer.music.get_volume() + v))

    def decreaseVol(self, v):
        self.setVolume(max(0, pygame.mixer.music.get_volume() - v))

    def mute(self):
        pygame.mixer.music.set_volume(0.0)

    def unmute(self):
        global volume_
        pygame.mixer.music.set_volume(volume_ / 100)

    def toggleMute(self):
        if pygame.mixer.music.get_volume() == 0.0:
            self.unmute()
        else:
            self.mute()

    def playAudio(self, path):
        sound = pygame.mixer.Sound(path)
        sound.play()
