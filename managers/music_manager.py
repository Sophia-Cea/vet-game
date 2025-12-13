import pygame

class MusicManager:
    current_track = None
    volume = 0.05  # default cozy volume

    @classmethod
    def play(cls, track, loop=True, fade_ms=1000):
        """Play a music track. Won't restart if it's already playing."""
        if cls.current_track == track:
            return

        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(fade_ms)

        pygame.mixer.music.load(track)
        pygame.mixer.music.set_volume(cls.volume)
        pygame.mixer.music.play(-1 if loop else 0)
        cls.current_track = track

    @classmethod
    def stop(cls, fade_ms=1000):
        """Stop the current music track."""
        pygame.mixer.music.fadeout(fade_ms)
        cls.current_track = None
