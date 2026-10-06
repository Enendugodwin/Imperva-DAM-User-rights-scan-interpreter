# User Rights Scan — Web Version

A browser-based version of the desktop User Rights Scan report builder. Select a CSV, XLSX, or XLS export and download an Excel workbook containing:

1. `Detailed_Hierarchy` — grouped by account, database, privilege type, and object type.
2. `Account_Priv_Summary` — source-row counts by account and privilege type.
3. `DB_Object_Summary` — source-row counts by database and object type.

## Run it

This is a static web app; it does not need a Python server or a build step. With Node.js installed, run `node serve.js` from this folder and open <http://127.0.0.1:8080>. The small local server binds to your computer only. You can also publish `index.html` using GitHub Pages or serve it with another static web server.

The spreadsheet libraries are loaded from jsDelivr, so an internet connection is needed when opening the page. The selected scan file itself is parsed and processed in the browser and is not uploaded to a server.

## Source data

The first worksheet in an Excel workbook, or the header row in a CSV, must contain these exact columns:

- `Account Name`
- `DB Name`
- `Priv. Type`
- `Obj. Type`
- `Object Name`

Rows missing grouping values are omitted from the relevant grouped output. CSV files are parsed incrementally; Excel files are read in the browser and may require substantial memory when very large.

## Files

- `index.html` — the complete web application.
- `serve.js` — optional, dependency-free local web server for Node.js.
- `UserRightScan.py` — the existing Tkinter desktop application.
- `UserRightScan.ipynb` — notebook development version.
