# 🎮 SmartWordle: AI-Powered Word Guessing Game

An interactive **Wordle-style web app** built with **Flask** that integrates **OpenAI** to generate intelligent hints.  
This project combines **software engineering, game logic, and AI integration** to create an engaging user experience while showcasing skills in **Python, APIs, data handling, and web development**.  

---

## ✨ Overview
SmartWordle challenges users to guess a hidden **5-letter word** within six attempts.  
Unlike traditional Wordle, this version leverages **OpenAI** to generate **contextual hints** that help players refine their guesses after three failed attempts.  

The game tracks performance, awards points, and stores scores — making it both fun and data-driven.  

---

## 🧩 Features
- **Classic Wordle Gameplay**: Guess a hidden 5-letter word with color-coded feedback.  
- **AI-Generated Hints**: After 3 attempts, request an **OpenAI-powered hint** describing the word without revealing it.  
- **Points System**:  
  - Start with 100 points.  
  - Lose 5 points per extra guess.  
  - Lose 10 points per hint.  
- **Score Tracking**: Saves game results (username, word, guesses, time, points) to `scores.json`.  
- **Web Interface**: Built with **Flask** templates (`index.html`, `game.html`, `win.html`, `lose.html`).  
- **Unit Testing**: Includes a test suite (`unittest`) for validating core game logic.  

---

## 🛠 Tech Stack
- **Backend**: Python, Flask  
- **Frontend**: HTML, CSS (via Flask templates)  
- **AI Integration**: OpenAI API (GPT-powered hints)  
- **Data Handling**: JSON for score persistence  
- **Testing**: Python `unittest`  
- **Other Tools**: Randomization, time tracking, regex validation  

---

## 💡 Skills Demonstrated
- **Flask Web Development**: Routing, rendering templates, handling requests.  
- **Game Logic Design**: Word selection, validation, hint mechanics, scoring system.  
- **AI Integration**: Prompt engineering + OpenAI API for intelligent clue generation.  
- **Data Persistence**: JSON-based score tracking with structured records.  
- **Testing & Reliability**: Unit tests to validate functions (guess validation, board state, scoring).  
- **Problem-Solving**: Designed rules for fairness (hints only after 3 attempts, unique guesses only, scoring balance).  

---

## 🎯 Key Outcomes
- Delivered a **working full-stack web app** with AI integration.  
- Reduced complexity by separating game logic (`WordleGame` class) from Flask routes.  
- Enhanced user experience with AI hints, scoring gamification, and error handling.  
- Built a **portfolio-ready project** that demonstrates **engineering + analytics skills**.  

---

## ☕ About Me

Hi! I’m **Palak Gupta**, a Mathematics–Computer Science student with a deep interest in data analytics, business intelligence, and data engineering. I enjoy building real-world projects that combine technical skill with business insight, using tools like SQL, Docker, Notion, and automation platforms like n8n.

📫 **Let’s connect**:  
- 🔗 [LinkedIn](https://www.linkedin.com/in/palakgupta28/)  
- 📧 [palakgupta0428@gmail.com](mailto:palakgupta0428@gmail.com)  

---


