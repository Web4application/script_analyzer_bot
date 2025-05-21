# Script Analyzer Bot

**AI-powered assistant for analyzing scripts, speeches, and textual content.**

Script Analyzer Bot is a fast, efficient, and intelligent tool designed to help writers, content creators, and communicators gain deep insights into their text. Using advanced NLP techniques and deep learning, it delivers structural analysis, sentiment breakdowns, pacing evaluations, and more—giving you a powerful edge in refining written or spoken content.

---

## Features

- **Script & Speech Analysis**  
  Automatically detects key sections, emotional tone, pacing, and logical flow.

- **Sentiment & Emotion Detection**  
  Classifies emotional undertones and overall sentiment trends in your script.

- **Linguistic Intelligence**  
  Highlights repetitive phrasing, verbosity, and grammar inconsistencies.

- **Named Entity Recognition (NER)**  
  Identifies people, places, events, and abstract concepts within the text.

- **FastAPI Backend**  
  RESTful API endpoints for integration with apps, dashboards, or other services.

- **Modular & Extensible**  
  Built with clean architecture to support plug-and-play NLP enhancements.

---

## Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **NLP Libraries:** spaCy, HuggingFace Transformers
- **Async Runtime:** Uvicorn
- **Containerization:** Docker (optional)
- **Frontend (optional):** Streamlit or React for UI layer (future support)

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip or conda
- (Optional) Docker

### Installation

```bash
git clone https://github.com/Web4application/script_analyzer_bot.git
cd script_analyzer_bot
pip install -r requirements.txt


## Running the API

uvicorn app.main:app --reload
http://127.0.0.1:8000/docs
