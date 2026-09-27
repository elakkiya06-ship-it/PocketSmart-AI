# Phase 3 – Project Design

## 1. Project Name

**PocketSmart AI – Smart Budget & Recommendation Assistant**

## 2. System Architecture

PocketSmart AI is designed as a web-based application.

The basic architecture is:

**User → Frontend → FastAPI Backend → Google Gemini AI → Recommendation → User**

### Main Components

* User Interface
* FastAPI Backend
* Google Gemini AI
* Data Storage
* GitHub
* Render Deployment

## 3. Main Modules

### 3.1 Authentication Module

This module handles:

* User registration
* User login
* User logout
* Session management

### 3.2 Dashboard Module

The dashboard provides access to the main features of PocketSmart AI.

### 3.3 Recommendation Module

The user provides information such as:

* Budget
* Requirements
* Preferences
* Category or purpose

The backend processes the information and sends the appropriate request to the AI service.

### 3.4 AI Recommendation Module

Google Gemini AI processes the user's requirements and generates a personalized recommendation.

### 3.5 Recommendation Details Module

This module displays the generated recommendation clearly to the user.

### 3.6 History Module

This module allows users to view their previous recommendation records.

## 4. Data Flow

1. User opens PocketSmart AI.
2. User registers or logs in.
3. User opens the dashboard.
4. User enters budget and requirement details.
5. The frontend sends the information to the FastAPI backend.
6. The backend processes the request.
7. The relevant information is sent to Google Gemini AI.
8. Gemini generates the recommendation.
9. The backend receives the AI response.
10. The recommendation is displayed to the user.
11. The recommendation can be available in the user's history.

## 5. User Interface Design

The application uses a clean and modern interface containing:

* Navigation bar
* Dashboard
* Input forms
* Cards
* Buttons
* Recommendation result section
* History section

The interface is designed to be responsive and easy to navigate.

## 6. Navigation Structure

```text
Home
│
├── Login
│
├── Register
│
└── Dashboard
    │
    ├── Recommendation
    │
    ├── Recommendation Details
    │
    ├── History
    │
    └── Logout
```

## 7. Technology Design

| Layer           | Technology            |
| --------------- | --------------------- |
| Frontend        | HTML, CSS, JavaScript |
| Backend         | Python, FastAPI       |
| AI              | Google Gemini AI      |
| Version Control | Git & GitHub          |
| Deployment      | Render                |

## 8. Design Goals

The system design focuses on:

* Simple navigation
* User-friendly interface
* Responsive layout
* Secure authentication
* AI-powered recommendations
* Budget-focused suggestions
* Easy maintenance
* Clear presentation of results

## 9. Expected Output

The completed design should provide a structured web application where users can enter their requirements and receive personalized AI-generated budget recommendations.

## 10. Conclusion

The Project Design phase defines the architecture, modules, data flow, navigation and technology structure of PocketSmart AI. This design will serve as the foundation for the project planning and development phases.
