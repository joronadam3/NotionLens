<p align="center">
  <img src="https://raw.githubusercontent.com/joronadam3/NotionLens/main/assets/logo.png" alt="NotionLens Logo" width="150"/>
</p>

# 🖼️ NotionLens

**Automatically capture screenshots and log them to Notion.** Designed for freelancers and productivity lovers who want a visual record of their work sessions.

---
![Product Launch Video](https://raw.githubusercontent.com/joronadam3/NotionLens/main/assets/Product%20Launch%20Video.gif)

## 🚀 Features

- ⏱️ Periodically takes macOS screenshots
- 🖥️ Captures all connected displays
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
pip install -e .
```

The editable install registers the `notionlens` command globally so you can run
it from any directory.

> **Note** macOS will ask for **Screen Recording** permission on first run.
Grant this to the terminal (or Python) so screenshots include your open apps.

Run the interactive setup:

```bash
notionlens setup
```

Command names are all lowercase.

Start capturing screenshots in the background:

```bash
notionlens start
```

Check the current status and tail the logs. If the process isn't running,
`notionlens status` also prints the latest error lines from the log file:

```bash
notionlens status
```

Stop the background process:

```bash
notionlens stop
```

Logs are written to `~/.notionlens/notionlens.log`.

Configuration is stored in `~/.notionlens/config.json`.

---

## 🗂️ Notion Template

A ready-to-use Notion database template is available here:  
[NotionLens Template](https://www.notion.com/templates/notinlens)


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
