# Google-Sheet-Automation-Scheduler
This Flask-based web application allows users to schedule automated data updates from a local JSON file (urls_data.json) into a Google Sheets document. Users can submit URL, XPath, index, and trigger time via a web form.
# Google Sheet Automation Scheduler Documentation

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technology Stack & Dependencies](#technology-stack--dependencies)
4. [Environment Setup](#environment-setup)
5. [Configuration Files](#configuration-files)
6. [Directory Structure](#directory-structure)
7. [Application Workflow](#application-workflow)
8. [Function & Module Descriptions](#function--module-descriptions)

   * `init_google()`
   * `append_column(sheet, data, url)`
   * `update_google_sheet()`
9. [API Endpoints](#api-endpoints)

   * `GET /` and `POST /`
   * `GET /fuck`
   * `GET /download_pre_json`
   * `POST /upload_pre_json`
10. [Scheduling Jobs](#scheduling-jobs)
11. [Error Handling & Logging](#error-handling--logging)
12. [Security Considerations](#security-considerations)
13. [Extensibility & Customization](#extensibility--customization)
14. [Troubleshooting & FAQs](#troubleshooting--faqs)
15. [SEO Keywords](#seo-keywords)
16. [Author & License](#author--license)

---

## Project Overview

This Flask-based web application allows users to schedule automated data updates from a local JSON file (`urls_data.json`) into a Google Sheets document. Users can submit URL, XPath, index, and trigger time via a web form. The application:

* Stores schedule entries in a JSON file.
* Inserts a new row in the Google Sheet for each entry.
* Schedules a daily job at the specified time to update the sheet with the latest scraped data.

## Key Features

* **Dynamic Scheduling**: Users schedule daily data updates via a simple form.
* **Google Sheets Integration**: Authenticates using service account and `gspread`.
* **Background Scheduler**: Uses `APScheduler` with `CronTrigger` for timed tasks.
* **JSON Persistence**: Stores schedule entries in `urls_data.json` for durability.
* **REST Endpoints**: Provides API endpoints to add tasks, download/update JSON data.

## Technology Stack & Dependencies

* **Python 3.8+**
* **Flask**: Lightweight web framework
* **gspread**: Google Sheets API client for Python
* **google-auth**: Service account credentials handling
* **APScheduler**: Advanced scheduling library for Python
* **Requests**: HTTP client for optional network calls
* **Werkzeug**: Underlying WSGI utility library in Flask

Install dependencies via `pip`:

```bash
pip install flask gspread google-auth apscheduler requests
```

## Environment Setup

1. **Google Service Account**

   * Create a service account in Google Cloud Console.
   * Download the JSON key file (e.g., `credet.json`).
   * Share the target Google Sheet with the service account email.
2. **Local Dependencies**

   * Install required Python packages.
   * Ensure network access to Google APIs.
3. **Run the App**

   ```bash
   export FLASK_APP=app.py
   flask run --host=0.0.0.0 --port=5000
   ```

## Configuration Files

* **`credet.json`**: Google service account credentials.
* **`urls_data.json`**: Stores scheduled tasks as a JSON array of objects:

  ```json
  [
    {"url":"https://...","xpath":"//div","index":0,"time":"14:30","data":"0"},
    ...
  ]
  ```

## Directory Structure

```
/project_root
├── app.py                # Main Flask application
├── credet.json           # Google service account key
├── templates/
│   ├── index.html        # Main form for scheduling
│   └── fuck.html         # Auxiliary page
├── urls_data.json        # Persisted schedule entries
└── requirements.txt      # Python dependencies
```

## Application Workflow

1. **User Submission** (`POST /`):

   * The form captures `url`, `xpath`, `index`, and `time`.
   * New entry appended to `urls_data.json`.
   * Inserts a new row in the Google Sheet (`sheet.insert_row`).
   * Schedules a daily job at specified time using `APScheduler`.
2. **Scheduled Task**:

   * Every day at each entry's time, `update_google_sheet()` runs.
   * Reads `urls_data.json`, fetches each entry's `data`, and updates the sheet.
3. **Data Sync Endpoints**:

   * `GET /download_pre_json`: Returns current `urls_data.json` content.
   * `POST /upload_pre_json`: Accepts JSON payload to update a specific entry's `data`.

## Function & Module Descriptions

### `init_google()`

* **Purpose**: Authenticate and return a `gspread` worksheet object.
* **Logic**:

  1. Load service account credentials.
  2. Authorize `gspread` client.
  3. Open spreadsheet by URL.
  4. Return the worksheet named **WebScrap**.

### `append_column(sheet, data, url)`

* **Purpose**: Append a new column of `data` for the row matching `url`.
* **Logic**:

  1. Locate the cell containing the URL (`sheet.find(url)`).
  2. Determine the last populated column in that row.
  3. Add one new column to the sheet.
  4. Update the cell at the new column index with `data`.

### `update_google_sheet()`

* **Purpose**: Batch-process all scheduled entries and push updates.
* **Logic**:

  1. Load `urls_data.json`.
  2. Initialize the Google Sheet via `init_google()`.
  3. For each entry, locate the URL and call `append_column`.
  4. Skip entries whose URLs are not found.

## API Endpoints

### `GET /` & `POST /`

* **GET**: Render `index.html` with current server time.
* **POST**: Accept form data (`url`, `xpath`, `index`, `time`), save to JSON, insert into sheet, schedule job.

### `GET /fuck`

* **Purpose**: Serve a secondary page (`fuck.html`).

### `GET /download_pre_json`

* **Purpose**: Return the current `urls_data.json` array as JSON.
* **Error**: Returns 404 if `urls_data.json` not found.

### `POST /upload_pre_json`

* **Purpose**: Update the `data` field for a specific URL entry.
* **Request**: JSON body with `url` and `data` fields.
* **Response**: Success or error message in JSON.

## Scheduling Jobs

Uses `BackgroundScheduler` from `APScheduler`:

```python
scheduler = BackgroundScheduler()
scheduler.start()
# On form submission:
trigger = CronTrigger(hour=HOUR, minute=MINUTE)
scheduler.add_job(update_google_sheet, trigger=trigger)
```

* Jobs persist only during the application runtime.
* For production, consider using a persistent job store (e.g., Redis).

## Error Handling & Logging

* **Form Validation**: Time format errors return HTTP 400 with JSON error.
* **Sheet Lookup**: Missing URLs are logged to console and skipped.
* **General Exceptions**: Wrapping critical sections with try/except and print stack trace.

## Security Considerations

* **Credential Safety**: `credet.json` must be secured and not exposed publicly.
* **Input Sanitization**: Validate form inputs to avoid injection into Google Sheets.
* **Rate Limiting**: Protect endpoints if exposed to the internet.

## Extensibility & Customization

* **Persistent Job Store**: Configure `APScheduler` to use Redis or SQLAlchemy.
* **Dynamic Sheet Selection**: Extend UI to choose worksheet names.
* **Enhanced Scraping**: Use `xpath` and `index` to pull live data before appending.
* **Authentication**: Add user login to secure scheduling interface.

## Troubleshooting & FAQs

* **Google API Errors**: Ensure service account has access and correct scopes.
* **Scheduling Issues**: Verify server time and timezone alignment.
* **File I/O Errors**: Check permissions on `urls_data.json`.

## SEO Keywords

```
Python Flask scheduler
Google Sheets API Python
gspread cron job
automated sheet update
APScheduler Flask example
Flask background jobs
JSON scheduling app
Python Flask scheduler
Google Sheets API Python
gspread cron job
automated sheet update
APScheduler Flask example
Flask background jobs
JSON scheduling app
```

---

## Author & License

**Author:** Smaron Biswas
**Date:** 2025-05-05
**License:** MIT License
