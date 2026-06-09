import pygame
from pathlib import Path

class AudioHandler:

    def __init__(self):

        pygame.mixer.pre_init(
            frequency=44100,
            size=-16,
            channels=2,
            buffer=256
        )

        pygame.mixer.init()

        pygame.mixer.set_num_channels(32)

        self.sounds = {}

        # ==================================
        # 경로
        # ==================================

        BASE_DIR = Path(__file__).resolve().parent.parent

        ASSETS_PATH = BASE_DIR / "assets"

        # ==================================
        # 코드별 파일
        # ==================================

        self.chord_strings = {

            "E Minor 7": [
                "Em7_6.wav",
                "Em7_5.wav",
                "Em7_4.wav",
                "Em7_3.wav",
                "Em7_2.wav",
                "Em7_1.wav"
            ],

            "A Dominant 7": [
                "A7_6.wav",
                "A7_5.wav",
                "A7_4.wav",
                "A7_3.wav",
                "A7_2.wav",
                "A7_1.wav"
            ],

            "D Major 7": [
                "DM7_6.wav",
                "DM7_5.wav",
                "DM7_4.wav",
                "DM7_3.wav",
                "DM7_2.wav",
                "DM7_1.wav"
            ],

            "D Dominant 7": [
                "D7_6.wav",
                "D7_5.wav",
                "D7_4.wav",
                "D7_3.wav",
                "D7_2.wav",
                "D7_1.wav"
            ],

            "G Major 7": [
                "GM7_6.wav",
                "GM7_5.wav",
                "GM7_4.wav",
                "GM7_3.wav",
                "GM7_2.wav",
                "GM7_1.wav"
            ],

            "G Minor 7": [
                "Gmin7_6.wav",
                "Gmin7_5.wav",
                "Gmin7_4.wav",
                "Gmin7_3.wav",
                "Gmin7_2.wav",
                "Gmin7_1.wav"
            ]
        }

        # ==================================
        # wav 로드
        # ==================================

        try:

            for chord_name, files in self.chord_strings.items():

                self.sounds[chord_name] = []

                for file in files:

                    path = ASSETS_PATH / file

                    sound = pygame.mixer.Sound(
                        str(path)
                    )

                    self.sounds[chord_name].append(sound)

            print("✅ wav 로드 완료")

        except Exception as e:

            print(f"❌ wav 로드 실패: {e}")

    # ======================================
    # 줄 재생
    # ======================================

    def play_string(self, chord_name, string_index):

        if chord_name not in self.sounds:
            return

        if string_index < 0 or string_index >= 6:
            return

        sound = self.sounds[chord_name][string_index]

        channel = pygame.mixer.find_channel()

        if channel:
            channel.play(sound)