# IBM-Quantum-Monster
This repository contains a quantum version of the classic Lake Monster math puzzle. This is a submission to the 2019 IBM Q Awards.

The objective of the game is to move your character from the center of the circle to the edge (click in the direciton you wish to move) without being eaten by the quantum monster. When running the game you are prompted with two options, how many slices to divide the lake into and how many shots each simulation will run. Each time your character touches a slice line the quantum monster will teleport to the result of a quantum circuit. This teleportation is based on a noisy simulation mimicking real physical quantum computing devices. This teleportation aspect means that the traditional solution to the non-quantum version no longer works, and you will have to come up with alternative strategies. You can find a live tutorial here: https://youtu.be/YIUZ_C1l-1E

This project is based on Python 3.6, and you are welcome to install each of the required packages yourself including Pygame, Json, and Qiskit. Alternatively you can use our included conda environment, which can be implemented with the below instructions.

We recommend using anaconda to easily install the proper environment to run this program. Here are the steps:
1. Open Aanaconda prompt
2. Navigate to director containing the quantumenv.yaml file
3. Run the following command in Anaconda prompt: conda env create -f quantumenv.yaml
4. Activate the environment by running the following command in the Anaconda prompt: activate quantumenv
5. You can now run the Quantum Monster.py file

6. (Optional) You can run this program in Spyder by running the following command in the activated environment: spyder
7. Once spider starts navigate via the gui to the Quantum Monster.py file, open it, and run by pressing the green play button in the tool bar.


This game was inspired by the traditional version which is perfectly demonstrated by HackPoet on github:
https://github.com/HackerPoet/GoblinEscape
He also has a great blog description of the traditional puzzle's limitations by geometry:
http://datagenetics.com/blog/october12013/index.html
