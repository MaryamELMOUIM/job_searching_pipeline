
# Job Searching Pipeline

This project is a job searching and tracking pipeline built using Flask, PostgreSQL, and Jooble API integration. It allows users to search, filter, and manage job listings, including scheduling interviews and updating job statuses. The app also includes an automated job fetch scheduler.

## Table of Contents

1. [Requirements](#requirements)
2. [Setup and Installation](#setup-and-installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Usage](#usage)
6. [Folder Structure](#folder-structure)
7. [Features](#features)
8. [Notes](#notes)

---

### Requirements

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- A [Jooble API Key](https://jooble.org/) (Register to get an API key)

---

### Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/job_searching_pipeline.git
   cd job_searching_pipeline
   ```

2. **Set Up Environment Variables**

   You will need to create a `.env` file in the root directory. This file contains the necessary environment variables for the app to function.

   **Example `.env` file:**
   ```env
   FLASK_ENV=development
   DATABASE_URL="your_database_url_here"
   JOOBLE_API_KEY="your_api_key_here"
   SECRET_KEY="your_secret_key_here"
   SCHEDULER_HOURS=24
   ```

   - `FLASK_ENV`: Set to `development` for development mode. Change to `production` when deploying.
   - `DATABASE_URL`: URL of your PostgreSQL database. If using Docker, this will likely be something like `postgresql://username:password@db:5432/dbname`.
   - `JOOBLE_API_KEY`: Your Jooble API key. Obtain it from Jooble's API dashboard.
   - `SECRET_KEY`: A secret key for Flask session management.
   - `SCHEDULER_HOURS`: Interval for the job fetching scheduler (e.g., 24 for daily updates).

3. **Build and Start the Docker Containers**
   ```bash
   docker-compose up --build
   ```

   This command will start the application and its dependencies (PostgreSQL and PGAdmin). The first time you run this, it will also build the necessary Docker images.

---

### Configuration

1. **Database Configuration**
   - The `DATABASE_URL` in the `.env` file should point to your PostgreSQL database.
   - By default, the database is set up to run in a Docker container.

2. **Jooble API Key**
   - You need to add your Jooble API key in the `.env` file. This is required for the job search functionality to work.
   - Replace `"your_api_key_here"` with the actual API key you obtained from Jooble.

3. **Scheduler**
   - The `SCHEDULER_HOURS` setting controls how often the scheduler fetches new jobs based on predefined keywords (e.g., every 24 hours).
   - This scheduler will automatically run as soon as the container starts for the first time.

---

### Running the Application

Once you've set up the environment variables and started the Docker containers, the application should be running. To access it:

1. **Open the application in your browser**
   - Go to `http://localhost:5000` to view the app.

2. **Access PGAdmin (optional)**
   - Go to `http://localhost:5050` to manage the PostgreSQL database.
   - Log in with the credentials provided in `docker-compose.yml`.

---

### Usage

- **Home Page (`All Jobs`)**: Shows all job listings with filtering options (by title, location, date, etc.).
  ![image](https://github.com/user-attachments/assets/c43c555f-fada-446a-9b0e-b1b4b95eaa59)
  
- **Applied Jobs Page**: Lists jobs marked as applied, with options to schedule interviews.
  ![image](https://github.com/user-attachments/assets/bf524b11-942d-43a8-b259-a0a7828b0203)
  ![image](https://github.com/user-attachments/assets/8384d95b-6a1a-4024-bf51-f9a7d84edfce)


- **Interview Scheduled Jobs Page**: Lists jobs scheduled for interviews. Here, you can set the interview date, update the interview status, and delete entries.
  ![image](https://github.com/user-attachments/assets/d4c1e9f7-f2aa-400e-84c3-650f1deffc1e)

- **Search for Jobs Page**: Allows users to manually search for jobs by keyword and location.
  ![image](https://github.com/user-attachments/assets/c18fe3df-0a9c-492c-bf38-7d07c01fb347)


---

### Folder Structure

The project folder structure is as follows:

```
job_searching_pipeline/
│
├── app.py                # Main application file
├── config.py             # Configuration file
├── models.py             # Database models
├── fetch_jobs.py         # Jooble API fetch logic
├── migrations/           # Database migrations folder
├── templates/            # HTML templates
│   ├── index.html        # Main jobs listing page
│   ├── applied_jobs.html # Applied jobs page
│   ├── interview_scheduled_jobs.html # Interview scheduled jobs page
│   ├── search.html       # Job search page
├── static/
│   └── style.css         # Custom CSS styles
├── .env                  # Environment variables
└── docker-compose.yml    # Docker Compose configuration
```

---

### Features

- **Job Searching**: Automatically fetches jobs based on specified keywords using the Jooble API.
- **Job Management**: Allows marking jobs as applied, scheduling interviews, and updating job statuses.
- **Automated Scheduler**: Periodically fetches new job postings based on keywords.
- **Filtering and Pagination**: Filters by title, location, date, and supports pagination for easy navigation.

---

### Notes

- Make sure to replace placeholder values in the `.env` file (e.g., `DATABASE_URL`, `JOOBLE_API_KEY`).
- The app uses `BackgroundScheduler` to periodically run the job fetching function.


---

Happy job searching!
