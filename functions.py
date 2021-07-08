from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5 import QtCore
from urllib.request import urlopen
import json
import pandas as pd
import random

#https://opentdb.com/api.php?amount=50&category=9&difficulty=medium&type=multiple
with urlopen("https://opentdb.com/api.php?amount=50&category=9&difficulty=easy&type=multiple") as webpage:
    data = json.loads(webpage.read().decode())
    df = pd.DataFrame(data["results"])

#preload vprasanj
def preload_data(indx):
    question = df["question"][indx]
    correct = df["correct_answer"][indx]
    wrong = df["incorrect_answers"][indx]
    #formatiranje neznanih simbolov v prave simbole
    formatting = [
        ("#039;", "'"),
        ("&'", "'"),
        ("&quot;", '"'),
        ("&lt;", "<"),
        ("&gt;", ">")
        ]
    #replace v stringu
    for tuple in formatting:
        question = question.replace(tuple[0], tuple[1])
        correct = correct.replace(tuple[0], tuple[1])
    #replace v listi
    for tuple in formatting:
        wrong = [char.replace(tuple[0], tuple[1]) for char in wrong]
        
    #.append doda v array 
    parameters["question"].append(question)
    parameters["correct"].append(correct)

    all_answers = wrong + [correct]
    random.shuffle(all_answers)

    parameters["answer1"].append(all_answers[0])
    parameters["answer2"].append(all_answers[1])
    parameters["answer3"].append(all_answers[2])
    parameters["answer4"].append(all_answers[3])

#globalni parametri
parameters = {
    "question":[],
    "answer1":[],
    "answer2":[],
    "answer3":[],
    "answer4":[],
    "correct":[],
    "score":[],
    "index":[]
}


#global spremenljivke za widget
widgets = {
    "logo": [],
    "button": [],
    "score": [],
    "question": [],
    "answer1": [],
    "answer2": [],
    "answer3": [],
    "answer4": [],
    "message": [],
    "message2": []
}

# grid layout
grid = QGridLayout()

#brisanje dodanih graficnih gumbov in vprasanj
def clear_widgets():
    ''' hide all existing widgets and erase
        them from the global dictionary'''
    for widget in widgets:
        if widgets[widget] != []:
            widgets[widget][-1].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()
# funkcija brisanje parametrov ob koncu igre
def clear_parameters():
    for parm in parameters:
        if parameters[parm] !=[]:
            for i in range(0, len(parameters[parm])):
                parameters[parm].pop()
    parameters["index"].append(random.randint(0,49))
    parameters["score"].append(0)


#funkcija zacetka igre
def start_game():
    #zacetek igre, reset vse widget
    clear_widgets()
    clear_parameters()
    preload_data(parameters["index"][-1])
    frame2()

#kreiranje gumbov z vprasanji
def create_buttons(answer, l_margin, r_margin):
    #kreiranje posodnih buttonov z custom left - right margin
    button = QPushButton(answer)
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setFixedWidth(485)
    button.setStyleSheet(
        #setting variable margins
        "*{margin-left: " + str(l_margin) +"px;"+
        "margin-right: " + str(r_margin) +"px;"+
        '''
        border: 4px solid '#176744';
        color: white;
        font-family: 'shanti';
        font-size: 16px;
        border-radius: 25px;
        padding: 15px 0;
        margin-top: 20px;
        }
        *:hover{
            background: '#176744';
        }
        '''
    )
    button.clicked.connect(lambda x: is_correct(button))
    return button
#funkcija preverjanje ce je vprasanje pravilno
def is_correct(btn):
    if btn.text() == parameters["correct"][-1]:
        print(btn.text() + "is correct")

        temp_score = parameters["score"][-1]
        #.pop() vzame samo en elemetn iz arraya
        parameters["score"].pop()
        parameters["score"].append(temp_score + 10)

        parameters["index"].pop()
        parameters["index"].append(random.randint(0,49))
        preload_data(parameters["index"][-1])

        widgets["score"][-1].setText(str(parameters["score"][-1]))
        widgets["question"][0].setText(parameters["question"][-1])
        widgets["answer1"][0].setText(parameters["answer1"][-1])
        widgets["answer2"][0].setText(parameters["answer2"][-1])
        widgets["answer3"][0].setText(parameters["answer3"][-1])
        widgets["answer4"][0].setText(parameters["answer4"][-1])

        if parameters["score"][-1]==100:
            clear_widgets()
            frame3()
    else:
        clear_widgets()
        frame4()
# funkcija za zacetni meni
def frame1():
    clear_widgets()
    #logo widget
    image = QPixmap("logo.png")
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet("margin-top: 100px;")
    widgets["logo"].append(logo)

    #button widget
    button = QPushButton("PLAY")
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.setStyleSheet(
        '''
        *{
            border: 4px solid '#176744';
            border-radius: 45px;
            font-size: 35px;
            color: 'white';
            padding: 25px 0;
            margin: 100px 200px;
        }
        *:hover{
            background: '#176744';
        }
        '''
    )
    #button callback
    button.clicked.connect(start_game)
    widgets["button"].append(button)

    #place global widgets 
    grid.addWidget(widgets["logo"][-1], 0, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 1, 0, 1, 2)


#FRAME 2
#funkcija za igro
def frame2():
    #score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet(
        '''
        font-size: 35px;
        color: 'white';
        padding: 15px 10px;
        margin: 20px 200px;
        background: '#64A314';
        border: 1px solid '#64A314';
        border-radius: 35px;
        '''
    )
    widgets["score"].append(score)

    #question widget
    question = QLabel(parameters["question"][-1])
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setWordWrap(True)
    question.setStyleSheet(
        '''
        font-family: 'shanti';
        font-size: 25px;
        color: 'white';
        padding: 75px;
        '''
    )
    widgets["question"].append(question)

    #answer button widgets
    button1 = create_buttons(parameters["answer1"][-1], 85, 5)
    button2 = create_buttons(parameters["answer2"][-1], 5, 85)
    button3 = create_buttons(parameters["answer3"][-1], 85, 5)
    button4 = create_buttons(parameters["answer4"][-1], 5, 85)

    widgets["answer1"].append(button1)
    widgets["answer2"].append(button2)
    widgets["answer3"].append(button3)
    widgets["answer4"].append(button4)


    #place widget
    grid.addWidget(widgets["score"][-1], 0, 1)
    grid.addWidget(widgets["question"][-1], 1, 0, 1, 2)
    grid.addWidget(widgets["answer1"][-1], 2, 0)
    grid.addWidget(widgets["answer2"][-1], 2, 1)
    grid.addWidget(widgets["answer3"][-1], 3, 0)
    grid.addWidget(widgets["answer4"][-1], 3, 1)

#FRAME 3 - WIN GAME
#v primeru pravilnih 10 odgovorov se izrise ta frame ki prikazuje stevilo tock in pohvalo

def frame3():
    #congradulations widget
    message = QLabel("Congratulations! your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 25px; color: 'white'; margin: 100px 0px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel("100")
    score.setStyleSheet("font-size: 100px; color: #8FC740; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #go back to work widget
    message2 = QLabel("Nice work")
    message2.setAlignment(QtCore.Qt.AlignCenter)
    message2.setStyleSheet(
        "font-family: 'Shanti'; font-size: 30px; color: 'white'; margin-top:0px; margin-bottom:75px;"
        )
    widgets["message2"].append(message2)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        "*{background:'#176744'; padding:25px 0px; border: 1px solid '#176744'; color: 'white'; font-family: 'Arial'; font-size: 25px; border-radius: 40px; margin: 10px 300px;} *:hover{background:'#176744';}"
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

    button.clicked.connect(frame1)

    widgets["button"].append(button)

    #logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet(
        "padding :10px; margin-top:75px; margin-bottom: 20px;"
    )
    widgets["logo"].append(logo)

    #place widgets on the grid
    grid.addWidget(widgets["message"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["button"][-1], 4, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 5, 0, 2, 2)


#              FRAME 4 - FAIL
#funkcija za frame ko je odgovor napacen
def frame4():
    #sorry widget
    message = QLabel("Sorry, this answer \nwas wrong\n your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet(
        "font-family: 'Shanti'; font-size: 35px; color: 'white'; margin: 75px 5px; padding:20px;"
        )
    widgets["message"].append(message)

    #score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setStyleSheet("font-size: 100px; color: white; margin: 0 75px 0px 75px;")
    widgets["score"].append(score)

    #button widget
    button = QPushButton('TRY AGAIN')
    button.setStyleSheet(
        '''*{
            padding: 25px 0px;
            background: '#176744';
            color: 'white';
            font-family: 'Arial';
            font-size: 35px;
            border-radius: 40px;
            margin: 10px 200px;
        }
        *:hover{
            background: '#176744';
        }'''
        )
    button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    button.clicked.connect(frame1)

    widgets["button"].append(button)

    

    #place widgets  na zaslonu
    grid.addWidget(widgets["message"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["button"][-1], 2, 0, 1, 2)
    #grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)