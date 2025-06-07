
# 🖼️ NotionLens

**Automatically capture screenshots every minute and log them to Notion.**  
Designed for freelancers, creators, and productivity lovers who want to visually track their work sessions in Notion.

---

## 🚀 Features

- ⏱️ Takes a screenshot every minute
- ☁️ Uploads screenshots to S3 (or any pre-signed URL)
- 🧠 Creates a Notion database entry with the image and timestamp
- 🧹 Automatically deletes local screenshots after upload
- 🔁 Runs quietly as a background process (daemonized)

---

## 🛠️ Requirements

- Python 3.7+
- macOS (uses `screencapture`)
- A Notion integration (API key + database)
- An S3 bucket or similar with pre-signed PUT URL support

---

## 📦 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/notionlens.git
   cd notionlens
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```env
   NOTION_API_KEY=your_notion_api_key
   DATABASE_ID=your_notion_database_id
   S3_UPLOAD_URL=https://yourbucket.s3.amazonaws.com/
   ```

---

## ⚙️ Run It Once (for testing)

```bash
python3 screenshot_to_notion.py
```

---

## 🧙‍♂️ Run It in the Background (Daemonize with PM2)

### Step 1: Install `pm2`
```bash
npm install -g pm2
```

### Step 2: Start the script with PM2
```bash
pm2 start screenshot_to_notion.py --interpreter python3 --name notionlens
```

### Step 3: Save the process
```bash
pm2 save
```

### Step 4: Enable auto-start on boot
```bash
pm2 startup
# Follow the instructions it outputs to finalize
```

---

## 📁 Folder Structure

```
notionlens/
├── screenshot_to_notion.py   # Main script
├── .env                      # Environment variables (not committed)
├── README.md                 # You're reading this
└── requirements.txt          # Python dependencies
```

---

## 📄 Example Notion Output

Each row in the Notion database will include:
- A title with the timestamp
- A file block with the uploaded screenshot
- A date field to sort/filter by

---

## 🧯 Stop or Restart

- Stop:
  ```bash
  pm2 stop notionlens
  ```
- Restart:
  ```bash
  pm2 restart notionlens
  ```

---

## 🛡️ Security Note

Never commit your `.env` file. Use `.gitignore` to exclude secrets.

```bash
echo ".env" >> .gitignore
```

---

## 📷 Built with ❤️ for productivity nerds
By Adam Joron (https://github.com/joronadam3)
