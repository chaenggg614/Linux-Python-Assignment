import tkinter as tk
from tkinter import ttk
import calendar
from datetime import date

class CalendarOnly(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calendar (Step 1)")
        self.geometry("520x420")

        # 1) 현재 연/월 상태 보관
        today = date.today()
        self.year = today.year
        self.month = today.month

        # 달력 기준: 월요일 시작
        calendar.setfirstweekday(calendar.MONDAY)

        # 2) 상단: 타이틀/네비게이션/선택표시
        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")

        ttk.Button(top, text="◀", width=3, command=self.prev_month).pack(side="left")
        ttk.Button(top, text="▶", width=3, command=self.next_month).pack(side="right")

        self.title_var = tk.StringVar()
        ttk.Label(top, textvariable=self.title_var, font=("Segoe UI", 14, "bold")).pack()

        self.selected_var = tk.StringVar(value="날짜를 선택하세요")
        ttk.Label(self, textvariable=self.selected_var).pack(pady=(0,6))

        # 3) 요일 헤더 + 달력 그리드 영역
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10)
        for i, wd in enumerate(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]):
            ttk.Label(header, text=wd, anchor="center", width=6).grid(row=0, column=i, padx=2)

        self.grid_frame = ttk.Frame(self)
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 초기 렌더링
        self.render_month()

    

    def render_month(self):
        """현재 self.year/self.month 기준으로 버튼 그리기"""
        # 타이틀 업데이트
        self.title_var.set(f"{self.year}-{self.month:02d}")

        # 기존 셀/버튼 제거
        for w in self.grid_frame.winfo_children():
            w.destroy()

        # 4) calendar.monthcalendar: 0은 공백, 그 외엔 일(day) 숫자
        #    예: [[0,0,1,2,3,4,5],[6,7,8,9,10,11,12], ...]
        weeks = calendar.monthcalendar(self.year, self.month)

        self.day_buttons = []
        for r, week in enumerate(weeks):
            row_btns = []
            for c, d in enumerate(week):
                if d == 0:
                    # 빈 셀
                    ttk.Label(self.grid_frame, text="", width=6)\
                        .grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                    row_btns.append(None)
                else:
                    # 날짜 버튼: 클릭 시 on_pick_day(d)
                    btn = ttk.Button(
                        self.grid_frame,
                        text=f"{d:02d}",
                        width=6,
                        command=lambda day=d: self.on_pick_day(day)
                    )
                    btn.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
                    row_btns.append(btn)
            self.day_buttons.append(row_btns)

        # 셀 비율: 창 크기 따라 적절히 늘어나도록
        for i in range(7):
            self.grid_frame.grid_columnconfigure(i, weight=1)
        for i in range(len(weeks)):
            self.grid_frame.grid_rowconfigure(i, weight=1)

    
    def on_pick_day(self, day: int):
        """날짜 버튼 클릭 시 호출: 선택 표시 업데이트"""
        self.selected_var.set(f"선택한 날짜: {self.year}-{self.month:02d}-{day:02d}")
        # (다음 단계에서: 여기서 To-Do 패널에 해당 날짜를 로드할 거야)

    
    def prev_month(self):
        if self.month == 1:
            self.year -= 1
            self.month = 12
        else:
            self.month -= 1
        self.render_month()

    def next_month(self):
        if self.month == 12:
            self.year += 1
            self.month = 1
        else:
            self.month += 1
        self.render_month()

