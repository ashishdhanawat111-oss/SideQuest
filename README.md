# 🌿 SideQuest — AI-Powered Real-World Adventures

**Go outside. Explore your surroundings. Complete quests. Earn XP.**

SideQuest is an AI-powered outdoor scavenger hunt that turns everyday surroundings into a game. Players receive real-world challenges, discover objects outdoors, and submit photographs for AI verification.

Instead of relying only on self-reported completion, SideQuest uses an open-weight vision-language model to examine photographs and decide whether a quest has been completed.

## 🎯 The Problem

Many digital experiences encourage people to spend more time looking at screens.

SideQuest explores a different approach: using AI to encourage real-world exploration, observation, creativity, and outdoor activity.

## ✨ Features

- **Outdoor quests:** Discover interesting objects and scenes in the real world.
- **AI photo verification:** Upload a photograph and receive a PASS or FAIL verdict with an explanation.
- **XP and levels:** Earn 100 XP for completing a new quest and progress through Explorer, Adventurer, and Legend.
- **Stamp collection:** View completed quests and achievements.
- **Quest progression:** Skip challenges and move toward unfinished quests.
- **Persistent progress:** SQLite stores earned XP and completed quests between sessions.
- **Adventure-inspired interface:** A dark-green, game-themed UI.

## 🧠 Open-Weight AI

SideQuest uses **Google Gemma 3 (4B)** through **Ollama**.

The model examines uploaded photographs together with the active quest description and provides a verdict.

The AI runs locally on the machine hosting the application. No paid AI API is required.

**AI workflow:**

1. The player receives a quest.
2. The player explores the real world and takes a photograph.
3. The photograph and quest description are sent to Gemma 3 through Ollama.
4. The model returns a PASS or FAIL decision with an explanation.
5. A successful new quest awards XP and a stamp, saved in SQLite.

AI verification is experimental. The model may occasionally make incorrect judgments, and uploaded photographs are not proof of when or where they were taken.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| User interface | Streamlit |
| Vision-language model | Gemma 3 4B |
| Local model runtime | Ollama |
| Database | SQLite |
| Styling | Custom CSS |

## 🚀 Run Locally

### Prerequisites

- Python 3
- Ollama installed
- Enough system resources to run Gemma 3 4B

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/ashishdhanawat111-oss/SideQuest.git
cd SideQuest
```

**2. Install Python dependencies**

```bash
python -m pip install -r requirements.txt
```

**3. Download the AI model**

```bash
ollama pull gemma3:4b
```

Make sure Ollama is running.

**4. Start SideQuest**

```bash
python -m streamlit run app.py
```

Open the local Streamlit address shown in your terminal.

## 🎮 How to Play

1. Open SideQuest.
2. Read your active outdoor quest.
3. Explore your surroundings and find a matching scene or object.
4. Take a photograph and upload it.
5. Let Gemma 3 judge your discovery.
6. Earn XP and a stamp for a successful new quest.
7. Continue exploring!

## ⚠️ Current Limitations

- The application currently runs locally and requires Ollama.
- Progress is stored in a local SQLite database, designed for a single-player setup.
- AI photo verification is not guaranteed to be accurate.
- The application does not verify GPS location, photo authenticity, or whether a photograph was taken outdoors.
- There is no hosted public demo yet.

## 🌱 Future Improvements

- More diverse AI-generated quests
- Improved photo verification
- Mobile-friendly deployment
- Location-aware challenges with user consent
- Additional achievements and game progression

## 🏆 Hacktoberfest 2026

Built for the **Hacktoberfest 2026 Week 1 — Touch Grass** challenge.

The goal is to demonstrate how open-weight AI can motivate people to interact with the physical world instead of spending more time on their screens.

**Core idea:** AI should encourage real-world experiences, not replace them.

## 📄 License

A license has not yet been selected. See the repository for licensing information.