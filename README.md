# User Rights Scan

User Rights Scan analyzes a database user-rights export and produces an Excel audit workbook. Choose either the **Python desktop app** or the **browser-based web app**.

Both versions generate these sheets:

1. `Detailed_Hierarchy` — groups objects by account, database, privilege type, and object type.
2. `Account_Priv_Summary` — source-row counts by account and privilege type.
3. `DB_Object_Summary` — source-row counts by database and object type.

## Python desktop version

### Run from source

Install Python 3, then open a terminal in this folder and run:

```powershell
python -m pip install pandas openpyxl
python UserRightScan.py
```

The app opens a file picker for a CSV or XLSX export, then asks where to save the report. Tkinter is included with most Windows Python installations. If Python is already installed but the `python` command is unavailable, try the Windows `py` launcher instead:

```powershell
py -m pip install pandas openpyxl
py UserRightScan.py
```

### Run the packaged Windows app

If the packaged executable is present, double-click `dist/UserRightScan.exe`. Python does not need to be installed to run that executable.

## Browser-based web version

With Node.js installed, run the local static server from this folder:

```powershell
node serve.js
```

Then open <http://127.0.0.1:8080>. The server binds to your computer only. Alternatively, publish `index.html` with GitHub Pages or serve it with another static web server.

The web app accepts CSV, XLSX, and XLS files. It uses the first worksheet in Excel workbooks. Spreadsheet libraries are loaded from jsDelivr, so an internet connection is needed when opening the page. The scan file itself is processed in the browser and is not uploaded to a server. CSV parsing is incremental; very large Excel files may require substantial browser memory.

## Required source columns

The CSV header row or first Excel worksheet must contain these exact column names:

- `Account Name`
- `DB Name`
- `Priv. Type`
- `Obj. Type`
- `Object Name`

The Python desktop app accepts CSV and XLSX files. The web app also accepts XLS files. Rows with blank grouping values are omitted from the corresponding grouped output.

## Project files

- `UserRightScan.py` — Python/Tkinter desktop app.
- `UserRightScan.ipynb` — notebook development version.
- `index.html` — browser-based app.
- `serve.js` — optional, dependency-free local server for the web app.
- `UserRightScan.spec` — PyInstaller build configuration.
