# 🧬 Blob Life: A Friendly Twist on Conway's Game of Life

---

## 🎮 Overview  
**Blob Life** is a fun, interactive simulation based on **Conway's Game of Life**, reimagined with colorful blobs, animations, themed backgrounds, sound effects, and a guided tutorial featuring Blobbo the blob. Designed to be intuitive for even a 5-year-old, it's both educational and fun!

---

## 🧠 Game Rules  
Each square (cell) can either have a **blob** or be **empty**. Every round (generation):  
- A lonely blob (0–1 friends) disappears.  
- A happy blob (2–3 friends) survives!  
- A crowded blob (4+ friends) disappears.  
- A new blob appears where there are **exactly 3 blob friends** nearby.  

---

## 🚀 How to Run the Game  
1. **Clone the repository:**  
   ```bash
   git clone https://github.com/HDSB-BCHS-2425-ICS3UC/final-evaluation-project-shreyasipanthee.git
   ```

2. **Navigate to the project directory:**  
   ```bash
   cd final-evaluation-project-shreyasipanthee
   ```

3. **Install dependencies (requires Python):**  
   ```bash
   pip install pygame
   ```

4. **Run the game:**  
   ```bash
   python blob_life_game.py
   ```

---

## 🌟 Features  
- 🎨 **Start Page with Animation** — colorful, moving blobs and shapes set the tone!  
- 🧠 **Tutorial Mode** — walk through the rules with Blobbo, your animated blob guide.  
- 🎭 **Themed Backgrounds** — choose your favorite visual style!  
- 🧩 **Templates** — instantly create fun patterns like a ❤️, 🙂, or even the letter **A**!  
- 🔊 **Mute Button** — toggle background music on any screen.  
- 🎮 **Game Screens** — Tutorial, Storyline, Simulation, Theme Select, Start Menu.  

---

## 🕹️ Controls  

| Key/Button     | Action                                  |
|----------------|------------------------------------------|
| **Mouse Click**| Toggle blobs on/off (in simulation)      |
| **Spacebar**   | Start/Pause simulation                   |
| **R**          | Randomize the grid                       |
| **Left Arrow** | Reset grid                               |
| **Right Arrow**| Advance one generation manually          |
| **1, 2, 3**    | Apply templates (Heart, Smiley, Letter A)|
| **S (Hold)**   | Speed up generation updates              |
| **Mute Button**| Toggle background music                  |
| **Back Button**| Return to the start menu                 |

---

## 📘 Developer Documentation  
- [Planning and Features](docs/PLANNING.md)  
- [Pseudocode](docs/PSEUDOCODE.md)  
- [Sources](docs/SOURCES.md)

---

## 👨‍💻 Credits  
Created by **Shreyasi Panthee**  
Inspired by **John Conway’s Game of Life**  
