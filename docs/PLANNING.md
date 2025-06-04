# Conway’s Game of Life – Final Evaluation Project

## 🔗 GitHub Repository
[Click here to view the GitHub repo](https://github.com/HDSB-BCHS-2425-ICS3UC/final-evaluation-project-shreyasipanthee.git)

---

## 📘 Project Overview
This project is a simulation of **Conway’s Game of Life** built using **Python** and the **pygame** library.

Conway’s Game of Life is a zero-player game where the evolution of a grid of cells is determined by its initial state and a set of mathematical rules.

---

## 🎮 Game Rules
- **Underpopulation**: Any live cell with fewer than two live neighbours dies.
- **Overcrowding**: Any live cell with more than three live neighbours dies.
- **Survival**: Any live cell with two or three live neighbours lives on to the next generation.
- **Reproduction**: Any dead cell with exactly three live neighbours becomes a live cell.

---

## 🧠 General Program Breakdown
- Initialize a **10x10 grid** of cells.
- Each cell can be in one of two states: **alive** or **dead**.
- Update the grid in generations according to the rules.
- Allow **user interaction**:
  - Click to toggle a cell’s state
  - Press keys to:
    - Start/pause simulation
    - Clear/reset the board
- Visually display everything using `pygame`.

---

## ✨ Features
- Accurate neighbor detection and rule application
- Smooth visual updating of the simulation
- Clean and user-friendly input handling
- Grid boundaries are handled safely

---

## 🧱 Program Structure
- A **2D list** (`grid`) represents the 10x10 cell matrix.
- A function counts **alive neighbours** with edge/boundary checks.
- **Pygame** handles window setup, drawing, and user input.
- A `Cell` class is used to:
  - Store state (alive/dead)
  - Draw itself to the screen
  - Toggle state on click
