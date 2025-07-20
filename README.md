# 🛠️ Multitool Utility Panel 🚀

A modular **Tkinter-based desktop application** built for automating common daily developer tasks. Designed for offline use, easy expansion, and clean user experience.

---

## 🌟 Features

- 📂 **PDF Editor** – Replace text in PDFs with word-level precision
- 📄 **PDF Summarizer** – AI-powered offline summarization using HuggingFace transformers
- 📎 **PDF Merger** – Merge multiple PDFs into one
- 🖼️ **Image to PDF** – Convert images into a single PDF
- 📁 **Download Sorter** – Organize cluttered downloads folder by file types
- 📄 **Dummy File Generator** – Generate dummy PDF, TXT, Excel, or Word files for testing
- 📥 **YouTube Downloader** – Download YouTube videos in various formats
- 🧠 **Helper Tab** – Auto-generated info about each tool and its usage

---

## 🧠 Technologies Used

| Category         | Tools / Libraries Used                                 |
|------------------|--------------------------------------------------------|
| GUI              | `tkinter`, `ttk`                                       |
| PDF Handling     | `PyMuPDF`, `PyPDF2`, `reportlab`, `Pillow`             |
| AI Summarization | `transformers`, `torch`, `huggingface-hub`             |
| Video Downloads  | `pytube`, `moviepy` (optional)                         |
| Image Handling   | `Pillow`                                               |
| Utilities        | `threading`, `os`, `shutil`, `json`, `importlib`       |

---

## 🔧 Folder Structure

project-root/
│
├── app.py # Main launcher file
├── config.json # All tool configurations
├── bots/ # All tool scripts (PDF, YouTube, etc.)
│ ├── pdf_editor_tool/
│ ├── pdf_summarizer/
│ ├── yt_downloader/
│ └── ...
│
├── tools/
│ └── helper_ui.py # Dynamic helper tab
│
├── utils/
│ ├── logger.py # Logging events
│ └── ... # Shared logic
│
└── requirements.txt # Python dependencies



# 1. Clone the repo
git clone https://github.com/your-username/multitool-utility-panel.git
cd multitool-utility-panel

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate   # for Windows
# OR
source venv/bin/activate  # for macOS/Linux

# 3. Install all requirements
pip install -r requirements.txt

# 4. Launch the app
python app.py