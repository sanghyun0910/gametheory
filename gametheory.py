import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class GameTheoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Theory Simulator")

        self.game_type = tk.StringVar(value="Prisoner's Dilemma")
        self.player_choices = [None, None]
        self.current_player = 0
        self.scores = [0, 0]
        self.round = 1

        self.image_label = None
        self.image_dict = {}

        self.load_images()
        self.create_widgets()
        self.update_buttons()

    def load_images(self):
        try:
            self.image_dict["interrogation"] = ImageTk.PhotoImage(Image.open("interrogation.png").resize((300, 180)))
            self.image_dict["forest"] = ImageTk.PhotoImage(Image.open("forest.png").resize((300, 180)))
            self.image_dict["chicken"] = ImageTk.PhotoImage(Image.open("chicken.png").resize((300, 180)))
        except Exception as e:
            print("이미지 로드 실패:", e)

    def create_widgets(self):
        tk.Label(self.root, text="Select Game:").pack()
        tk.OptionMenu(self.root, self.game_type,
                      "Prisoner's Dilemma", "Stag Hunt", "Chicken Game",
                      command=lambda _: self.update_story_and_image()).pack()

        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=5)

        self.story_label = tk.Label(self.root, text="", wraplength=300, justify="left")
        self.story_label.pack(pady=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.choice_buttons = []
        self.choice_labels = ["묵비", "자백"]
        for i in range(2):
            btn = tk.Button(self.button_frame, text=self.choice_labels[i], command=lambda c=i: self.make_choice(c), width=20)
            btn.pack(pady=5)
            self.choice_buttons.append(btn)

        self.status_label = tk.Label(self.root, text="Player 1의 차례입니다.")
        self.status_label.pack(pady=10)

        self.score_label = tk.Label(self.root, text="Scores - Player 1: 0 | Player 2: 0")
        self.score_label.pack(pady=5)

        self.round_label = tk.Label(self.root, text="Round 1")
        self.round_label.pack(pady=5)

        self.reset_button = tk.Button(self.root, text="Next Round", command=self.reset_game)
        self.reset_button.pack()

        self.update_story_and_image()

    def update_buttons(self):
        for btn in self.choice_buttons:
            btn.config(state=tk.NORMAL if self.player_choices[self.current_player] is None else tk.DISABLED)

        game = self.game_type.get()
        if game == "Prisoner's Dilemma":
            self.choice_labels = ["묵비", "자백"]
        elif game == "Stag Hunt":
            self.choice_labels = ["사슴", "토끼"]
        elif game == "Chicken Game":
            self.choice_labels = ["돌진", "피함"]

        for i, label in enumerate(self.choice_labels):
            self.choice_buttons[i].config(text=label)

        self.update_story_and_image()

    def update_story_and_image(self):
        game = self.game_type.get()
        if game == "Prisoner's Dilemma":
            if self.player_choices[0] is None:
                self.story_label.config(text="\n어두운 취조실 안, 형사가 당신을 바라보며 말한다...\n\"너, 이제 말할 때 됐잖아. 묵비할 건가? 자백할 건가?\"")
            elif self.player_choices[1] is None:
                self.story_label.config(text="\n잠시 후, 옆방에서도 누군가 취조를 받고 있다...\n형사는 조용히 웃으며 말한다.\n\"자백하면 넌 집에 갈 수 있어. 하지만 친구는...?\"")
            self.image_label.config(image=self.image_dict["interrogation"])
        elif game == "Stag Hunt":
            self.story_label.config(text="\n깊은 숲속, 두 사냥꾼이 선택의 기로에 섰다...\n사슴을 노릴 것인가, 안전한 토끼를 잡을 것인가?")
            self.image_label.config(image=self.image_dict["forest"])
        elif game == "Chicken Game":
            self.story_label.config(text="\n두 마리의 닭이 마주보고 달리고 있다!\n누가 먼저 피할 것인가? 둘 다 피하지 않으면 대형사고!")
            self.image_label.config(image=self.image_dict["chicken"])

    def make_choice(self, choice):
        if self.player_choices[self.current_player] is None:
            self.player_choices[self.current_player] = choice
            if self.current_player == 0:
                self.current_player = 1
                self.status_label.config(text="Player 2의 차례입니다.")
            else:
                self.evaluate_game()
            self.update_buttons()

    def evaluate_game(self):
        p1, p2 = self.player_choices
        game = self.game_type.get()

        if game == "Prisoner's Dilemma":
            payoff_matrix = [[(-1, -1), (-10, 0)], [(0, -10), (-7, -7)]]
        elif game == "Stag Hunt":
            payoff_matrix = [[(4, 4), (0, 3)], [(3, 0), (3, 3)]]
        elif game == "Chicken Game":
            payoff_matrix = [[(-10, -10), (1, -1)], [(-1, 1), (1, 1)]]

        result = payoff_matrix[p1][p2]
        self.scores[0] += result[0]
        self.scores[1] += result[1]

        if game == "Prisoner's Dilemma":
            choices = ["묵비", "자백"]
            message = (f"Player 1 선택: {choices[p1]}\n"
                       f"Player 2 선택: {choices[p2]}\n\n"
                       f"형량 결과:\nPlayer 1: {-result[0]}년\nPlayer 2: {-result[1]}년")
            ending = "둘 다 입을 다물었군. 정의로운 선택이야." if p1 == 0 and p2 == 0 else \
                     "둘 다 자백했군. 서로를 믿지 못했지..." if p1 == 1 and p2 == 1 else \
                     "한 명만 자백했군. 배신의 대가는 크지."
        elif game == "Stag Hunt":
            choices = ["사슴", "토끼"]
            message = (f"Player 1 선택: {choices[p1]}\n"
                       f"Player 2 선택: {choices[p2]}\n\n"
                       f"보상: Player 1 = {result[0]}, Player 2 = {result[1]}")
            ending = "사슴 사냥 성공! 협력은 위대하다." if p1 == 0 and p2 == 0 else \
                     "서로 다른 길을 택했군. 협력은 실패했어."
        elif game == "Chicken Game":
            choices = ["돌진", "피함"]
            message = (f"Player 1 선택: {choices[p1]}\n"
                       f"Player 2 선택: {choices[p2]}\n\n"
                       f"결과: Player 1 = {result[0]}, Player 2 = {result[1]}")
            ending = "둘 다 돌진! 대형사고 발생!! 💥" if p1 == 0 and p2 == 0 else \
                     "한 명만 피했다! 배짱이 이겼다!" if p1 != p2 else \
                     "둘 다 피했다... 겁쟁이들인가? 🐔"

        messagebox.showinfo("결과", message + "\n\n" + ending)

        self.status_label.config(text="라운드 종료. 'Next Round'를 눌러 계속하세요.")
        self.score_label.config(text=f"Scores - Player 1: {self.scores[0]} | Player 2: {self.scores[1]}")
        self.round += 1
        self.round_label.config(text=f"Round {self.round}")

        if self.round > 5:
            if self.scores[0] > self.scores[1]:
                winner_msg = "\U0001F3C6 Player 1이 최종 승리했습니다!"
            elif self.scores[0] < self.scores[1]:
                winner_msg = "\U0001F3C6 Player 2가 최종 승리했습니다!"
            else:
                winner_msg = "🤝 비겼습니다! 두 사람 모두 멋졌어요."

            messagebox.showinfo("게임 종료", f"5라운드가 끝났습니다!\n\n최종 점수:\n"
                                             f"Player 1: {self.scores[0]}\n"
                                             f"Player 2: {self.scores[1]}\n\n{winner_msg}")

            for btn in self.choice_buttons:
                btn.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.DISABLED)

    def reset_game(self):
        self.player_choices = [None, None]
        self.current_player = 0
        self.status_label.config(text="Player 1의 차례입니다.")
        self.update_buttons()

if __name__ == '__main__':
    root = tk.Tk()
    app = GameTheoryApp(root)
    root.mainloop()