# 🧠 Blob Life – Final Evaluation Project: Planning File

## ✅ Option Chosen
**Option:** Create an enhanced, fun version of Conway’s Game of Life using Python and Pygame.

---

## 💡 Problem Breakdown – Steps to Solve the Project

### 1. Setup and Grid System
- Initialize a 10x10 2D list of `Cell` objects.
- Each `Cell` will store its row/col position, alive state, and display image.

### 2. Cell Class Implementation
- Add `draw()` and `toggle()` methods.
- Use animated blob images instead of colored squares.
- Animate blobs using frame-switching or transitions.

### 3. Conway’s Rules Logic
- Implement the 4 main rules:
  - **Underpopulation**: Fewer than 2 neighbors → dies
  - **Overcrowding**: More than 3 neighbors → dies
  - **Survival**: 2–3 neighbors → lives
  - **Reproduction**: Exactly 3 neighbors → becomes alive
- Ensure boundary-safe neighbor checking.

### 4. User Input and Controls
- Mouse click to toggle blob state.
- Keyboard controls:
  - `Spacebar` – Start/pause simulation
  - `Left Arrow` – Reset all blobs
  - `R` – Randomize blobs
  - `ESC` – Exit the game

### 5. Themes System
- Add multiple themes that change:
  - Background color
  - Blob images

### 6. Templates
- Create fun preset patterns like:
  - Heart
  - Smiley
  - Letter A
- Load them with one click.

### 7. Tutorial and Storyline
- Friendly character "Blobbo" explains the rules.
- Simple language and visuals for young children.
- Add a skip button and a back button.

### 8. Audio Features
- Background music and sound effects.
- Add a mute/unmute button.

### 9. Navigation and UI
- Start page with buttons to Play, Tutorial, Templates, etc.
- Use `current_page` variable to control navigation.
- Add:
  - Back button
  - Generation counter
  - Progress bar

---

## ⚠️ Potential Challenges and Solutions

| Problem | Anticipated Difficulty | Planned Solution |
|--------|-------------------------|------------------|
| Blobs not animating correctly | Medium | Use multiple blob frames and cycle with `pygame.time.get_ticks()` |
| Neighbor count errors at grid edges | High | Create a safe `get_neighbors()` function with bounds checking |
| Switching between pages | Medium | Use a `current_page` variable and draw different content per state |
| Game continues 1 more generation after pause | High | Only update grid when `running` is True, ignore if just paused |
| Reset doesn't clear blobs | Medium | Loop through grid, set `alive = False`, `image = None`, reset gen count |
| Confusing UI | Medium | Use readable fonts, soft button shapes, clear labels |
| Audio sync issues | Low | Use `pygame.mixer.music` for BGM |
| Accessibility for users | High | Use big buttons, simple text, visuals, and help from Blobbo |

---

## 🗂️ Summary of the Full Plan

Blob Life is a friendly, animated simulation game inspired by Conway’s Game of Life, built for kids. It features colorful themes, sound, templates, and a tutorial with a mascot. The project is broken into clear steps: building the logic and cell system first, then UI, animation, audio, templates, and navigation. Key challenges like user-friendly design and safe neighbor logic are addressed in the plan, ensuring a smooth, fun experience.

---

🔗 [Click here to view the GitHub repository](https://github.com/HDSB-BCHS-2425-ICS3UC/final-evaluation-project-shreyasipanthee.git)
