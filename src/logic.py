import time

class StrumLogic:

    def __init__(self):

        self.strings_y = [
            0.42,
            0.48,
            0.54,
            0.60,
            0.66,
            0.72
        ]

        self.prev_y = None

        self.last_trigger_times = [0] * 6

        self.cooldown = 0.08

    # ======================================
    # 줄 충돌 체크
    # ======================================
    def check_strings(self, current_y, downstrum_only=False):

        if current_y is None:
            self.prev_y = None
            return []

        current_time = time.time()
        crossed_strings = []

        if self.prev_y is not None:
            for i, string_y in enumerate(self.strings_y):
                
                # 상태에 따른 교차 판정 분기
                if downstrum_only:
                    # 아래로 칠 때만 (이전 y가 더 작고, 현재 y가 더 클 때)
                    crossed = (self.prev_y < string_y and current_y >= string_y)
                else:
                    # 양방향 모두
                    crossed = (
                        (self.prev_y < string_y and current_y >= string_y)
                        or
                        (self.prev_y > string_y and current_y <= string_y)
                    )

                if crossed:
                    if (current_time - self.last_trigger_times[i]) > self.cooldown:
                        crossed_strings.append(i)
                        self.last_trigger_times[i] = current_time

        self.prev_y = current_y

        return crossed_strings

    # ======================================
    # 코드 결정
    # ======================================

    def determine_chord(self, gesture_name):

        chord_map = {

            "FIST": "G Minor 7",

            "V_SIGN": "G Major 7",

            "THREE": "D Major 7",

            "OPEN_HAND": "D Dominant 7",

            "THUMB_UP": "A Dominant 7"
        }

        return chord_map.get(
            gesture_name,
            "E Minor 7"
        )