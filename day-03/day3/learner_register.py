

import tkinter as tk
from tkinter import ttk, messagebox


# ----------------------- DATA -----------------------

# Example:
# learners = {
#     "1234567": {"name": "Thabo", "marks": [75, 82, 90]},
# }
learners = {}


# ----------------------- PROCESSING FUNCTIONS -----------------------

def valid_student_number(student_number):
    """Return True if the student number contains exactly 7 digits."""
    return student_number.isdigit() and len(student_number) == 7


def add_learner(student_number, name):
    """Add a learner. Returns (success, message). Does not print."""
    student_number = student_number.strip()
    name = name.strip()

    if not valid_student_number(student_number):
        return False, "Student number must contain exactly 7 digits."

    if not name:
        return False, "Please enter the learner's name."

    if student_number in learners:
        return False, "A learner with this student number already exists."

    learners[student_number] = {"name": name, "marks": []}
    return True, f"Learner {name} was added successfully."


def add_mark(student_number, mark):
    """Add a mark to an existing learner. Returns (success, message)."""
    student_number = student_number.strip()

    if student_number not in learners:
        return False, "Learner not found. Check the student number."

    try:
        mark = float(mark)
    except (TypeError, ValueError):
        return False, "Please enter a valid numeric mark."

    if not 0 <= mark <= 100:
        return False, "Mark must be between 0 and 100."

    learners[student_number]["marks"].append(mark)
    return True, (
        f"Mark {mark:g} added for "
        f"{learners[student_number]['name']}."
    )


def rename_learner(student_number, new_name):
    """Rename an existing learner. Returns (success, message)."""
    student_number = student_number.strip()
    new_name = new_name.strip()

    if student_number not in learners:
        return False, "Learner not found. Check the student number."

    if not new_name:
        return False, "Please enter the new name."

    old_name = learners[student_number]["name"]
    learners[student_number]["name"] = new_name
    return True, f"{old_name} was renamed to {new_name}."


def delete_learner(student_number):
    """Delete an existing learner. Returns (success, message)."""
    student_number = student_number.strip()

    if student_number not in learners:
        return False, "Learner not found. Check the student number."

    name = learners[student_number]["name"]
    del learners[student_number]
    return True, f"Learner {name} was deleted."


def find_by_name(search_text):
    """Return a list of matching learner records. Does not print."""
    search_text = search_text.strip().casefold()

    if not search_text:
        return []

    matches = []
    for student_number, learner in learners.items():
        if search_text in learner["name"].casefold():
            average = learner_average(student_number)
            matches.append(
                (student_number, learner["name"],
                 learner["marks"][:], average)
            )
    return matches


def learner_average(student_number):
    """Return a learner's average, or None if there are no marks."""
    marks = learners[student_number]["marks"]
    if not marks:
        return None
    return sum(marks) / len(marks)


def ranking():
    """
    Return a list of tuples:
    (student_number, name, average, number_of_marks)

    Uses bubble sort to put the highest average first.
    Learners without marks are placed at the bottom.
    Does not print.
    """
    ranked = []

    for student_number, learner in learners.items():
        average = learner_average(student_number)
        ranked.append((
            student_number,
            learner["name"],
            average,
            len(learner["marks"])
        ))

    # Bubble sort: highest average first.
    # None (no marks yet) is treated as lower than any numeric average.
    n = len(ranked)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            left_avg = ranked[j][2]
            right_avg = ranked[j + 1][2]

            left_value = left_avg if left_avg is not None else float("-inf")
            right_value = right_avg if right_avg is not None else float("-inf")

            if left_value < right_value:
                ranked[j], ranked[j + 1] = ranked[j + 1], ranked[j]
                swapped = True

        if not swapped:
            break

    return ranked


# ----------------------- GUI -----------------------

class LearnerRegisterApp:
    MENU_OPTIONS = [
        "1. Add learner",
        "2. Add mark",
        "3. Rename learner",
        "4. Delete learner",
        "5. Find by name",
        "6. Print ranking",
        "7. Exit",
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Learner Register System")
        self.root.geometry("1000x680")
        self.root.minsize(850, 580)
        self.root.configure(bg="#eef2f7")

        self._build_interface()
        self.refresh_table()

    def _build_interface(self):
        header = tk.Frame(self.root, bg="#173b70", padx=18, pady=15)
        header.pack(fill="x")

        tk.Label(
            header,
            text="LEARNER REGISTER SYSTEM",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#173b70",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Register learners, manage marks, search and view rankings",
            font=("Arial", 10),
            fg="#e1eafa",
            bg="#173b70",
        ).pack(anchor="w", pady=(4, 0))

        main = tk.Frame(self.root, bg="#eef2f7", padx=15, pady=12)
        main.pack(fill="both", expand=True)

        # Menu and input area
        input_frame = ttk.LabelFrame(main, text="Menu and learner details", padding=12)
        input_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(input_frame, text="Menu option:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.menu_var = tk.StringVar(value=self.MENU_OPTIONS[0])
        self.menu_box = ttk.Combobox(
            input_frame,
            textvariable=self.menu_var,
            values=self.MENU_OPTIONS,
            state="readonly",
            width=27,
        )
        self.menu_box.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.menu_box.bind("<<ComboboxSelected>>", self.on_menu_change)

        ttk.Label(input_frame, text="Student number (7 digits):").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.student_entry = ttk.Entry(input_frame, width=30)
        self.student_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(input_frame, text="Learner name / new name:").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        self.name_entry = ttk.Entry(input_frame, width=30)
        self.name_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(input_frame, text="Mark (0 to 100):").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        self.mark_entry = ttk.Entry(input_frame, width=30)
        self.mark_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(input_frame, text="Search text:").grid(
            row=4, column=0, sticky="w", padx=5, pady=5
        )
        self.search_entry = ttk.Entry(input_frame, width=30)
        self.search_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        input_frame.columnconfigure(1, weight=1)

        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=0, column=2, rowspan=5, padx=18, sticky="ns")

        ttk.Button(
            button_frame, text="Perform selected option",
            command=self.perform_action
        ).pack(fill="x", pady=(4, 8))

        ttk.Button(
            button_frame, text="Clear input fields",
            command=self.clear_inputs
        ).pack(fill="x", pady=4)

        ttk.Button(
            button_frame, text="Refresh register",
            command=self.refresh_table
        ).pack(fill="x", pady=4)

        # Status/output message
        self.status_var = tk.StringVar(value="Select a menu option to begin.")
        self.status_label = tk.Label(
            main,
            textvariable=self.status_var,
            anchor="w",
            justify="left",
            bg="#e0eaf7",
            fg="#173b70",
            padx=10,
            pady=9,
            font=("Arial", 10, "bold"),
        )
        self.status_label.pack(fill="x", pady=(0, 10))

        # Register table
        table_frame = ttk.LabelFrame(main, text="Learner register / ranking", padding=8)
        table_frame.pack(fill="both", expand=True)

        columns = ("student_number", "name", "marks", "average")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=12
        )

        self.tree.heading("student_number", text="Student Number")
        self.tree.heading("name", text="Learner Name")
        self.tree.heading("marks", text="Marks")
        self.tree.heading("average", text="Average")

        self.tree.column("student_number", width=145, anchor="center")
        self.tree.column("name", width=240)
        self.tree.column("marks", width=300)
        self.tree.column("average", width=110, anchor="center")

        vertical_scroll = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        horizontal_scroll = ttk.Scrollbar(
            table_frame, orient="horizontal", command=self.tree.xview
        )
        self.tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set,
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical_scroll.grid(row=0, column=1, sticky="ns")
        horizontal_scroll.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        footer = tk.Label(
            main,
            text="Tip: Add a learner before adding marks. Ranking uses each learner's average.",
            bg="#eef2f7",
            fg="#4b5563",
            font=("Arial", 9),
        )
        footer.pack(anchor="w", pady=(8, 0))

    def on_menu_change(self, _event=None):
        option = self.menu_var.get()
        if option.startswith("1."):
            self.status_var.set("Enter a unique 7-digit student number and learner name.")
        elif option.startswith("2."):
            self.status_var.set("Enter the learner's student number and a mark from 0 to 100.")
        elif option.startswith("3."):
            self.status_var.set("Enter the learner's student number and the new name.")
        elif option.startswith("4."):
            self.status_var.set("Enter the student number of the learner to delete.")
        elif option.startswith("5."):
            self.status_var.set("Enter all or part of a learner's name in Search text.")
        elif option.startswith("6."):
            self.status_var.set("The register will be sorted by average mark, highest first.")
        else:
            self.status_var.set("Choose Perform selected option to close the application.")

    def get_student_number(self):
        return self.student_entry.get().strip()

    def get_name(self):
        return self.name_entry.get().strip()

    def perform_action(self):
        option = self.menu_var.get()

        if option.startswith("1."):
            success, message = add_learner(
                self.get_student_number(), self.get_name()
            )
            self.show_message(message, success)
            if success:
                self.refresh_table()

        elif option.startswith("2."):
            success, message = add_mark(
                self.get_student_number(), self.mark_entry.get().strip()
            )
            self.show_message(message, success)
            if success:
                self.refresh_table()

        elif option.startswith("3."):
            success, message = rename_learner(
                self.get_student_number(), self.get_name()
            )
            self.show_message(message, success)
            if success:
                self.refresh_table()

        elif option.startswith("4."):
            student_number = self.get_student_number()
            if student_number not in learners:
                self.show_message("Learner not found. Check the student number.", False)
                return

            learner_name = learners[student_number]["name"]
            confirm = messagebox.askyesno(
                "Confirm deletion",
                f"Are you sure you want to delete {learner_name} ({student_number})?"
            )
            if confirm:
                success, message = delete_learner(student_number)
                self.show_message(message, success)
                if success:
                    self.refresh_table()

        elif option.startswith("5."):
            search_text = self.search_entry.get().strip()
            if not search_text:
                self.show_message("Enter text in the Search text field.", False)
                return

            matches = find_by_name(search_text)
            self.refresh_table(matches)
            if matches:
                self.show_message(
                    f"{len(matches)} matching learner(s) found.", True
                )
            else:
                self.show_message("No learners match that search text.", False)

        elif option.startswith("6."):
            ranked = ranking()
            self.refresh_table(ranked, already_ranked=True)
            self.show_message(
                f"Ranking displayed for {len(ranked)} learner(s), highest average first.",
                True
            )

        elif option.startswith("7."):
            if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                self.root.destroy()

    def show_message(self, message, success):
        self.status_var.set(message)
        self.status_label.configure(
            bg="#dcfce7" if success else "#fee2e2",
            fg="#166534" if success else "#991b1b",
        )

    def clear_inputs(self):
        for entry in (
            self.student_entry, self.name_entry,
            self.mark_entry, self.search_entry
        ):
            entry.delete(0, tk.END)
        self.status_var.set("Input fields cleared.")
        self.status_label.configure(bg="#e0eaf7", fg="#173b70")

    def refresh_table(self, records=None, already_ranked=False):
        """Refresh the table. Normal view uses registration order."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        if records is None:
            records = []
            for student_number, learner in learners.items():
                records.append((
                    student_number,
                    learner["name"],
                    learner["marks"][:],
                    learner_average(student_number),
                ))
        elif already_ranked:
            # ranking() returns (number, name, average, number_of_marks)
            converted = []
            for student_number, name, average, _count in records:
                converted.append((
                    student_number,
                    name,
                    learners[student_number]["marks"][:],
                    average,
                ))
            records = converted

        for record in records:
            student_number, name, marks, average = record
            marks_text = ", ".join(f"{m:g}" for m in marks) if marks else "No marks"
            average_text = f"{average:.2f}" if average is not None else "N/A"
            self.tree.insert(
                "", tk.END,
                values=(student_number, name, marks_text, average_text)
            )


def main():
    root = tk.Tk()
    app = LearnerRegisterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
