import tkinter as tk
from PIL import Image, ImageTk
from random import randint

MOVE_INCREMENT = 20
snakes_speed = 12
GAME_SPEED = int(round(1000/snakes_speed))


class Snake(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(height = 620, width = 600, highlightthickness = 0, background = 'black')

        self.snakes_positions = [(100,100), (80,100), (60,100)]
        self.foods_position = (120, 120)
        self.score = 0

        self.direction = 'Right'
        self.direction_options = ['Right', 'Left', 'Up', 'Down']
        self.opposites = [{"Right", "Left"}, {"Up", "Down"}]

        self.bind_all("<Key>", self.on_key_press)

        self.load_assets()

        self.create_objects()

        self.after(GAME_SPEED, self.perform_action)


    def load_assets(self):
        try:
            self.snakes_body_image = Image.open('assets\snake.png')
            self.snakes_body = ImageTk.PhotoImage(self.snakes_body_image)

            self.foods_body_image = Image.open('assets\\food.png')
            self.foods_body = ImageTk.PhotoImage(self.foods_body_image)
        except EOFError as e:
            print(e)
            app.destroy()

    def create_objects(self):
        self.create_text(42, 12, text = f'Score: {self.score}', tag = 'score' , fill = '#fff', font = ('TkDefaultFont', 14))

        for position_x, position_y in self.snakes_positions:
            self.create_image(position_x, position_y, image = self.snakes_body, tag = 'snake')

        self.create_image(*self.foods_position, image = self.foods_body, tag = 'food')

        self.create_rectangle(7, 27, 593, 613, outline = '#525d69')

    def move_snake(self):
        x_head_position, y_head_position = self.snakes_positions[0]

        if self.direction == "Left":
            new_snake_position = (x_head_position - MOVE_INCREMENT, y_head_position)
        elif self.direction == "Right":
            new_snake_position = (x_head_position + MOVE_INCREMENT, y_head_position)  
        elif self.direction == "Up":
            new_snake_position = (x_head_position, y_head_position - MOVE_INCREMENT)        
        elif self.direction == "Down":
            new_snake_position = (x_head_position, y_head_position + MOVE_INCREMENT)  
                    
        self.snakes_positions = [new_snake_position] + self.snakes_positions[:-1]

        for segment, position in zip(self.find_withtag('snake'), self.snakes_positions):
            self.coords(segment, position)
        
    def perform_action(self):
        if self.forbidden_collision():
            self.end_game()
            return
        self.food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_action)

    def on_key_press(self, e):
        new_direction = e.keysym
        if new_direction in self.direction_options and {new_direction, self.direction} not in self.opposites:
            self.direction = new_direction
    
    def forbidden_collision(self):
        return (self.snakes_positions[0] in self.snakes_positions[1:] or 
        self.snakes_positions[0][0] in (0, 600) or 
        self.snakes_positions[0][1] in (20, 620))

    
    def food_collision(self):
        global snakes_speed
        if self.foods_position == self.snakes_positions[0]:
            self.score += 1
            self.itemconfig('score', text = f'Score: {self.score}')
            self.create_image(*self.snakes_positions[-1], image = self.snakes_body, tag = 'snake')
            self.snakes_positions.append(self.snakes_positions[-1])
            self.put_food()
        if self.score % 5 == 0:
            snakes_speed += 1

    def put_food(self):
        new_food_x_position = randint(1,29) * MOVE_INCREMENT
        new_food_y_position = randint(3,30) * MOVE_INCREMENT

        if (new_food_x_position, new_food_y_position) not in self.snakes_positions:
            new_foods_position = (new_food_x_position, new_food_y_position)
            for segment, position in zip(self.find_withtag('food'), self.foods_position):
                self.coords(segment, new_foods_position)
                self.foods_position = new_foods_position
        
    def end_game(self):
        self.delete(tk.ALL)
        if self.score < 10:
            summary = "Try harder!"
        elif self.score < 50:
            summary = "Not bad."
        else:
            summary = "Congratulations!"
        self.create_text(
            self.winfo_width()/2,
            self.winfo_height()/2,
            text = f'End of the game! \nYour score is {self.score}. \n{summary}',
            font = ('TkDefaultFont', 24),
            fill = '#fff'
        )


app = tk.Tk()
app.title('Snake')
app.resizable(False, False)

snake = Snake(app)
snake.pack()

app.mainloop()


