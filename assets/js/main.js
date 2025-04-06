// Global state management
const appState = {
    isLoggedIn: false,
    currentUser: null,
    appointments: [],
    doctors: [
        {
            id: 1,
            name: 'Dr. Sarah Johnson',
            specialty: 'Endocrinologist',
            rating: 4.8,
            experience: '15+ years',
            nextAvailable: 'Today, 2:00 PM',
            about: 'Board-certified endocrinologist specializing in diabetes management.',
            education: 'Harvard Medical School',
            languages: ['English', 'Spanish'],
            location: 'Medical Center, Room 302'
        },
        {
            id: 2,
            name: 'Dr. Michael Chen',
            specialty: 'Cardiologist',
            rating: 4.9,
            experience: '20+ years',
            nextAvailable: 'Tomorrow, 10:00 AM',
            about: 'Experienced cardiologist focused on preventive care.',
            education: 'Stanford Medical School',
            languages: ['English', 'Mandarin'],
            location: 'Heart Center, Room 205'
        },
        {
            id: 3,
            name: 'Dr. Emily Brown',
            specialty: 'General Practitioner',
            rating: 4.7,
            experience: '10+ years',
            nextAvailable: 'Today, 4:30 PM',
            about: 'Family physician with expertise in preventive medicine.',
            education: 'Yale Medical School',
            languages: ['English'],
            location: 'Family Care Center, Room 101'
        }
    ],
    healthData: {
        bloodGlucose: [],
        bloodPressure: [],
        weight: [],
        steps: []
    },
    notifications: {
        push: true,
        email: true,
        medicationReminders: true,
        appointmentReminders: true
    }
};

// Initialize app state from localStorage if available
function initializeState() {
    const savedState = localStorage.getItem('healthsync_state');
    if (savedState) {
        Object.assign(appState, JSON.parse(savedState));
    }
}

// Save state to localStorage
function saveState() {
    localStorage.setItem('healthsync_state', JSON.stringify(appState));
}

// Navigation function
function navigateToPage(path) {
    window.location.href = path;
}

// Loading state management
function showLoading() {
    const loader = document.createElement('div');
    loader.className = 'loader-overlay';
    loader.innerHTML = `
        <div class="loader">
            <div class="spinner"></div>
            <p>Loading...</p>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.querySelector('.loader-overlay');
    if (loader) {
        loader.remove();
    }
}

// Error/Success message handling
function showMessage(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('show');
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }, 100);
}

// Authentication functions
function login(email, password) {
    showLoading();
    // Simulate API call
    setTimeout(() => {
        appState.isLoggedIn = true;
        appState.currentUser = {
            name: 'John Doe',
            email: email,
            avatar: null
        };
        saveState();
        hideLoading();
        navigateToPage('APP_Screen2_User Dashboard(Home Page).html');
    }, 1000);
}

function logout() {
    showLoading();
    setTimeout(() => {
        appState.isLoggedIn = false;
        appState.currentUser = null;
        saveState();
        hideLoading();
        navigateToPage('APP_Screen1_Welcome&Login.html');
    }, 500);
}

// Appointment management
function bookAppointment(doctorId, date, time) {
    if (!appState.appointments) {
        appState.appointments = [];
    }

    const doctor = appState.doctors.find(d => d.id === doctorId);
    if (!doctor) return;

    const appointment = {
        id: Date.now(),
        doctor: {
            id: doctor.id,
            name: doctor.name,
            specialty: doctor.specialty
        },
        date: date,
        time: time,
        status: 'upcoming',
        location: doctor.location
    };

    appState.appointments.push(appointment);
    saveState();
    return appointment;
}

// Health data management
function addHealthData(type, value, date = new Date()) {
    if (!appState.healthData[type]) {
        appState.healthData[type] = [];
    }

    const data = {
        id: Date.now(),
        value: value,
        date: date.toISOString(),
        timestamp: date.getTime()
    };

    appState.healthData[type].push(data);
    appState.healthData[type].sort((a, b) => b.timestamp - a.timestamp);
    saveState();
    return data;
}

// Add CSS styles for loader and toast
const style = document.createElement('style');
style.textContent = `
    .loader-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.8);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }

    .loader {
        text-align: center;
    }

    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid var(--border-color);
        border-top: 4px solid var(--primary-color);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .toast {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%) translateY(100px);
        background: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
        z-index: 9999;
    }

    .toast.show {
        transform: translateX(-50%) translateY(0);
    }

    .toast-success {
        border-left: 4px solid #22c55e;
    }

    .toast-error {
        border-left: 4px solid #ef4444;
    }
`;

document.head.appendChild(style);

// Initialize state when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeState); 