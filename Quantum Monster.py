# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 12:50:02 2019

@author: jn135
"""
# Required imports
import pygame, sys, math
import json
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer import noise
from qiskit import *
from qiskit.visualization import plot_histogram

# Basic variables for design of game
width = 1024
height = 720
radius = 300.0
monster = math.pi/2
boatx = 0.1
boaty = 0.0
bspeed = 1.0
gspeed = 3.5
speed_mult = 3.0
clicking = False
color = (255,255,255)

# User prompts allowing for n number of slices and n number of shots
num_slice = int(input("How many quantum slices do you want? Type 0 for standard game, and >1 for quantum game. : "))
num_shots = int(input("How many shots do you want to simulate on slice collision? Must be >0 : "))

# Filepath to IBM font
font_path = "IBMPlexMono-Medium.ttf"

# Generate an Aer noise model for device
f = open('noise_file.txt', 'r')
noise_dict_file = json.loads(f.read())

# Feature of Aer to export/import noise models from dictionaries
noise_model = NoiseModel.from_dict(noise_dict_file)
basis_gates = noise_model.basis_gates

# Generate a quantum circuit
q = QuantumRegister(2)
c = ClassicalRegister(2)
qc = QuantumCircuit(q, c)

qc.h(q[0])
qc.cx(q[0], q[1])
qc.measure(q, c)


# Allows for the game to reset after win or loss.
def restart():
    global monster, boatx, boaty, clicking
    monster = 0.0
    boatx = 0.1
    boaty = 0.0
    clicking = False


pygame.init()
window = pygame.display.set_mode((width, height))


def clear():
    global gspeed, num_slice, cut_list
    radius_mult = bspeed / gspeed
    window.fill((33, 39, 42))
    pygame.draw.circle(window, (116, 200, 255), (int(width / 2), int(height / 2)), int(radius * 1.00), 0)
    cut_list = [0]

    # The following lines allow the circle to be divided into quantum slices.
    if num_slice == 0:
        cut_list = []
    
    else:
        slice_step = 360/num_slice

        for i in range(1,num_slice):
            cut_angle = cut_list[0] + slice_step*i
            cut_list.append(cut_angle)
    

    for i in range(0,len(cut_list)):
        ibm_line_color=(69, 137 ,255)
        angle_rad = cut_list[i]*(math.pi /180)
        pygame.draw.line(window,ibm_line_color,((int(width / 2), int(height / 2))),
                         (int(width / 2)+radius*(math.cos(angle_rad)), int(height / 2)+radius*(math.sin(angle_rad))),3)

        
def redraw(draw_text=False, win=False):
    global monster, gspeed, color
    clear() 
    neg_cut_list = [i * -1 for i in cut_list]
    final_cut_list = cut_list + neg_cut_list
    
    # The following allows the game to know when the boat has crossed a quantum slice, activating the quantum simulation
    if cut_list != []:
        if abs((int(round((math.atan2(boaty, boatx)*(180/math.pi))))) - 
               min(final_cut_list, key=lambda x:abs(x-(int(round((math.atan2(boaty, boatx)*(180/math.pi)))))))) <= 5:
            color = (255, 0, 0)
            # Perform noisy simulation
            backend = Aer.get_backend('qasm_simulator')
            job_sim = execute(qc, backend,
                              noise_model=noise_model,
                              basis_gates=basis_gates, shots=num_shots)
            sim_result = job_sim.result()
            result_dict = dict(sim_result.get_counts(qc))
            
            # The result of the quantum simulation will teleport the monster to the corresponding location.
            if max(result_dict, key=result_dict.get) == '01':
                monster = math.pi/2
            if max(result_dict, key=result_dict.get) == '10':
                monster = -math.pi/2
            if max(result_dict, key=result_dict.get) == '00':
                monster = math.pi           
            if max(result_dict, key=result_dict.get) == '11':
                monster = 0      
        else:
            color = (255, 255, 255) 
    pygame.draw.circle(window, color, (int(width / 2 + boatx), int(height / 2 + boaty)), 6, 2)
    pygame.draw.circle(window, (218, 30, 40),
                       (int(width / 2 + radius * math.cos(monster)), int(height / 2 + radius * math.sin(monster))), 6, 0)

    
    # All text functions to indicate quantum results, victory, loss, title, and current score.
    if draw_text:
        font = pygame.font.Font(font_path, 35)
        if win:
            text = font.render("Victory! Increasing Monster's Speed, Try Again!", 1, (36, 161, 72))
        else:
            text = font.render("Your Wave Function Collapsed, Try Again!", 1, (218, 30, 40))
        textpos = text.get_rect()
        textpos.centerx = window.get_rect().centerx
        textpos.centery = height / 3
        window.blit(text, textpos)

    font = pygame.font.Font(font_path, 20)
    
    text = font.render("IBM Quantum Monster Game", 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centerx = width / 4 - 50
    textpos.centery = height - 45
    window.blit(text, textpos)
    
    text = font.render("Quantum Monsters's Speed: " + str(round(gspeed,3)), 1, (255, 255, 255))
    textpos = text.get_rect()
    textpos.centerx = width / 4 - 50
    textpos.centery = height - 20
    window.blit(text, textpos)
    
    text2 = font.render("[1:0]", 1, (255, 255, 255))
    textpos2 = text2.get_rect()
    textpos2.centerx = width / 2
    textpos2.centery = height - 680
    window.blit(text2, textpos2)
    
    text3 = font.render("[0:1]", 1, (255, 255, 255))
    textpos3 = text3.get_rect()
    textpos3.centerx = width / 2
    textpos3.centery = height - 35
    window.blit(text3, textpos3)
    
    text4 = font.render("[0:0]", 1, (255, 255, 255))
    textpos4 = text4.get_rect()
    textpos4.centerx = width / 6 - 5
    textpos4.centery = height - 360
    window.blit(text4, textpos4)
    
    text5 = font.render("[1:1]", 1, (255, 255, 255))
    textpos5 = text5.get_rect()
    textpos5.centerx = width - width / 6 + 5
    textpos5.centery = height - 360
    window.blit(text5, textpos5)

    pygame.display.flip()

# Enables the monster to follow the character around the circle
def updatemonster():
    global monster, gspeed
 
    newang = math.atan2(boaty, boatx)
    diff = newang - monster
    if diff < math.pi: diff += math.pi * 2.0
    if diff > math.pi: diff -= math.pi * 2.0
    if abs(diff) * radius <= gspeed * speed_mult:
        monster = newang
    else:
        monster += gspeed * speed_mult / radius if diff > 0.0 else -gspeed * speed_mult / radius
    if monster < math.pi: monster += math.pi * 2.0
    if monster > math.pi: monster -= math.pi * 2.0
        
def moveBoat(x, y):
    global boatx, boaty
    dx = x - boatx
    dy = y - boaty
    mag = math.sqrt(dx * dx + dy * dy)
    if mag <= bspeed * speed_mult:
        boatx = x
        boaty = y
    else:
        boatx += bspeed * speed_mult * dx / mag
        boaty += bspeed * speed_mult * dy / mag

# Detects win and adds to speed if the character wins, if not resets the game
def detectWin():
    global gspeed
    if boatx * boatx + boaty * boaty > radius * radius:
        diff = math.atan2(boaty, boatx) - monster
        if diff < math.pi: diff += math.pi * 2.0
        if diff > math.pi: diff -= math.pi * 2.0
        while True:
            is_win = abs(diff) > 0.000001
            redraw(True, is_win)
            events = [event.type for event in pygame.event.get()]
            if pygame.QUIT in events:
                pygame.display.quit()
                sys.exit(0)
                pygame.quit()
            elif pygame.MOUSEBUTTONDOWN in events:
                restart()
                if is_win:
                    gspeed += 0.2
                break


clock = pygame.time.Clock()
clear()
while True:
    x = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit(0)
            pygame.quit()
        clicking = pygame.mouse.get_pressed()[0]
        if pygame.mouse.get_pressed()[2]:
            restart()

    if clicking:
        x, y = pygame.mouse.get_pos()
        moveBoat(x - width / 2, y - height / 2)
    updatemonster()
    detectWin()
    redraw()
    clock.tick(60)
