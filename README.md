Reddit Persona Builder

A Python script that generates a **user persona** by scraping a Reddit user's profile (posts and comments) and using a transformer-based language model to infer personality traits, interests, profession, and more — with **citations**.

---

## Features

-  Takes any Reddit user profile URL as input
-  Scrapes the user’s recent **posts and comments**
-  Uses a **transformer-based LLM** (GPT-2 or any HuggingFace model) to build a persona
-  Outputs a detailed **user persona in text format**
-  Cites the Reddit comments/posts used to infer each trait
-  Clean and modular codebase

---

##  Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/reddit-persona-builder.git
cd reddit-persona-builder
```

---

### 2. Install Dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

Install requirements:

```bash
pip install -r requirements.txt
```

---

### 3. Configure Reddit API

Create a `.env` and add your Reddit API credentials:

```
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
REDDIT_USER_AGENT=your_user_agent
```

You can get these credentials by creating an app at: https://www.reddit.com/prefs/apps

---

### 4. Run the Script

Run the script with a Reddit profile URL:

```bash
python reddit_persona_builder.py https://www.reddit.com/user/kojied/
```

---

##Output

- The generated persona will be saved in the `personas/` folder.
- Example:
  ```
  personas/
  ├── kojied_persona.txt
  ├── Hungry-Move-6603_persona.txt
  ```

Each persona file contains:
- An LLM-generated description of the user
- A `[Citations]` section citing the posts/comments used

---

## Example Output (snippet)

```
User Persona:
This user appears to be interested in space exploration and computer science. They often post about ethical issues in AI and have a critical yet thoughtful tone...

[Citations]
- Interest from: "AI must be regulated... "
- Personality from: "I believe everyone should question authority..."
- Location: Not explicitly found, inferred by model.
- Profession from: "Working in robotics gives me a unique view on..."
```

---

##Example Reddit Profiles

Run on:
- https://www.reddit.com/user/kojied/
- https://www.reddit.com/user/Hungry-Move-6603/

These are already included in `/personas/`.

---

## Project Structure

```
reddit-persona-builder/
├── reddit_persona_builder.py      # Main script
├── requirements.txt               # Python dependencies
├── .env.example                   # Sample env file
├── README.md                      # This file
├── personas/                      # Output folder
│   ├── kojied_persona.txt
│   └── Hungry-Move-6603_persona.txt
```

---

##  Model Used

- [HuggingFace Transformers](https://huggingface.co/models) - GPT-2 (`gpt2`) by default
- You can change the model in the `pipeline()` function inside `reddit_persona_builder.py`

---

## License

This project is for evaluation purposes only. All data belongs to its respective Reddit users. Do not use it to create profiles without permission.

---
