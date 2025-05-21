<h1 align="center">
  🌲 wtree
</h1>

<h4 align="center">Visualize a website’s structure from the command line</h4>

<p align="center">
  <a href="#context">Context</a> •
  <a href="#features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#example">Example</a>
</p>

---

## 🧠 Context

**wtree** is a Command Line Interface (CLI) tool designed to map out the structure of a website starting from its homepage. This project was created in an academic context focused on cybersecurity and surface mapping. wtree lets you visualize accessible paths, detect exposed directories or files, and perform basic keyword analysis on web content.

This project was developed as part of a student initiative at Paris Cité University.

---

## ✨ Key Features

- 🔗 Automatically extracts all links (`<a>`, `<img>`, `<script>`) from a given URL.
- 🌳 Builds a tree-like structure of the website’s layout.
- ⏱️ Optionally retrieves HTTP status codes, response times, and content sizes.
- 🔍 Supports keyword search in HTML content.
- 🎨 Colorful and readable CLI output.
- 🧠 Smart page caching to avoid redundant HTTP requests.

---

## ⚙️ How To Use

### 1. Clone the repository

```bash
git clone https://github.com/youruser/wtree
cd wtree
```

### 2. Run the script

```bash
python3 main.py <URL> [options]
```

### Available Options

| Option               | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `-f, --full`         | Display the full URL instead of just the file or folder name.              |
| `-r, --response`     | Check the HTTP status code, response time, and content size of each link. |
| `-k, --keyword`      | Comma-separated keywords to search for in page content.                   |

### Example

```bash
python3 main.py https://example.com -f -r -k login,password,admin
```

### 🔧 Build as an Executable

You can package `wtree` into a single standalone binary using `pyinstaller`:

```bash
# Install pyinstaller if not already installed
pip install pyinstaller

# Build the executable
pyinstaller --onefile --name wtree main.py

# Move it to a system path
sudo cp dist/wtree /usr/bin/
sudo chmod +x /usr/bin/wtree

# Run from anywhere
wtree https://example.com -r -f
```

---

## 📷 Example

Here is a sample output in the terminal:

![screenshot](https://i.imgur.com/TaUsA28.png)


---

## 🚨 Disclaimer

This project is intended for educational purposes only. Do not scan websites unless you have permission to do so.
