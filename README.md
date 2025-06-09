<p align="center">
  <img src="https://raw.githubusercontent.com/joronadam3/NotionLens/main/logo.png" alt="NotionLens Logo" width="150"/>
</p>

# 🖼️ NotionLens

**Automatically capture screenshots and log them to Notion.** Designed for freelancers and productivity lovers who want a visual record of their work sessions.

---

## 🚀 Features

- ⏱️ Periodically takes macOS screenshots
- ☁️ Uploads screenshots to an S3 bucket (or any pre-signed URL)
- 🧠 Creates entries in a Notion database
- 🔁 Runs quietly in the background after setup

---

## 🛠️ Requirements

- Python 3.7+
- macOS (uses `screencapture`)
- A Notion integration (API key + database)
- An S3 bucket or similar with pre-signed PUT URL support

---

## 📦 Installation

```bash
# Clone and install
git clone https://github.com/joronadam3/NotionLens.git
cd NotionLens
pip install -r requirements.txt
```

Run the interactive setup:

```bash
python -m notionlens setup
```

Start capturing screenshots in the background:

```bash
python -m notionlens start
```

Configuration is stored in `~/.notionlens/config.json`.

## Usage

Logs are written to `~/.notionlens/notionlens.log`.
Check that the background process is running with:

```bash
ps -ef | grep notionlens
```

The output should show a `python -m notionlens capture` entry with its PID.
You can also search for this PID in Activity Monitor to locate or stop the process.


---

## 📁 Folder Structure

```
NotionLens/
├── notionlens/          # Package with CLI and capture logic
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🛡️ Security Note

Your configuration file may contain secrets. Keep it safe and never commit it to version control.

---

## 📷 Built with ❤️ for productivity nerds
By [Adam Joron](https://github.com/joronadam3)
