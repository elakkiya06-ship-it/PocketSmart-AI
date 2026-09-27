# Phase 5 – Project Development

## 1. Project Name

**PocketSmart AI – Smart Budget & Recommendation Assistant**

## 2. Development Overview

PocketSmart AI was developed as a web-based AI recommendation application.

The application allows users to provide their requirements and budget-related information and receive personalized recommendations generated using artificial intelligence.

## 3. Development Environment

The project was developed using:

* Visual Studio Code
* Python
* FastAPI
* HTML
* CSS
* JavaScript
* Google Gemini AI
* Git
* GitHub

## 4. Project Structure

The main project contains the following components:

```text
PocketSmart-AI/
│
├── 01_Brainstorming_and_Ideation/
├── 02_Requirement_Analysis/
├── 03_Project_Design/
├── 04_Project_Planning/
├── 05_Project_Development/
├── 06_Project_Testing/
├── 07_Project_Documentation/
├── 08_Project_Demonstration/
│
├── static/
│   └── css/
│       └── style.css
│
├── templates/
│
├── main.py
├── requirements.txt
└── README.md
```

## 5. Frontend Development

The frontend was developed using HTML, CSS and JavaScript.

The interface includes:

* Home page
* Login page
* Registration page
* Dashboard
* Recommendation input forms
* Recommendation results
* Recommendation details
* History
* Navigation and action buttons

The UI uses responsive layouts so that the application can be used on different screen sizes.

## 6. Backend Development

The backend was developed using Python and FastAPI.

The backend is responsible for:

* Handling application routes
* Processing user requests
* Managing authentication
* Receiving recommendation inputs
* Communicating with the AI service
* Returning recommendation results
* Handling application responses

## 7. AI Integration

Google Gemini AI is integrated into the application to generate personalized recommendations.

The basic process is:

```text
User Requirements
       ↓
FastAPI Backend
       ↓
Gemini AI
       ↓
AI Generated Recommendation
       ↓
Recommendation Result
```

The AI receives the relevant user requirements and generates a response based on the provided information.

## 8. Recommendation Result

The recommendation result page presents:

* AI-generated recommendation
* Budget-focused information
* Practical suggestions
* Additional recommendation details
* Navigation options

The result interface is designed to make the generated information easy to understand.

## 9. Authentication

The application includes user authentication features.

Users can:

* Register an account
* Log in
* Access the dashboard
* Log out

Authentication helps control access to user-specific features.

## 10. History Feature

The application provides a history section for accessing previous recommendation information.

This allows users to refer back to earlier recommendations instead of generating the same information repeatedly.

## 11. Error Handling

The application handles common problems such as:

* Invalid user input
* Authentication errors
* AI service errors
* Missing information
* Application request errors

Suitable messages can be displayed to help users understand the problem.

## 12. Dependency Management

The project dependencies are maintained in:

```text
requirements.txt
```

This allows the required Python packages to be installed when setting up or deploying the project.

## 13. Version Control

Git is used for version control.

The project is maintained in a public GitHub repository:

**PocketSmart-AI**

The development work is committed phase-wise so that project progress can be tracked.

## 14. Deployment

The application was deployed as a web service using Render.

The deployed application can be accessed through the Render-provided web URL.

## 15. Development Result

The development phase produced a working PocketSmart AI web application with:

* User authentication
* Dashboard
* AI-powered recommendations
* Budget-focused suggestions
* Recommendation details
* History
* Responsive UI
* Online deployment

## 16. Conclusion

The Project Development phase converted the planned system design into a working web application. The frontend, backend, AI integration, authentication, recommendation features and deployment were implemented to create the PocketSmart AI system.
