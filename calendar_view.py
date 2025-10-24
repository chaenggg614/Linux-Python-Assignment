import tkinter as tk
from tkinter import ttk
import calendar
from datetime import date
from todo import TodoPanel
import storage

class CalendarOnly(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Calendar")
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

        # 3) 요일 헤더 + 달력 그리드 영역
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # 왼쪽: 달력 테이블
        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True)
        self.table = ttk.Frame(left)
        self.table.pack(fill="both", expand=True)

        # 오른쪽: To-Do 패널
        self.todo = TodoPanel(main, on_changed=self.render_month)
        self.todo.pack(side="left", fill="both", expand=False, padx=(10,0))

        self.selected_var = tk.StringVar(value="select the date") 
        self.selected_label = ttk.Label(self, textvariable=self.selected_var)
        self.selected_label.pack(pady=(0, 6))


        # 초기 렌더링
        self.render_month()

    

    def render_month(self):
        # 타이틀
        self.title_var.set(f"{self.year}-{self.month:02d}")

        # 테이블 비우기
        for w in self.table.winfo_children():
            w.destroy()

        # 0행: 요일 헤더
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for c, wd in enumerate(weekdays):
            ttk.Label(self.table, text=wd, anchor="center")\
                .grid(row=0, column=c, sticky="nsew", padx=2, pady=(0, 4))

        # 1~: 날짜 버튼
        weeks = calendar.monthcalendar(self.year, self.month)
        for r, week in enumerate(weeks, start=1):
            for c, d in enumerate(week):
                if d == 0:
                    ttk.Label(self.table, text="")\
                        .grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
                else:
                    ttk.Button(
                        self.table, text=f"{d:02d}",
                        command=lambda day=d: self.on_pick_day(day)
                    ).grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        # 칼럼/행 확장
        for i in range(7):
            self.table.grid_columnconfigure(i, weight=1)
        for i in range(len(weeks) + 1):
            self.table.grid_rowconfigure(i, weight=1)

    
    def on_pick_day(self, day: int):
        self.selected_var.set(f"selected date: {self.year}-{self.month:02d}-{day:02d}")
        self.todo.set_date(self.year, self.month, day)

    
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

