# forestGrub - Dinosaur Game

A classic dinosaur runner game implemented in Python using pygame, similar to the Chrome browser offline game.

## Features

- **Dinosaur Character**: Jump and duck to avoid obstacles
- **Dynamic Obstacles**: Cacti and flying birds with varying heights and designs  
- **Progressive Difficulty**: Game speed and obstacle frequency increase over time
- **Scoring System**: Distance-based scoring with high score tracking
- **Visual Effects**: 
  - Day/night cycle with dynamic sky colors
  - Animated dinosaur with running legs
  - Ground dust particles
  - Detailed obstacle sprites
- **Sound Effects**: Jump, collision, and scoring sounds
- **Smooth Controls**: Space bar to jump, C key to duck

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python dinosaur_game.py
```

## Controls

- **Space Bar**: Make the dinosaur jump
- **C Key**: Make the dinosaur duck/crouch
- **Space Bar** (during game over): Restart the game

## Game Mechanics

- Avoid cacti by jumping over them
- Avoid flying birds by ducking under them or jumping over them
- Score increases based on distance traveled
- Game speed gradually increases for added challenge
- Collision with any obstacle ends the game

## Technical Implementation

- Built with Python 3 and pygame
- Collision detection using pygame rectangles
- Smooth animations and particle effects
- Dynamic difficulty scaling
- Sound generation using numpy for audio effects

## File Structure

```
forestGrub/
├── dinosaur_game.py          # Main game file
├── requirements.txt          # Python dependencies  
├── sounds/
│   └── sound_generator.py    # Sound effect generation
├── assets/                   # Placeholder for future sprite files
└── README.md                 # This file
```

Enjoy playing the dinosaur game!