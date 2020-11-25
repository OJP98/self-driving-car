# self-driving-car
Little self learning racing car made in python and a genetic algorithm implementation. It's mainly made with Pygame and NEAT.

## Requirements

* Python 3
* Python package manager (pip)


## Installation

Use the package manager **pip** to install the requirements.

```bash
pip install -r requirements.txt
```

## Usage

1. Head to *simulation* folder
2. Run `python main.py`


### How to change the amount of sensors

Quick note: The amount of sensors can only be: 3, 4, 5, 9 or 11

1. Go to *simulation* folder
2. Edit the file *.env* and change the value of **NUM_SENSORES** to how many sensors you'd like
3. Save changes and close the file
4. While still in the folder, edit the file *config-feedforward.txt*
5. Go to line 48 and change the value of **num_inputs** to match the amount of sensors in step 2
6. Save changes and close the file
7. Run `python main.py`


### How to change the map

Quick note: The map can only be 1, 2 or 3. 1 is the easiest map, meanwhile 3 is the hardest.

1. Go to *simulation* folder
2. Edit the file *.env* and the value of *MAP* to the difficulty of the map you'd like
3. Save changes and close the file
4. Run `python main.py`


## Video Demonstration
<a href="http://www.youtube.com/watch?feature=player_embedded&v=eSVx6LJKfRc
" target="_blank"><img src="http://img.youtube.com/vi/eSVx6LJKfRc/0.jpg" 
alt="Youtube video thumbnail" width="800" height="450" border="10" /></a>


## Developers

* Oscar Juárez
* José Pablo Cifuentes


Universidad del Valle de Guatemala - 2020
