import customtkinter as ctk
import cv2
import numpy as np
import math
import time
from PIL import Image, ImageTk, ImageDraw
import os
import sys
import csv

# =========================================================
# 프로젝트 루트 연결
# =========================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

if project_root not in sys.path:
    sys.path.append(project_root)

from src.vision import VisionController
from src.logic import StrumLogic
from src.audio_handler import AudioHandler


class AirGuitarGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =========================================================
        # WINDOW
        # =========================================================
        self.title("Air Guitar System Dashboard")
        self.geometry("1350x910")
        self.resizable(False, False)

        self.configure(
            fg_color="#ECECEC"
        )

        # =========================================================
        # LAYOUT
        # =========================================================
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=8)
        self.grid_rowconfigure(1, weight=2)

        # =========================================================
        # ENGINE
        # =========================================================
        self.vision = VisionController()
        self.logic = StrumLogic()
        self.audio = AudioHandler()

        # =========================================================
        # CAMERA
        # =========================================================
        self.cap = cv2.VideoCapture(0)

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            1280
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            720
        )

        # =========================================================
        # STATE
        # =========================================================
        self.current_chord = "E Minor 7"
        self.string_vibrations = [0] * 6
        self.downstrum_only = False  # 새로 추가할 변수 (기본값: 양방향)
        self.all_csv_data = []      # 전체 데이터를 저장할 리스트
        self.start_time = time.time() # 프로그램 시작 시간 기록

        # =========================================================
        # UI
        # =========================================================
        self.setup_camera_and_gesture()
        self.setup_chord_panel()

        # =========================================================
        # LOOP
        # =========================================================
        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        self.loop_id = self.after(200, self.update_frame)

    # =========================================================
    # LEFT FRAME
    # =========================================================
    def setup_camera_and_gesture(self):

        # =========================================================
        # CAMERA OUTER FRAME
        # =========================================================
        self.camera_outer = ctk.CTkFrame(
            self,
            corner_radius=40,
            fg_color="transparent"  # 기존 "#DADDE3" 에서 변경
        )

        self.camera_outer.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(20,10)
        )

        # =========================================================
        # CAMERA FRAME
        # =========================================================
        self.camera_frame = ctk.CTkFrame(
            self.camera_outer,
            corner_radius=36,
            fg_color="transparent",  # 기존 "#DADDE3" 에서 변경
            border_width=0
        )

        self.camera_frame.pack(
            padx=6,
            pady=6
        )

        self.camera_frame.configure(
            width=1100,
            height=700
        )

        self.camera_frame.grid_propagate(False)

        self.camera_label = ctk.CTkLabel(
            self.camera_frame,
            text=""
        )

        self.camera_label.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        # =========================================================
        # GESTURE AREA
        # =========================================================
        self.gesture_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.gesture_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(20,10),
            pady=(0,20)
        )

        self.gestures = [
            {"chord": "G Minor 7", "desc": "Rock Sign", "img_path": "rock.png"},
            {"chord": "G Major 7", "desc": "Two fingers", "img_path": "two.png"},
            {"chord": "D Major 7", "desc": "Three fingers", "img_path": "three.png"},
            {"chord": "D Dominant 7", "desc": "Open Hand", "img_path": "open.png"},
            {"chord": "A Dominant 7", "desc": "Thumb", "img_path": "thumb.png"},
            {"chord": "E Minor 7", "desc": "No gesture", "img_path": "none.png"}
        ]

        self.gesture_widgets = {}

        for i, gest in enumerate(self.gestures):

            self.gesture_frame.grid_columnconfigure(
                i,
                weight=1,
                uniform="gesture"
            )

            item_frame = ctk.CTkFrame(
                self.gesture_frame,
                corner_radius=24,
                fg_color="#E9EDF3",
                border_width=2,
                border_color="#DDE3EA"
            )

            item_frame.grid(
                row=0,
                column=i,
                sticky="nsew",
                padx=5,
                pady=4
            )

            img_path = os.path.join(
                current_dir,
                "gui",
                gest["img_path"]
            )

            try:

                pil_img = Image.open(img_path)

                ctk_img = ctk.CTkImage(
                    light_image=pil_img,
                    dark_image=pil_img,
                    size=(60, 60)
                )

                img_label = ctk.CTkLabel(
                    item_frame,
                    image=ctk_img,
                    text=""
                )

                img_label.image = ctk_img

                img_label.pack(
                    pady=(16, 8)
                )

            except:
                pass

            chord_label = ctk.CTkLabel(
                item_frame,
                text=gest["chord"],
                font=("Arial", 16, "bold"),
                text_color="#111111"
            )

            chord_label.pack()

            desc_label = ctk.CTkLabel(
                item_frame,
                text=gest["desc"],
                font=("Arial", 12),
                text_color="#7A7A7A"
            )

            desc_label.pack(
                pady=(4, 16)
            )

            self.gesture_widgets[gest["chord"]] = item_frame

    # =========================================================
    # RIGHT FRAME
    # =========================================================
    def setup_chord_panel(self):

        # =========================================================
        # CHORD PANEL
        # =========================================================
        self.chord_frame = ctk.CTkFrame(
            self,
            corner_radius=24,
            fg_color="#161616",
            border_width=2,
            border_color="#2E2E2E"
        )

        self.chord_frame.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(10,20),
            pady=(0,20)
        )

        # =========================================================
        # LAYOUT
        # =========================================================
        self.chord_frame.grid_columnconfigure(0, weight=1)
        self.chord_frame.grid_columnconfigure(1, weight=4)
        self.chord_frame.grid_rowconfigure(0, weight=1)

        # =========================================================
        # STATUS GLOW
        # =========================================================
        self.status_canvas = ctk.CTkCanvas(
            self.chord_frame,
            width=70,
            height=70,
            bg="#161616",
            highlightthickness=0
        )

        self.status_canvas.grid(
            row=0,
            column=0,
            padx=(18, 5),
            pady=6
        )

        self.status_canvas.create_oval(
            12, 12, 58, 58,
            fill="#3E3200",
            outline=""
        )

        self.status_canvas.create_oval(
            22, 22, 48, 48,
            fill="#BDBDBD",  # 처음엔 꺼진 상태(회색)로 시작하도록 변경
            outline="",
            tags="inner_glow" # 태그 추가
        )

        # 클릭 이벤트 바인딩 추가
        self.status_canvas.bind("<Button-1>", self.toggle_strum_mode)

        # =========================================================
        # TEXT AREA
        # =========================================================
        self.text_frame = ctk.CTkFrame(
            self.chord_frame,
            width=220,
            fg_color="transparent"
        )

        self.text_frame.grid_propagate(False)

        self.text_frame.grid(
            row=0,
            column=1,
            sticky="w"
        )

        self.chord_title_label = ctk.CTkLabel(
            self.text_frame,
            text="CURRENT CHORD",
            font=("Arial", 11, "bold"),
            text_color="#8A8A8A"
        )

        self.chord_title_label.pack(
            anchor="w",
            pady=(4, 0)
        )

        self.current_chord_label = ctk.CTkLabel(
            self.text_frame,
            text="E Minor 7",
            width=220,
            anchor="w",
            font=("Arial", 30, "bold"),
            text_color="#FFD700"
        )

        self.current_chord_label.pack(
            anchor="w"
        )

        self.chord_sub_label = ctk.CTkLabel(
            self.text_frame,
            text="Air Guitar Active",
            font=("Arial", 12),
            text_color="#707070"
        )

        self.chord_sub_label.pack(
            anchor="w",
            pady=(0, 6)
        )

    # =========================================================
    # UPDATE UI
    # =========================================================
    # 새로 추가할 토글 함수
    def toggle_strum_mode(self, event=None):
        self.downstrum_only = not self.downstrum_only

        if self.downstrum_only:
            # 켜짐 (아래로만)
            outer = "#3E3200"
            inner = "#FFD700"
            sub_text = "Downstrum Only"
        else:
            # 꺼짐 (양방향)
            outer = "#3A3A3A"
            inner = "#BDBDBD"
            sub_text = "Bidirectional Strum"

        self.status_canvas.delete("all")
        self.status_canvas.create_oval(12, 12, 58, 58, fill=outer, outline="")
        self.status_canvas.create_oval(22, 22, 48, 48, fill=inner, outline="")
        self.chord_sub_label.configure(text=sub_text)

    def update_ui_state(self, active_chord):
        display_chord = (
            "E Minor 7"
            if active_chord == "E Minor 7"
            else active_chord
        )

        self.current_chord_label.configure(
            text=display_chord
        )

        # 상태 캔버스(status_canvas) 업데이트 부분은 지우고 버튼만 업데이트합니다.
        for chord_name, frame in self.gesture_widgets.items():
            if chord_name == display_chord:
                frame.configure(
                    fg_color="#F6E7BA",
                    border_color="#FFD700"
                )
            else:
                frame.configure(
                    fg_color="#E9EDF3",
                    border_color="#DDE3EA"
                )

    # =========================================================
    # DRAW STRING
    # =========================================================
    def draw_vibrating_string(
        self,
        frame,
        y,
        vibration,
        width,
        string_index,
        active=False
    ):

        points = []

        current_time = time.time()

        for x in range(160, width - 160, 10):

            wave = math.sin(
                (x * 0.05) + (current_time * 18)
            )

            offset = int(
                wave * vibration
            )

            points.append(
                [x, y + offset]
            )

        points = np.array(
            points,
            np.int32
        )

        base_thickness = (
            1 + (string_index * 0.5)
        )

        if active:

            color = (80, 220, 255)

            thickness = int(
                base_thickness + 2
            )

        else:

            color = (255, 255, 255)

            thickness = int(
                base_thickness
            )

        cv2.polylines(
            frame,
            [points],
            False,
            color,
            thickness
        )

    # =========================================================
    # UPDATE FRAME
    # =========================================================
    def update_frame(self):

        success, frame = self.cap.read()

        if success:

            frame = cv2.flip(
                frame,
                1
            )

            h, w, _ = frame.shape

            frame, strum_y, gesture_name = (
                self.vision.process_frame(frame)
            )

            chord_name = (
                self.logic.determine_chord(
                    gesture_name
                )
            )

            crossed_strings = (
                self.logic.check_strings(
                    strum_y,
                    self.downstrum_only
                )
            )

            if crossed_strings:

                for string_index in crossed_strings:

                    self.audio.play_string(
                        chord_name,
                        string_index
                    )

                    self.string_vibrations[
                        string_index
                    ] = 10

            # =========================================================
            # STRINGS
            # =========================================================
            for i, string_y in enumerate(
                self.logic.strings_y
            ):

                y = int(
                    string_y * h
                )

                vibration = (
                    self.string_vibrations[i]
                )

                active = vibration > 1

                text_color = (
                    (80, 220, 255)
                    if active
                    else (230, 230, 230)
                )

                cv2.putText(
                    frame,
                    str(i + 1),
                    (120, y + 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    text_color,
                    2,
                    cv2.LINE_AA
                )

                self.draw_vibrating_string(
                    frame,
                    y,
                    vibration,
                    w,
                    i,
                    active
                )

                self.string_vibrations[i] *= 0.86

            # CSV 저장
            if strum_y is not None:

                elapsed_time = time.time() - self.start_time
                self.all_csv_data.append([elapsed_time, strum_y])

            else:

                elapsed_time = time.time() - self.start_time

                if self.all_csv_data:
                    last_y = self.all_csv_data[-1][1]
                    self.all_csv_data.append([elapsed_time, last_y])

            self.update_ui_state(
                chord_name
            )

            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # =========================================================
            # CAMERA SIZE FIXED
            # =========================================================
            target_w = 1100
            target_h = 700

            h_img, w_img = rgb.shape[:2]

            scale = max(
                target_w / w_img,
                target_h / h_img
            )

            new_w = int(
                w_img * scale
            )

            new_h = int(
                h_img * scale
            )

            image = Image.fromarray(rgb)

            image = image.resize(
                (new_w, new_h),
                Image.Resampling.BILINEAR
            )

            left = (
                new_w - target_w
            ) // 2

            top = (
                new_h - target_h
            ) // 2

            image = image.crop(
                (
                    left,
                    top,
                    left + target_w,
                    top + target_h
                )
            )

            # =========================================================
            # CAMERA ROUNDING
            # =========================================================
            mask = Image.new(
                "L",
                (target_w, target_h),
                0
            )

            draw = ImageDraw.Draw(mask)

            draw.rounded_rectangle(
                (0, 0, target_w, target_h),
                radius=28,
                fill=255
            )

            # =========================================================
            # CAMERA ROUND MASK
            # =========================================================
            rounded = Image.new(
                "RGBA",
                (target_w, target_h),
                (0, 0, 0, 0)
            )

            rounded.paste(
                image,
                (0, 0)
            )

            mask = Image.new(
                "L",
                (target_w, target_h),
                0
            )

            draw = ImageDraw.Draw(mask)

            draw.rounded_rectangle(
                (0, 0, target_w, target_h),
                radius=40,
                fill=255
            )

            rounded.putalpha(mask)

            image = rounded

            imgtk = ctk.CTkImage(
                light_image=image,
                size=(target_w, target_h)
            )

            self.camera_label.configure(
                anchor="center",
                image=imgtk,
                text=""
            )

            self.camera_label.image = imgtk

        self.loop_id = self.after(
            30,
            self.update_frame
        )

    # =========================================================
    # CLOSE
    # =========================================================
    def on_close(self):
        
        # 1. 예약된 루프 취소
        if hasattr(self, 'loop_id'):
            self.after_cancel(self.loop_id)

        # 2. 웹캠 및 OpenCV 자원 해제
        self.cap.release()
        cv2.destroyAllWindows()

        # 3. --- [새로 교체/추가할 영역] CSV 자동 저장 로직 ---
        if self.all_csv_data:  # 기록된 데이터가 있을 때만 저장 진행
            try:
                # app.py 파일이 있는 위치에 'csv' 폴더 경로 지정
                csv_folder = os.path.join(current_dir, "csv")
                
                # 폴더가 없으면 자동으로 생성
                if not os.path.exists(csv_folder):
                    os.makedirs(csv_folder)
                
                # 실행할 때마다 새로운 파일을 만들기 위해 현재 시각으로 파일명 생성
                # 예: hand_data_20260528_191530.csv
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                file_name = f"hand_data_{timestamp}.csv"
                file_path = os.path.join(csv_folder, file_name)
                
                # CSV 파일 쓰기
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Time_Seconds", "Y_Coordinate"]) # MATLAB에서 읽을 헤더명
                    writer.writerows(self.all_csv_data)            # 누적 데이터 기록
                    
                print(f"✅ 데이터가 성공적으로 저장되었습니다: {file_path}")
            except Exception as e:
                print(f"❌ CSV 저장 중 오류 발생: {e}")
        # -----------------------------------------------------

        # 4. Tkinter 창 종료 및 프로세스 깔끔하게 강제 종료
        self.quit()
        self.destroy()
        os._exit(0)


if __name__ == "__main__":

    app = AirGuitarGUI()

    app.mainloop()