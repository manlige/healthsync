# HealthSync App Prototype

A comprehensive health data management application prototype that helps users track their medications, appointments, and health records.

## Features

- **User Authentication**
  - Login and Sign Up functionality
  - Profile management
  - Multi-profile support

- **Health Data Management**
  - Medication tracking
  - Appointment scheduling
  - Health records storage
  - Data visualization

- **Profile Management**
  - User profiles
  - Profile switching
  - Privacy settings

## Project Structure

```
health-app-prototype/
├── frontend/
│   ├── assets/
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── icons/
│   └── *.html
├── backend/
│   ├── app.py
│   ├── check_db.py
│   ├── create_sample_db.py
│   ├── requirements.txt
│   ├── data/
│   │   └── health_data.json
│   └── healthsync_sample.db
├── README.md
├── LICENSE
└── .gitignore
```

## Technical Stack

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Bootstrap

- **Backend**
  - Python Flask
  - SQLite Database
  - RESTful API

## Setup Instructions

1. **Prerequisites**
   - Python 3.x
   - pip (Python package manager)

2. **Installation**
   ```bash
   # Clone the repository
   git clone https://github.com/datasciencemasters/go.git
   cd go/health-app-prototype

   # Install dependencies
   pip install -r backend/requirements.txt
   ```

3. **Database Setup**
   ```bash
   # Create sample database (optional)
   cd backend
   python create_sample_db.py
   ```

4. **Running the Application**
   ```bash
   # Start the backend server
   cd backend
   python app.py
   ```

5. **Accessing the Application**
   - Open `frontend/index.html` in your web browser
   - The application will be available at `http://127.0.0.1:5000`

## Sample Data

The application comes with a sample database (`healthsync_sample.db`) containing:

- Demo user account:
  - Username: demo_user
  - Password: demo123
  - Email: demo@example.com

- Sample medications:
  - Metformin (500mg)
  - Insulin (10 units)
  - Aspirin (81mg)

- Sample appointments:
  - Regular checkup with Dr. Smith
  - Specialist consultation with Dr. Johnson

- Sample health records:
  - Blood sugar readings
  - Blood pressure measurements
  - Weight tracking

## API Endpoints

- `/api/users`: User management
- `/api/medications`: Medication tracking
- `/api/appointments`: Appointment scheduling
- `/api/health-records`: Health data management

## Development

To contribute to this project:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 