# Valentine's Surprise

This project is a fun, interactive Python application designed to create a personalized Valentine’s Day surprise. It blends engaging animations with an interactive word search puzzle and a final heartfelt message to provide a unique and memorable experience.

## Purpose

The purpose of this project is to offer a creative and interactive way to ask someone to be your Valentine. It achieves this by:
- Displaying an animated main screen with bouncing background hearts and a central, pulsing (beating) heart.
- Asking the question "Will you be my Valentine?" with interactive Yes/No buttons.
- Transitioning to an interactive word search puzzle where hidden words (e.g., **LOVE**, **GABITA**, **HAPPY**, and **VALENTINES**) must be found by clicking and dragging across a grid.
- Providing an optional Hint button that gives a clue (one word at a time) for any word that has not yet been found.
- Revealing a final heartfelt message once all words are found.

## How It Works

The project is built using Python with the Tkinter GUI toolkit and is divided into several modules:

- **main.py**  
  Manages the overall application and navigation between different screens:
  - **Home Page:**  
    - Contains a top section with a canvas for bouncing hearts and an overlaid canvas for a large, pulsing heart.
    - Includes a bottom section with the question label and interactive Yes/No buttons.
    - Clicking **Yes** leads to the interactive word search puzzle.
  
- **animation.py**  
  Provides functions for all animated elements:
  - **Bouncing Hearts:**  
    Small hearts of various sizes and colors bounce around within a designated canvas area.
  - **Pulsing Heart:**  
    A large central heart beats (scales up and down) continuously, drawing attention to the main question.

- **puzzle.py**  
  Implements the interactive word search puzzle:
  - Generates a 12×12 grid with hidden words.
  - Users interact by clicking and dragging across grid cells to select letters.
  - The selection is dynamically highlighted; if the selected cells match one of the hidden words, that word remains highlighted.
  - A **Hint** button provides a clue (e.g., for **HAPPY** or **VALENTINES**, the hint is "HOLIDAY"; for **GABITA**, it is "NICKNAME"; for **LOVE**, it is "WHAT WE DO WITH IN A BED", **Shaboinking** it is for fun time) for one word that has not yet been found.
  - When all words are found, a success message is displayed and the application transitions to the final message screen.

- **messages.py**  
  (If included) Displays a final loving message to conclude the experience.

## Running the Project

1. **Requirements:**  
   - Python 3 with Tkinter support.

2. **Setup:**  
   - Clone this repository.
   - Optionally, create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate  # On Windows use: venv\Scripts\activate
     ```

3. **Run the Application:**  
   In your project directory, execute:
   ```bash
   python main.py

4. **Interact:**
- Enjoy the animated main page.
- Click **Yes** to start the interactive word search puzzle.
- Use the **Hint** button if you need a clue.
- Solve the puzzle to reveal the final animated loving message.

# Summary

"Valentine's Surprise" is a creative, interactive project that combines dynamic animations with an engaging word search puzzle. It culminates in a personalized, heartfelt message, making it a perfect way to add a special touch to your Valentine’s Day celebration.

## Happy Valentine’s Day!