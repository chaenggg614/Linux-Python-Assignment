import tkinter as tk
from tkinter import ttk, messagebox
import storage

class TodoPanel(ttk.LabelFrame):
    def __init__(self, master, on_changed):
        super().__init__(master, text="To-Do", padding=8)
        self.on_changed = on_changed
        self.y = self.m = self.d = None

        # 상단: 선택된 날짜 라벨
        self.sel_var = tk.StringVar(value="select the date")
        ttk.Label(self, textvariable=self.sel_var).pack(anchor="w", pady=(0,6))

        # 리스트 + 스크롤
        self.listbox = tk.Listbox(self, height=18)
        self.listbox.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(self, command=self.listbox.yview)
        sb.pack(side="left", fill="y")
        self.listbox.config(yscrollcommand=sb.set)

        # 우측 버튼 영역
        right = ttk.Frame(self); right.pack(side="left", fill="y", padx=(8,0))
        self.entry = ttk.Entry(right, width=28); self.entry.pack(pady=(0,6))
        ttk.Button(right, text="+ Add", command=self.add).pack(fill="x", pady=2)
        ttk.Button(right, text="✓ Toggle", command=self.toggle).pack(fill="x", pady=2)
        ttk.Button(right, text="x Delete", command=self.delete).pack(fill="x", pady=2)

    # 외부(달력)에서 날짜가 선택되면 호출
    def set_date(self, y: int, m: int, d: int):
        self.y, self.m, self.d = y, m, d
        self.sel_var.set(f"{y}-{m:02d}-{d:02d}")
        self.refresh()

    def refresh(self):
        self.listbox.delete(0, "end")
        if self.d is None: return
        for t in storage.tasks_for(self.y, self.m, self.d):
            prefix = "[✓] " if t.get("done") else "[ ] "
            self.listbox.insert("end", prefix + t["text"])

    def add(self):
        if self.d is None:
            messagebox.showwarning("No day")
            return
        text = self.entry.get().strip()
        if not text: return
        storage.tasks_for(self.y, self.m, self.d).append({"text": text, "done": False})
        self.entry.delete(0, "end")
        self.refresh()
        self.on_changed()

    def toggle(self):
        if self.d is None: return
        sel = self.listbox.curselection()
        if not sel: return
        i = sel[0]
        tasks = storage.tasks_for(self.y, self.m, self.d)
        if 0 <= i < len(tasks):
            tasks[i]["done"] = not tasks[i].get("done")
            self.refresh()
            self.on_changed()

    def delete(self):
        if self.d is None: return
        sel = self.listbox.curselection()
        if not sel: return
        i = sel[0]
        tasks = storage.tasks_for(self.y, self.m, self.d)
        if 0 <= i < len(tasks):
            tasks.pop(i)
            self.refresh()
            self.on_changed()


