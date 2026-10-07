# Python - Executable Title Changer (Windows)

**Python - Executable Title Changer** is a Windows command-line utility designed to change the window title of executable (`.exe`) files. It features two operational modes: dynamically overriding the window title in memory (Test Mode) or permanently altering the embedded string by generating a modified copy of the executable (Save Mode). 

This tool universally supports **UTF-16LE**, **UTF-8**, and **ASCII** text encodings commonly found in windows binaries.

## 🛠️ Requirements
* **Operating System:** Windows (7, 10, or 11)
* **Language:** [Python 3.6 or higher](https://python.org)
## 📥 How to Clone and Setup

Follow these steps to clone the repository to your local machine using Git:

1. Open your terminal of choice (**Command Prompt (CMD)**, **PowerShell**, or **Git Bash**).
2. Navigate to the directory where you want to store the project (e.g., `cd Documents`).
3. Run the following command to clone the repository:
   ```bash
   git clone https://github.com
   ```
   *(Make sure to replace `YOUR-USERNAME` with your actual GitHub username)*
4. Move into the project folder:
   ```bash
   cd Python-TitleEXEChanger
   ```
## 💻 How to Use

This script is a strict CLI tool and is not interactive (dragging and dropping an `.exe` file onto the script will not work). You must run it through the terminal by passing the required arguments.

### 1. Test Mode (`test`)
Launches the application and forces the window title change **only inside the RAM memory** while it runs. Your original file remains 100% untouched.

```bash
python flash_title_tool.py test "C:\Path\To\YourGame.exe" "Your New Title"
```
* To stop monitoring the title and return to the terminal, press `CTRL + C`.

### 2. Permanent Save Mode (`save`)
Searches for the specific old string inside the binary structure and outputs a **brand new modified file** (with a `_modificado.exe` suffix) with the title altered permanently.

If the executable uses the default Flash Player 34 string, run:
```bash
python flash_title_tool.py save "C:\Path\To\YourGame.exe" "New Title"
```

If the original file uses a custom title or an older Flash version, you **must** use the `--old-title` argument to specify the exact current window text (case-sensitive):
```bash
python flash_title_tool.py save "C:\Path\To\YourGame.exe" "New Title" --old-title "Adobe Flash Player 32"
```

## ⚠️ Important Rules for Save Mode

1. **Character Length Limit:** In `save` mode, your **New Title** cannot contain more characters (bytes) than the **Old Title**. This restriction keeps the PE file layout intact and prevents binary corruption. If you need a longer title, use **Test Mode**.
2. **Safety Measures:** The script explicitly blocks overwriting the original file directly, ensuring your source data is always safe.

## 🤝 Contributing
Contributions are welcome! Feel free to open an **Issue** or submit a **Pull Request** if you have optimizations or feature suggestions.

## 📝 License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
