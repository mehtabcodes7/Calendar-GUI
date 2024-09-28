import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import calendar

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Infinite Calendar")
        self.root.geometry("1100x800")
        self.root.minsize(800, 600)

        # Variables
        self.current_view = "month"
        self.current_date = datetime.now()
        self.dark_mode = False

        # Fonts
        self.font_large = ("Helvetica", 20, "bold")
        self.font_medium = ("Helvetica", 16)
        self.font_small = ("Helvetica", 12)

        # Themes
        self.light_theme = {
            "bg": "#f7f7f7",
            "fg": "#000000",
            "button_bg": "#4285F4",
            "button_fg": "#ffffff",
        }
        self.dark_theme = {
            "bg": "#303030",
            "fg": "#ffffff",
            "button_bg": "#5E5E5E",
            "button_fg": "#ffffff",
        }

        # Frames
        self.top_frame = tk.Frame(self.root, bg=self.light_theme['bg'])
        self.top_frame.pack(pady=20, fill=tk.X)

        self.nav_frame = tk.Frame(self.root, bg=self.light_theme['bg'])
        self.nav_frame.pack(pady=10, fill=tk.X)

        self.calendar_frame = tk.Frame(self.root, bg=self.light_theme['bg'])
        self.calendar_frame.pack(pady=20, fill="both", expand=True)

        # Center buttons in top frame
        self.create_button(self.top_frame, "Toggle Theme", self.toggle_theme).pack(side=tk.LEFT, padx=10, expand=True)
        self.create_button(self.top_frame, "Week View", self.show_week_view).pack(side=tk.LEFT, padx=10, expand=True)
        self.create_button(self.top_frame, "Month View", self.show_month_view).pack(side=tk.LEFT, padx=10, expand=True)

        # Center navigation buttons
        self.prev_btn = self.create_button(self.nav_frame, "◀", self.previous_view)
        self.prev_btn.pack(side=tk.LEFT, padx=20, expand=True)

        self.next_btn = self.create_button(self.nav_frame, "▶", self.next_view)
        self.next_btn.pack(side=tk.RIGHT, padx=20, expand=True)

        # Default view: Month
        self.show_month_view()

    def create_button(self, parent, text, command):
        theme = self.get_current_theme()
        button = tk.Button(parent, text=text, command=command, relief="flat", font=self.font_medium,
                           bg=theme['button_bg'], fg=theme['button_fg'],
                           activebackground="#d9d9d9", bd=0, padx=15, pady=5)
        button.configure(cursor="hand2")
        button.bind("<Enter>", lambda e: button.config(bg="#3367D6"))
        button.bind("<Leave>", lambda e: button.config(bg=theme['button_bg']))
        return button

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme(self.get_current_theme())
        self.refresh_calendar_view()

    def get_current_theme(self):
        return self.dark_theme if self.dark_mode else self.light_theme

    def apply_theme(self, theme):
        self.root.configure(bg=theme["bg"])
        self.top_frame.configure(bg=theme["bg"])
        self.nav_frame.configure(bg=theme["bg"])
        self.calendar_frame.configure(bg=theme["bg"])

        for widget in self.top_frame.winfo_children() + self.nav_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.configure(bg=theme["button_bg"], fg=theme["button_fg"])

        self.refresh_calendar_view()

    def refresh_calendar_view(self):
        if self.current_view == "month":
            self.show_month_view()
        elif self.current_view == "week":
            self.show_week_view()

    def show_week_view(self):
        self.clear_calendar()
        self.current_view = "week"
        week_days = [self.current_date + timedelta(days=i) for i in range(7)]

        week_label = tk.Label(self.calendar_frame, text=f"Week of {week_days[0].strftime('%B %d, %Y')}", font=self.font_large, bg=self.get_current_theme()['bg'], fg=self.get_current_theme()['fg'])
        week_label.pack(pady=10)

        days_frame = tk.Frame(self.calendar_frame, bg=self.get_current_theme()['bg'])
        days_frame.pack(pady=10)

        for day in week_days:
            day_frame = tk.Frame(days_frame, bg=self.get_current_theme()['bg'])
            day_frame.pack(side=tk.LEFT, padx=10, pady=5, expand=True)

            day_label = tk.Label(day_frame, text=day.strftime('%A'), font=self.font_medium, bg=self.get_current_theme()['bg'], fg=self.get_current_theme()['fg'], width=10)
            day_label.pack()

            date_label = tk.Label(day_frame, text=day.strftime('%d'), font=self.font_medium, bg=self.get_current_theme()['bg'], fg=self.get_current_theme()['fg'], width=5)
            date_label.pack()

        days_frame.pack(pady=10)

    def show_month_view(self):
        self.clear_calendar()
        self.current_view = "month"
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)

        month_year_label = tk.Label(self.calendar_frame, text=f"{calendar.month_name[self.current_date.month]} {self.current_date.year}", font=self.font_large, bg=self.get_current_theme()['bg'], fg=self.get_current_theme()['fg'])
        month_year_label.pack(pady=10)

        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        days_frame = tk.Frame(self.calendar_frame, bg=self.get_current_theme()['bg'])
        days_frame.pack(pady=10)

        for col, day in enumerate(days_of_week):
            label = tk.Label(days_frame, text=day, font=self.font_medium, width=5, anchor="center", bg=self.get_current_theme()['bg'], fg=self.get_current_theme()['fg'])
            label.grid(row=0, column=col, padx=5, pady=5)

        for row_index, week in enumerate(cal):
            for col_index, day in enumerate(week):
                if day != 0:  # Only display valid days
                    day_label = tk.Label(days_frame, text=str(day), font=self.font_medium, width=5, anchor="center", bg=self.get_current_theme()['bg'], fg=self.get_current_theme()['fg'], borderwidth=1, relief="solid")
                    day_label.grid(row=row_index + 1, column=col_index, padx=5, pady=5)

        days_frame.pack(pady=10)

    def next_view(self):
        if self.current_view == "week":
            self.current_date += timedelta(days=7)
            self.show_week_view()
        elif self.current_view == "month":
            first_day_next_month = (self.current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
            self.current_date = first_day_next_month
            self.show_month_view()

    def previous_view(self):
        if self.current_view == "week":
            self.current_date -= timedelta(days=7)
            self.show_week_view()
        elif self.current_view == "month":
            last_day_prev_month = (self.current_date.replace(day=1) - timedelta(days=1)).replace(day=1)
            self.current_date = last_day_prev_month
            self.show_month_view()

    def clear_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
