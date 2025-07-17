import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from datetime import datetime
import re
from pathlib import Path


class ModernAttendanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Calculator")
        self.root.geometry("1200x800")

        # Modern color scheme
        self.colors = {
            'bg': '#f0f0f0',
            'primary': '#2563eb',
            'secondary': '#64748b',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'card_bg': '#ffffff',
            'text': '#1f2937',
            'text_secondary': '#6b7280'
        }

        # Configure root
        self.root.configure(bg=self.colors['bg'])

        # Sample data (you would replace this with your actual data)
        self.course_details = {
            'APTI401': {'course_name': 'Aptitude-IV', 'attended': 9, 'occurred': 14, 'percentage': 64.29},
            'BUPRP': {'course_name': 'Preparatory Paper', 'attended': 1, 'occurred': 1, 'percentage': 100.0},
            'SBC': {'course_name': 'Soft Skill Boot Camp', 'attended': 25, 'occurred': 29, 'percentage': 86.21},
            'BCA47111(T)': {'course_name': 'Design and Analysis of Algorithm', 'attended': 23, 'occurred': 28, 'percentage': 82.14},
            'BCA47111(P)': {'course_name': 'Design and Analysis of Algorithm', 'attended': 44, 'occurred': 59, 'percentage': 74.58},
            'BCA49112': {'course_name': 'PHP and MySQL Lab', 'attended': 40, 'occurred': 53, 'percentage': 75.47},
            'BCA47113(T)': {'course_name': 'Full-Stack Development-I', 'attended': 20, 'occurred': 30, 'percentage': 66.67},
            'BCA47113(P)': {'course_name': 'Full-Stack Development-I', 'attended': 45, 'occurred': 60, 'percentage': 75.0},
            'BCA40201': {'course_name': 'Sustainability in Indian Knowledge System', 'attended': 48, 'occurred': 60, 'percentage': 80.0},
            'BCA40202': {'course_name': 'Computer Network', 'attended': 50, 'occurred': 59, 'percentage': 84.75}
        }

        self.routine_data = {
            'MON': ['', '', '', '', '', '', '', '', '', '', ''],
            'TUE': ['', 'BCA40202', 'BCA40202', '', 'BCA49112', '', '', '', '', '', ''],
            'WED': ['', '', 'SBC', '', 'BCA40201', 'BCA40201', '', 'BCA47113(P)', 'BCA47113(P)', 'BCA47113(P)', ''],
            'THU': ['', '', 'SBC', '', 'BCA40202', 'BCA47113(P)', '', 'BCA47111(P)', 'BCA47111(P)', 'BCA47111(P)', ''],
            'FRI': ['', '', 'BCA40201', '', 'BCA47111(T)', '', '', 'BCA49112', 'BCA49112', 'BCA49112', ''],
            'SAT': ['', 'BCA40201', 'BCA40202', 'BCA47111(P)', '', 'BCA47111(T)', 'BCA47113(T)', 'BCA47113(T)', 'APTI401', '', '']
        }

        self.time_slots = ['8:00-9:00', '9:00-10:00', '10:00-11:00', '11:00-12:00',
                           '12:00-1:00', '1:00-2:00', '2:00-3:00', '3:00-4:00',
                           '4:00-5:00', '5:00-6:00', '6:00-7:00']

        self.days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

        self.setup_ui()
        # self.update_tables()

    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = tk.Label(main_frame, text="Attendance Calculator",
                               font=('Arial', 24, 'bold'),
                               bg=self.colors['bg'],
                               fg=self.colors['primary'])
        title_label.pack(pady=(0, 20))

        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Configure notebook style
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 10])

        # Create tabs
        self.create_attendance_tab()
        # self.create_routine_tab()
        # self.create_calculator_tab()

    def create_attendance_tab(self):
        # Attendance tab
        attendance_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(attendance_frame, text="Current Attendance")

        # Header
        header_frame = tk.Frame(attendance_frame, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(header_frame, text="Current Attendance Status",
                 font=('Arial', 12, 'bold'),
                 pady=10,
                 bg=self.colors['bg'],
                 fg=self.colors['text']).pack()

        # Refresh button
        # refresh_btn = tk.Button(header_frame, text="Refresh",
        #                         bg=self.colors['primary'],
        #                         fg='white',
        #                         font=('Arial', 10, 'bold'),
        #                         padx=20, pady=5,
        #                         relief=tk.FLAT)
        # refresh_btn.pack(side=tk.RIGHT)

        # Attendance table frame
        table_frame = tk.Frame(
            attendance_frame, bg=self.colors['card_bg'], relief=tk.RAISED, bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create treeview for attendance table
        columns = ('Course Code', 'Course Name',
                   'Attended', 'Occurred', 'Percentage')
        self.attendance_tree = ttk.Treeview(
            table_frame, columns=columns, show='headings', height=12)

        # Configure column headings and widths
        for col in columns:
            self.attendance_tree.heading(col, text=col)
            if col == 'Course Code':
                self.attendance_tree.column(col, width=120)
            elif col == 'Course Name':
                self.attendance_tree.column(col, width=350)
            else:
                self.attendance_tree.column(col, width=100)

        # Scrollbar for attendance table
        attendance_scrollbar = ttk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscrollcommand=attendance_scrollbar.set)

        # Pack attendance table and scrollbar
        self.attendance_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        attendance_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Summary frame
        summary_frame = tk.Frame(
            attendance_frame, bg=self.colors['card_bg'], relief=tk.RAISED, bd=1)
        summary_frame.pack(fill=tk.X, padx=10, pady=10)

        self.summary_label = tk.Label(summary_frame, text="",
                                      font=('Arial', 10, 'bold'),
                                      bg=self.colors['card_bg'],
                                      fg=self.colors['text'])
        self.summary_label.pack(pady=20)

    # def create_routine_tab(self):
    #     # Routine tab
    #     routine_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
    #     self.notebook.add(routine_frame, text="Class Routine")

    #     # Header
    #     header_frame = tk.Frame(routine_frame, bg=self.colors['bg'])
    #     header_frame.pack(fill=tk.X, pady=(0, 20))

    #     tk.Label(header_frame, text="Class Routine",
    #              font=('Arial', 12, 'bold'),
    #              pady=10,
    #              bg=self.colors['bg'],
    #              fg=self.colors['text']).pack()

    #     # Routine table frame
    #     routine_table_frame = tk.Frame(
    #         routine_frame, bg=self.colors['card_bg'], relief=tk.RAISED, bd=1)
    #     routine_table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    #     # Create treeview for routine table
    #     routine_columns = ['Days'] + self.time_slots
    #     self.routine_tree = ttk.Treeview(
    #         routine_table_frame, columns=routine_columns, show='headings', height=8)

    #     # Configure routine column headings and widths
    #     for col in routine_columns:
    #         self.routine_tree.heading(col, text=col)
    #         if col == 'Days':
    #             self.routine_tree.column(col, width=80)
    #         else:
    #             self.routine_tree.column(col, width=120)

    #     # Horizontal scrollbar for routine table
    #     routine_h_scrollbar = ttk.Scrollbar(
    #         routine_table_frame, orient=tk.HORIZONTAL, command=self.routine_tree.xview)
    #     self.routine_tree.configure(xscrollcommand=routine_h_scrollbar.set)

    #     # Pack routine table and scrollbar
    #     self.routine_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    #     routine_h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    # def create_calculator_tab(self):
    #     # Calculator tab
    #     calc_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
    #     self.notebook.add(calc_frame, text="Calculate Attendance")

    #     # Header
    #     header_frame = tk.Frame(calc_frame, bg=self.colors['bg'])
    #     header_frame.pack(fill=tk.X, pady=(0, 30))

    #     tk.Label(header_frame, text="Attendance Calculator",
    #              font=('Arial', 12, 'bold'),
    #              pady=10,
    #              bg=self.colors['bg'],
    #              fg=self.colors['text']).pack()

    #     # Input form frame
    #     form_frame = tk.Frame(
    #         calc_frame, bg=self.colors['card_bg'], relief=tk.RAISED, bd=1)
    #     form_frame.pack(fill=tk.X, padx=50, pady=20)

    #     # Form content
    #     form_content = tk.Frame(form_frame, bg=self.colors['card_bg'])
    #     form_content.pack(padx=40, pady=40)

    #     # Day selection
    #     day_frame = tk.Frame(form_content, bg=self.colors['card_bg'])
    #     day_frame.pack(fill=tk.X, pady=(0, 20))

    #     tk.Label(day_frame, text="Select Day:",
    #              font=('Arial', 10, 'bold'),
    #              bg=self.colors['card_bg'],
    #              fg=self.colors['text']).pack(side=tk.LEFT, padx=(0, 20))

    #     self.day_var = tk.StringVar()
    #     day_combobox = ttk.Combobox(day_frame, textvariable=self.day_var, values=self.days,
    #                                 state='readonly', width=15, font=('Arial', 12))
    #     day_combobox.pack(side=tk.LEFT)
    #     day_combobox.bind('<<ComboboxSelected>>', self.on_day_selected)

    #     # Attendance marking options
    #     option_frame = tk.Frame(form_content, bg=self.colors['card_bg'])
    #     option_frame.pack(fill=tk.X, pady=(0, 20))

    #     tk.Label(option_frame, text="Attendance Option:",
    #              font=('Arial', 10, 'bold'),
    #              bg=self.colors['card_bg'],
    #              fg=self.colors['text']).pack(side=tk.LEFT, padx=(0, 20))

    #     self.attendance_option = tk.StringVar(value="custom")

    #     option_buttons_frame = tk.Frame(
    #         option_frame, bg=self.colors['card_bg'])
    #     option_buttons_frame.pack(side=tk.LEFT)

    #     tk.Radiobutton(option_buttons_frame, text="All Present", variable=self.attendance_option,
    #                    value="present", bg=self.colors['card_bg'], font=('Arial', 11),
    #                    command=self.on_option_changed).pack(side=tk.LEFT, padx=(0, 20))

    #     tk.Radiobutton(option_buttons_frame, text="All Absent", variable=self.attendance_option,
    #                    value="absent", bg=self.colors['card_bg'], font=('Arial', 11),
    #                    command=self.on_option_changed).pack(side=tk.LEFT, padx=(0, 20))

    #     tk.Radiobutton(option_buttons_frame, text="Custom", variable=self.attendance_option,
    #                    value="custom", bg=self.colors['card_bg'], font=('Arial', 11),
    #                    command=self.on_option_changed).pack(side=tk.LEFT)

    #     # Classes for selected day
    #     self.classes_frame = tk.Frame(form_content, bg=self.colors['card_bg'])
    #     self.classes_frame.pack(fill=tk.X, pady=(0, 20))

    #     self.class_vars = {}

    #     # Calculate button
    #     calc_button = tk.Button(form_content, text="Calculate Attendance",
    #                             command=self.calculate_attendance,
    #                             bg=self.colors['success'],
    #                             fg='white',
    #                             font=('Arial', 12, 'bold'),
    #                             padx=30, pady=10,
    #                             relief=tk.FLAT)
    #     calc_button.pack(pady=20)

    #     # Results frame
    #     self.results_frame = tk.Frame(
    #         calc_frame, bg=self.colors['card_bg'], relief=tk.RAISED, bd=1)
    #     self.results_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

    #     # Results header
    #     results_header = tk.Frame(
    #         self.results_frame, bg=self.colors['card_bg'])
    #     results_header.pack(fill=tk.X, pady=(20, 10))

    #     tk.Label(results_header, text="Before and After Comparison",
    #              font=('Arial', 16, 'bold'),
    #              bg=self.colors['card_bg'],
    #              fg=self.colors['text']).pack()

    #     # Results content
    #     results_content = tk.Frame(
    #         self.results_frame, bg=self.colors['card_bg'])
    #     results_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    #     # Before and After frames
    #     before_frame = tk.Frame(results_content, bg=self.colors['card_bg'])
    #     before_frame.pack(side=tk.LEFT, fill=tk.BOTH,
    #                       expand=True, padx=(0, 10))

    #     after_frame = tk.Frame(results_content, bg=self.colors['card_bg'])
    #     after_frame.pack(side=tk.RIGHT, fill=tk.BOTH,
    #                      expand=True, padx=(10, 0))

    #     # Before label
    #     tk.Label(before_frame, text="Before",
    #              font=('Arial', 10, 'bold'),
    #              bg=self.colors['card_bg'],
    #              fg=self.colors['text']).pack(pady=(0, 10))

    #     self.before_label = tk.Label(before_frame, text="",
    #                                  font=('Arial', 12),
    #                                  bg=self.colors['card_bg'],
    #                                  fg=self.colors['text'],
    #                                  justify=tk.LEFT)
    #     self.before_label.pack()

    #     # After label
    #     tk.Label(after_frame, text="After",
    #              font=('Arial', 10, 'bold'),
    #              bg=self.colors['card_bg'],
    #              fg=self.colors['text']).pack(pady=(0, 10))

    #     self.after_label = tk.Label(after_frame, text="",
    #                                 font=('Arial', 12),
    #                                 bg=self.colors['card_bg'],
    #                                 fg=self.colors['text'],
    #                                 justify=tk.LEFT)
    #     self.after_label.pack()

    # def update_tables(self):
    #     # Clear existing items
    #     for item in self.attendance_tree.get_children():
    #         self.attendance_tree.delete(item)

    #     for item in self.routine_tree.get_children():
    #         self.routine_tree.delete(item)

    #     # Populate attendance table
    #     for course_code, details in self.course_details.items():
    #         percentage_color = self.get_percentage_color(details['percentage'])
    #         self.attendance_tree.insert('', 'end', values=(
    #             course_code,
    #             details['course_name'],
    #             details['attended'],
    #             details['occurred'],
    #             f"{details['percentage']:.2f}%"
    #         ))

    #     # Populate routine table
    #     for day in self.days:
    #         row_values = [day] + \
    #             [cls if cls else '' for cls in self.routine_data[day]]
    #         self.routine_tree.insert('', 'end', values=row_values)

    #     # Update summary
    #     total_attended = sum(details['attended']
    #                          for details in self.course_details.values())
    #     total_occurred = sum(details['occurred']
    #                          for details in self.course_details.values())
    #     overall_percentage = (
    #         total_attended / total_occurred * 100) if total_occurred > 0 else 0

    #     self.summary_label.config(
    #         text=f"Overall Attendance: {total_attended}/{total_occurred} ({overall_percentage:.2f}%)")

    # def get_percentage_color(self, percentage):
    #     if percentage >= 80:
    #         return self.colors['success']
    #     elif percentage >= 75:
    #         return self.colors['warning']
    #     else:
    #         return self.colors['danger']

    # def on_day_selected(self, event):
    #     selected_day = self.day_var.get()
    #     if selected_day:
    #         self.update_classes_for_day(selected_day)

    # def update_classes_for_day(self, day):
    #     # Clear existing class checkboxes
    #     for widget in self.classes_frame.winfo_children():
    #         widget.destroy()

    #     self.class_vars = {}

    #     # Get classes for the selected day
    #     day_classes = [cls for cls in self.routine_data[day] if cls]

    #     if not day_classes:
    #         tk.Label(self.classes_frame, text="No classes scheduled for this day",
    #                  font=('Arial', 12),
    #                  bg=self.colors['card_bg'],
    #                  fg=self.colors['text_secondary']).pack(pady=10)
    #         return

    #     tk.Label(self.classes_frame, text=f"Classes for {day}:",
    #              font=('Arial', 12, 'bold'),
    #              bg=self.colors['card_bg'],
    #              fg=self.colors['text']).pack(pady=(0, 10))

    #     # Create checkboxes for each class
    #     for cls in day_classes:
    #         if cls in self.course_details:
    #             self.class_vars[cls] = tk.BooleanVar(value=True)

    #             class_frame = tk.Frame(
    #                 self.classes_frame, bg=self.colors['card_bg'])
    #             class_frame.pack(fill=tk.X, pady=2)

    #             cb = tk.Checkbutton(class_frame,
    #                                 text=f"{cls} - {self.course_details[cls]['course_name']}",
    #                                 variable=self.class_vars[cls],
    #                                 bg=self.colors['card_bg'],
    #                                 font=('Arial', 11))
    #             cb.pack(side=tk.LEFT)

    #     self.on_option_changed()

    # def on_option_changed(self):
    #     option = self.attendance_option.get()

    #     if option == "present":
    #         for var in self.class_vars.values():
    #             var.set(True)
    #     elif option == "absent":
    #         for var in self.class_vars.values():
    #             var.set(False)
    #     # For custom, leave checkboxes as they are

    # def calculate_attendance(self):
    #     selected_day = self.day_var.get()
    #     if not selected_day:
    #         messagebox.showwarning("Warning", "Please select a day first!")
    #         return

    #     if not self.class_vars:
    #         messagebox.showwarning(
    #             "Warning", "No classes available for the selected day!")
    #         return

    #     # Store original values for "Before" display
    #     original_total_attended = sum(
    #         details['attended'] for details in self.course_details.values())
    #     original_total_occurred = sum(
    #         details['occurred'] for details in self.course_details.values())
    #     original_percentage = (
    #         original_total_attended / original_total_occurred * 100) if original_total_occurred > 0 else 0

    #     # Apply attendance changes
    #     for course_code, var in self.class_vars.items():
    #         if course_code in self.course_details:
    #             self.course_details[course_code]['occurred'] += 1
    #             if var.get():  # If present
    #                 self.course_details[course_code]['attended'] += 1

    #             # Recalculate percentage
    #             attended = self.course_details[course_code]['attended']
    #             occurred = self.course_details[course_code]['occurred']
    #             self.course_details[course_code]['percentage'] = (
    #                 attended / occurred * 100) if occurred > 0 else 0

    #     # Calculate new totals for "After" display
    #     new_total_attended = sum(details['attended']
    #                              for details in self.course_details.values())
    #     new_total_occurred = sum(details['occurred']
    #                              for details in self.course_details.values())
    #     new_percentage = (new_total_attended / new_total_occurred *
    #                       100) if new_total_occurred > 0 else 0

    #     # Update displays
    #     self.before_label.config(
    #         text=f"Total: {original_total_attended}/{original_total_occurred}\nPercentage: {original_percentage:.2f}%")
    #     self.after_label.config(
    #         text=f"Total: {new_total_attended}/{new_total_occurred}\nPercentage: {new_percentage:.2f}%")

    #     # Update tables
    #     self.update_tables()

    #     # Show success message
    #     messagebox.showinfo(
    #         "Success", f"Attendance calculated for {selected_day}!")


def main():
    root = tk.Tk()
    app = ModernAttendanceGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
