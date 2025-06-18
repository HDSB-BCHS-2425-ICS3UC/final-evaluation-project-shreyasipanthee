# Blob Life – Final Evaluation Project

## 🔗 GitHub Repository
[Click here to view the GitHub repo](https://github.com/HDSB-BCHS-2425-ICS3UC/final-evaluation-project-shreyasipanthee.git)

---

## 📘 Project Overview
This project is an enhanced, fun version of **Conway’s Game of Life** called **Blob Life**, built using **Python** and the **pygame** library.

Blob Life simulates cellular automaton behavior with animated blob-like cells, colorful themes, and interactive gameplay designed to engage users.

---

## 🎮 Game Rules
- The core rules of Conway’s Game of Life still apply:
  - **Underpopulation**: Any live blob with fewer than two live neighbours disappears.
  - **Overcrowding**: Any live blob with more than three live neighbours disappears.
  - **Survival**: Any live blob with two or three live neighbours survives.
  - **Reproduction**: Any dead cell with exactly three live neighbours creates a new blob.

---

## 🧠 General Program Breakdown
- Initialize a **10x10 grid** of animated blob cells.
- Each blob cell can be **alive (visible, animated)** or **dead (invisible)**.
- Multiple **colorful themes** change the background and blob colors.
- Interactive gameplay features:
  - Click cells to toggle blobs alive/dead before simulation starts.
  - Keyboard controls for starting, pausing, reseting, randomizing, and exiting.
  - Templates for preset patterns (like heart, smiley, initials).
  - Tutorial screens with a friendly character explaining rules.
- Animated blobs use visuals and smooth transitions.
- Sound effects and background music enhance user experience.

---

## ✨ Features
- Animated blob visuals replacing simple squares.
- Multiple colorful themes with matching backgrounds and blobs.
- User interface elements including a tutorial with Blobbo character.
- Preset templates to quickly load fun patterns.
- Responsive controls and smooth simulation updates.
- Clean, accessible UI for users.
- Sound and music integration.
- Grid boundaries handled safely in neighbor counts.

---

## 🧱 Program Structure
- A **2D list** (`grid`) contains `Cell` objects representing blobs.
- `Cell` class stores:
  - Position, size, alive state.
  - Methods for drawing animated blobs and toggling state.
- Theme system managing colors for backgrounds and blobs.
- Main game loop:
  - Handles user input and events.
  - Updates grid based on Conway’s rules each generation when running.
  - Draws animated blobs and UI elements.
- Additional modules or functions for:
  - Playing sounds and music.
  - Managing tutorials and storyline screens.

---

## 🕹️ Controls Summary
- **Mouse Click:** Toggle blob alive/dead before simulation starts.
- **Spacebar:** Start/pause simulation.
- **Left-arrow:** Reset all blobs to dead.
- **R:** Randomize blobs.
- **ESC:** Exit game.