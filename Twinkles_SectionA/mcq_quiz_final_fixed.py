import tkinter as tk
from tkinter import messagebox

class QuizData:
    def __init__(self):
        self.questions = [
            "What is the capital of ITALY?",
            "What is the full form of AI?",
            "Which language is best for AI?",
            "What is machine learning?",
            "Which of the following is an AI application?",
            "Who is considered the father of AI?"
        ]
        self.options = [
            ["Rome", "London", "Paris", "None"],
            ["Artificial Intelligence", "Automatic Interface", "Auto Internet", "None"],
            ["Python", "HTML", "CSS", "PHP"],
            ["Learning to code", "Learning machines", "Giving ability to learn", "None"],
            ["Google Maps", "MS Word", "Paint", "Calculator"],
            ["John McCarthy", "Alan Turing", "Bill Gates", "Elon Musk"]
        ]
        self.answers = [
            "Rome",
            "Artificial Intelligence",
            "Python",
            "Giving ability to learn",
            "Google Maps",
            "John McCarthy"
        ]

class QuizLogic:
    def __init__(self, quiz_data):
        self.quiz_data = quiz_data
        self.index = 0
        self.score = 0

    def get_current_question(self):
        return self.quiz_data.questions[self.index]

    def get_current_options(self):
        return self.quiz_data.options[self.index]

    def check_answer(self, selected):
        correct = self.quiz_data.answers[self.index]
        if selected == correct:
            self.score += 1
            return True, correct
        else:
            return False, correct

    def next_question(self):
        self.index += 1
        return self.index < len(self.quiz_data.questions)

    def get_score(self):
        return self.score, len(self.quiz_data.questions)

class QuizGUI:
    def __init__(self, quiz_logic):
        self.quiz_logic = quiz_logic
        self.window = tk.Tk()
        self.window.title("AI Quiz Project")
        self.window.geometry("550x400")

        self.var = tk.StringVar()
        self.question_label = tk.Label(self.window, text="", font=("Arial", 16), wraplength=500)
        self.question_label.pack(pady=20)

        self.options_buttons = []
        for i in range(4):
            btn = tk.Radiobutton(self.window, text="", variable=self.var, font=("Arial", 14), wraplength=500)
            btn.pack(anchor="w", padx=50)
            self.options_buttons.append(btn)

        self.result_label = tk.Label(self.window, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.next_button = tk.Button(self.window, text="Next", command=self.process_next, font=("Arial", 14))
        self.next_button.pack(pady=10)

        self.load_question()
        self.window.mainloop()

    def load_question(self):
        question = self.quiz_logic.get_current_question()
        options = self.quiz_logic.get_current_options()
        self.question_label.config(text=question)
        self.var.set(None)
        for i, opt in enumerate(options):
            self.options_buttons[i].config(text=opt, value=opt)

    def process_next(self):
        selected = self.var.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select an option")
            return

        is_correct, correct_ans = self.quiz_logic.check_answer(selected)
        if is_correct:
            self.result_label.config(text="✅ Correct", fg="green")
        else:
            self.result_label.config(text=f"❌ Wrong (Correct: {correct_ans})", fg="red")

        if self.quiz_logic.next_question():
            self.window.after(1000, self.load_question)
            self.window.after(1000, lambda: self.result_label.config(text=""))
        else:
            self.show_result_screen()

    def show_result_screen(self):
        score, total = self.quiz_logic.get_score()

        self.window.destroy()

        result_win = tk.Tk()
        result_win.title("Quiz Result")
        result_win.geometry("500x300")

        tk.Label(result_win, text=f"🎯 Final Score: {score} out of {total}", font=("Arial", 18)).pack(pady=20)

        if score < total * 0.5:
            feedback = """Result is below average.
🧠 Tips to improve:
- Study AI basics from online tutorials
- Try solving practice MCQs
- Discuss answers with friends"""
        elif score < total:
            feedback = """Almost there!
✅ Keep practicing and revise incorrect topics."""
        else:
            feedback = "🎉 Excellent! You have strong basic knowledge in AI."

        tk.Label(result_win, text=feedback, font=("Arial", 14), wraplength=480, justify="left").pack(pady=10)

        tk.Button(result_win, text="Exit", command=result_win.destroy, font=("Arial", 14)).pack(pady=10)

        result_win.mainloop()

if __name__ == "__main__":
    quiz_data = QuizData()
    quiz_logic = QuizLogic(quiz_data)
    QuizGUI(quiz_logic)
