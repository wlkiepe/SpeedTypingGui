# import everything I will need
from tkinter import *

# Originally I was going to have the GUI make a messagebox to tell the user their results, but I found the user
# experience to be too easy to close the window box before seeing the score, so I commented it out. I chose not to
# delete the line because I am still not in love with the user experience and may circle back to this idea later
# from tkinter import messagebox

import random
import pandas

# I have a csv with ~1000 of the most common words in the English language to pull the words from
word_list = pandas.read_csv('1000-words-csv.csv')

# set up my window
background = '#DDDDDD'
window = Tk()
window.title("Typing Timer")
window.wm_minsize(width=1200, height=400)
window.config(bg=background)

# Make an error message if the user makes a typo
error_msg = Label(text="You made a typo \nplease try again.", bg=background, fg='#820000',
                  font=('Arial', 14, "bold"))

# Make a countdown and score
timer = None
game_on = False
score = 0


def count_down(seconds):
    second = seconds
    global game_on
    # This first if portion is just for aesthetics, makes the time a two-digit number like 06 instead of just 6.
    if seconds < 10:
        second = f"0{seconds}"
    canvas.itemconfig(timer_text, text=f"Time: \n   {second}")
    if seconds > 0:
        global timer
        timer = window.after(1000, count_down, seconds - 1)
    else:
        game_on = False


# Create a function to start the timer
def start_timer():
    # Destroy the button so that it doesn't get in the way, turn the game on, and start the count_down at 60 seconds
    button.destroy()
    global game_on
    game_on = True
    count_down(60)
    # run the entry_box function from the next lines of code to set up the entry_box
    entry_box()
    # Make a label f"Type the word {string}"


# Make a function that will create an entry box for the user
def entry_box():
    global background
    global score
    # The random integer will help pull a random word from the csv file. I start at 10 because the first few words
    # are mostly two or three-letter words like it, at, on, the
    n = random.randint(10, 997)
    # Uses the random number to pull an element from the column starting with 'the'
    word = word_list['the'][n]
    entry = Entry(width=20, font=('Arial', 16, "bold"))
    # Make the GUI start out in the entry box so that the user can start typing without having to click on it each word
    entry.focus()
    # Make a label telling the user what word to type
    quiz = Label(text=f"Type: {word}", font=('Arial', 32, "bold"), bg=background)

    # Create a function in entry_box to either send an error message if there was a typo. If the user types the word
    # correctly then it will give them a new word and update their score
    def new_word():
        global error_msg
        check_answer = entry.get()
        if game_on:
            if check_answer.lower() != word:
                error_msg.grid(column=1, row=4, padx=50)
                entry.delete(0, END)
            else:
                global score
                score += 1
                scoreboard.config(text=f"Score: {score}")
                quiz.config(text=f"Type: {word}")
                entry.delete(0, END)
                error_msg.grid_remove()
                entry.destroy()
                quiz.destroy()
                entry_box()
        # If the timer has run up, then when the user presses enter it will tell them their score. I would prefer to
        # make this happen automatically when the time runs up, but the methods I tried were either buggy or led to
        # a bad user experience, so this is what I settled on.
        else:
            entry.destroy()
            error_msg.destroy()
            quiz.config(text=f"Time's Up! \nYou typed {score} words \nper minute.", fg='#820000')

    # Create a button to submit responses that is invisible and will respond to the user pressing enter.
    submit = Button(width=40, text='Submit', command=new_word)
    window.bind('<Return>', lambda event: new_word())
    quiz.grid(column=1, row=1, padx=50)
    entry.grid(column=1, row=2, padx=50)
    submit.grid(column=1, row=3, padx=50)
    submit.grid_forget()


# Create the canvas and the necessary pieces to it.
canvas = Canvas(width=300, height=150, bg=background, highlightthickness=0)
timer_text = canvas.create_text(160, 100, text='Time: \n   60', font=('Arial', 32, "bold"))

button = Button(width=60, text='Start', command=start_timer)

title = Label(text='How fast can you type?', bg=background, font=('Arial', 32, "bold"), padx=50, pady=50)
scoreboard = Label(text=f'Score: {score}', bg=background, font=('Arial', 32, "bold"), padx=50, pady=50)

title.grid(column=0, row=0)
scoreboard.grid(column=0, row=1, padx=50)
canvas.grid(column=1, row=0)
button.grid(column=1, row=1, padx=50)

window.mainloop()

# Things I would like to update for the user experience:
# 1. Make it so that the quiz label and timer text don't change sizes as the length of the words change. When I tried to
# fix that it often made the column more spread out than I like which was aesthetically unappealing.
# 2. Figure out a way to make it so that the program will automatically tell the user their score when the time runs
# out. This program works well if you know you need to press 'enter' one last time when the timer reaches 0, but
# otherwise it may not be super intuitive. 
# 3. Make a prettier user interface. I like that the color and font choices are easy to read, but I would like it to
# look prettier.
