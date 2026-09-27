import os
import uuid
import html

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from database import (
    create_users_table,
    create_history_table,
    register_user,
    check_user,
    save_history,
    get_history
)

from gemini_utils import (
    generate_recommendation,
    generate_image_recommendation
)


# =========================================================
# APP SETUP
# =========================================================

app = FastAPI(
    title="PocketSmart AI",
    version="1.0"
)

app.add_middleware(
    SessionMiddleware,
    secret_key="pocketsmart-secret-key-change-later"
)


# =========================================================
# FOLDERS
# =========================================================

os.makedirs("uploads", exist_ok=True)
os.makedirs("static/css", exist_ok=True)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


# =========================================================
# DATABASE
# =========================================================

create_users_table()
create_history_table()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def is_logged_in(request: Request):
    return "username" in request.session


def current_user(request: Request):
    return request.session.get("username")


def login_required(request: Request):

    if not is_logged_in(request):
        return RedirectResponse(
            "/login",
            status_code=303
        )

    return None


# =========================================================
# NAVBAR
# =========================================================

def navbar(request: Request):

    username = current_user(request)

    if username:

        safe_username = html.escape(
            str(username)
        )

        return f"""
        <nav class="navbar">

            <div class="nav-container">

                <a href="/" class="logo">
                    <span class="logo-icon">✦</span>
                    PocketSmart <span>AI</span>
                </a>

                <div class="nav-links">

                    <a href="/">Home</a>

                    <a href="/dashboard">
                        Dashboard
                    </a>

                    <a href="/history">
                        History
                    </a>

                    <a href="/recommendations-details">
                        Explore
                    </a>

                    <a href="/how-it-works">
                        How It Works
                    </a>

                    <span class="user-name">
                        Hi, {safe_username}
                    </span>

                    <a
                        href="/logout"
                        class="logout-btn"
                    >
                        Logout
                    </a>

                </div>

            </div>

        </nav>
        """

    return """
    <nav class="navbar">

        <div class="nav-container">

            <a href="/" class="logo">
                <span class="logo-icon">✦</span>
                PocketSmart <span>AI</span>
            </a>

            <div class="nav-links">

                <a href="/">
                    Home
                </a>

                <a href="/login">
                    Login
                </a>

                <a href="/register">
                    Register
                </a>

                <a href="/how-it-works">
                    How It Works
                </a>

            </div>

        </div>

    </nav>
    """


# =========================================================
# PAGE TEMPLATE
# =========================================================

def page_template(
    request: Request,
    title: str,
    content: str
):

    safe_title = html.escape(title)

    return f"""
    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <meta
            name="description"
            content="PocketSmart AI - Smart Budget Recommendation Assistant"
        >

        <title>
            {safe_title} | PocketSmart AI
        </title>

        <link
            rel="stylesheet"
            href="/static/css/style.css"
        >

    </head>

    <body>

        {navbar(request)}

        <main>
            {content}
        </main>

        <footer class="footer">

            <div class="footer-inner">

                <div>
                    <strong>
                        ✦ PocketSmart AI
                    </strong>

                    <p>
                        Smart planning.
                        Smarter spending.
                    </p>
                </div>

                <div>
                    <p>
                        © 2026 PocketSmart AI
                    </p>
                </div>

            </div>

        </footer>

    </body>

    </html>
    """


# =========================================================
# HOME
# =========================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    content = """

    <section class="hero">

        <div class="hero-content">

            <div class="hero-badge">
                ✨ AI-POWERED BUDGET ASSISTANT
            </div>

            <h1>
                Plan Smart.
                <span>Spend Smarter.</span>
            </h1>

            <p class="hero-description">
                PocketSmart AI helps you create
                personalized, practical and
                budget-friendly plans for your
                home, parties and jewelry needs.
            </p>

            <div class="hero-buttons">

                <a
                    href="/register"
                    class="btn"
                >
                    Get Started
                </a>

                <a
                    href="/login"
                    class="btn secondary-btn"
                >
                    Login
                </a>

            </div>

        </div>

    </section>


    <section class="section">

        <div class="section-heading">

            <span class="eyebrow">
                SMART PLANNING
            </span>

            <h2 class="section-title">
                One Assistant. Multiple Plans.
            </h2>

            <p>
                Choose a planner and let
                PocketSmart AI organize your
                ideas around your budget.
            </p>

        </div>


        <div class="planner-grid">

            <a
                href="/register"
                class="card planner-card"
            >

                <div class="card-icon">
                    🏠
                </div>

                <h3>
                    Home Planner
                </h3>

                <p>
                    Plan furniture, lights,
                    fans and other home
                    requirements according
                    to your budget.
                </p>

                <span class="card-link">
                    Plan your home →
                </span>

            </a>


            <a
                href="/register"
                class="card planner-card"
            >

                <div class="card-icon">
                    🎉
                </div>

                <h3>
                    Party Planner
                </h3>

                <p>
                    Organize food, decoration,
                    venue and entertainment
                    while keeping your budget
                    under control.
                </p>

                <span class="card-link">
                    Plan your party →
                </span>

            </a>


            <a
                href="/register"
                class="card planner-card"
            >

                <div class="card-icon">
                    💎
                </div>

                <h3>
                    Jewelry Planner
                </h3>

                <p>
                    Get jewelry suggestions
                    based on your occasion,
                    preferred style and budget.
                </p>

                <span class="card-link">
                    Plan jewelry →
                </span>

            </a>

        </div>

    </section>


    <section class="section soft-section">

        <div class="section-heading">

            <span class="eyebrow">
                WHY POCKETSMART?
            </span>

            <h2 class="section-title">
                Designed Around Your Budget
            </h2>

        </div>


        <div class="features">

            <div class="feature">

                <div class="feature-number">
                    01
                </div>

                <h3>
                    💰 Budget Focused
                </h3>

                <p>
                    Start with the amount
                    you are comfortable spending
                    and build your plan around it.
                </p>

            </div>


            <div class="feature">

                <div class="feature-number">
                    02
                </div>

                <h3>
                    🤖 AI Powered
                </h3>

                <p>
                    Generate personalized
                    recommendations based on
                    your selected requirements.
                </p>

            </div>


            <div class="feature">

                <div class="feature-number">
                    03
                </div>

                <h3>
                    📊 Organized
                </h3>

                <p>
                    Save your previous
                    recommendations and
                    revisit them through History.
                </p>

            </div>

        </div>

    </section>

    """

    return HTMLResponse(
        page_template(
            request,
            "Home",
            content
        )
    )


# =========================================================
# REGISTER PAGE
# =========================================================

@app.get(
    "/register",
    response_class=HTMLResponse
)
async def register_page(request: Request):

    content = """

    <section class="auth-section">

        <div class="auth-card">

            <div class="auth-icon">
                ✦
            </div>

            <span class="eyebrow">
                GET STARTED
            </span>

            <h1>
                Create Your Account
            </h1>

            <p class="auth-subtitle">
                Start creating smarter budget plans.
            </p>


            <form
                method="post"
                action="/register"
            >

                <label>
                    Username
                </label>

                <input
                    type="text"
                    name="username"
                    placeholder="Enter username"
                    required
                    minlength="3"
                >


                <label>
                    Password
                </label>

                <input
                    type="password"
                    name="password"
                    placeholder="Minimum 6 characters"
                    required
                    minlength="6"
                >


                <button
                    type="submit"
                    class="btn full-btn"
                >
                    Create Account
                </button>

            </form>


            <p class="auth-footer">
                Already have an account?
                <a href="/login">
                    Login
                </a>
            </p>

        </div>

    </section>

    """

    return HTMLResponse(
        page_template(
            request,
            "Register",
            content
        )
    )


# =========================================================
# REGISTER PROCESS
# =========================================================

@app.post(
    "/register",
    response_class=HTMLResponse
)
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    username = username.strip()

    message = ""

    if len(username) < 3:

        message = """
        <div class="alert error">
            Username must contain at least
            3 characters.
        </div>
        """

    elif len(password) < 6:

        message = """
        <div class="alert error">
            Password must contain at least
            6 characters.
        </div>
        """

    elif register_user(
        username,
        password
    ):

        return RedirectResponse(
            "/login",
            status_code=303
        )

    else:

        message = """
        <div class="alert error">
            Username already exists.
            Please choose another username.
        </div>
        """


    content = f"""

    <section class="auth-section">

        <div class="auth-card">

            <div class="auth-icon">
                ✦
            </div>

            <span class="eyebrow">
                GET STARTED
            </span>

            <h1>
                Create Your Account
            </h1>

            {message}

            <form
                method="post"
                action="/register"
            >

                <label>
                    Username
                </label>

                <input
                    type="text"
                    name="username"
                    required
                >


                <label>
                    Password
                </label>

                <input
                    type="password"
                    name="password"
                    required
                >


                <button
                    type="submit"
                    class="btn full-btn"
                >
                    Create Account
                </button>

            </form>


            <p class="auth-footer">
                Already have an account?
                <a href="/login">
                    Login
                </a>
            </p>

        </div>

    </section>

    """

    return HTMLResponse(
        page_template(
            request,
            "Register",
            content
        )
    )


# =========================================================
# LOGIN PAGE
# =========================================================

@app.get(
    "/login",
    response_class=HTMLResponse
)
async def login_page(request: Request):

    content = """

    <section class="auth-section">

        <div class="auth-card">

            <div class="auth-icon">
                🔐
            </div>

            <span class="eyebrow">
                WELCOME BACK
            </span>

            <h1>
                Login
            </h1>

            <p class="auth-subtitle">
                Continue planning smarter.
            </p>


            <form
                method="post"
                action="/login"
            >

                <label>
                    Username
                </label>

                <input
                    type="text"
                    name="username"
                    placeholder="Enter username"
                    required
                >


                <label>
                    Password
                </label>

                <input
                    type="password"
                    name="password"
                    placeholder="Enter password"
                    required
                >


                <button
                    type="submit"
                    class="btn full-btn"
                >
                    Login
                </button>

            </form>


            <p class="auth-footer">
                Don't have an account?
                <a href="/register">
                    Create one
                </a>
            </p>

        </div>

    </section>

    """

    return HTMLResponse(
        page_template(
            request,
            "Login",
            content
        )
    )


# =========================================================
# LOGIN PROCESS
# =========================================================

@app.post(
    "/login",
    response_class=HTMLResponse
)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    user = check_user(
        username.strip(),
        password
    )

    if user:

        request.session["username"] = (
            user["username"]
        )

        return RedirectResponse(
            "/dashboard",
            status_code=303
        )


    content = """

    <section class="auth-section">

        <div class="auth-card">

            <div class="auth-icon">
                🔐
            </div>

            <span class="eyebrow">
                WELCOME BACK
            </span>

            <h1>
                Login
            </h1>

            <div class="alert error">
                Invalid username or password.
            </div>


            <form
                method="post"
                action="/login"
            >

                <label>
                    Username
                </label>

                <input
                    type="text"
                    name="username"
                    required
                >


                <label>
                    Password
                </label>

                <input
                    type="password"
                    name="password"
                    required
                >


                <button
                    type="submit"
                    class="btn full-btn"
                >
                    Login
                </button>

            </form>

        </div>

    </section>

    """

    return HTMLResponse(
        page_template(
            request,
            "Login",
            content
        )
    )


# =========================================================
# LOGOUT
# =========================================================

@app.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        "/",
        status_code=303
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.get(
    "/dashboard",
    response_class=HTMLResponse
)
async def dashboard(request: Request):

    redirect = login_required(request)

    if redirect:
        return redirect


    username = html.escape(
        str(current_user(request))
    )


    content = f"""

    <section class="dashboard-section">

        <div class="dashboard-header">

            <span class="eyebrow">
                YOUR WORKSPACE
            </span>

            <h1>
                Welcome back,
                <span>{username}</span> 👋
            </h1>

            <p>
                Choose a planner and create
                your personalized budget recommendation.
            </p>

        </div>


        <div class="planner-grid">

            <a
                href="/home-planner"
                class="card planner-card"
            >

                <div class="card-icon">
                    🏠
                </div>

                <h3>
                    Home Planner
                </h3>

                <p>
                    Plan your room, furniture
                    and home requirements.
                </p>

                <span class="card-link">
                    Start planning →
                </span>

            </a>


            <a
                href="/party-planner"
                class="card planner-card"
            >

                <div class="card-icon">
                    🎉
                </div>

                <h3>
                    Party Planner
                </h3>

                <p>
                    Organize your event,
                    food and entertainment.
                </p>

                <span class="card-link">
                    Start planning →
                </span>

            </a>


            <a
                href="/jewelry-planner"
                class="card planner-card"
            >

                <div class="card-icon">
                    💎
                </div>

                <h3>
                    Jewelry Planner
                </h3>

                <p>
                    Find jewelry ideas based
                    on your style and occasion.
                </p>

                <span class="card-link">
                    Start planning →
                </span>

            </a>

        </div>


        <div class="quick-actions">

            <a
                href="/history"
                class="quick-card"
            >
                <span>📜</span>
                <div>
                    <strong>
                        Recommendation History
                    </strong>
                    <small>
                        View your previous plans
                    </small>
                </div>
            </a>


            <a
                href="/recommendations-details"
                class="quick-card"
            >
                <span>🛍️</span>
                <div>
                    <strong>
                        Explore Platforms
                    </strong>
                    <small>
                        Browse useful external platforms
                    </small>
                </div>
            </a>

        </div>

    </section>

    """

    return HTMLResponse(
        page_template(
            request,
            "Dashboard",
            content
        )
    )


# =========================================================
# HOME PLANNER
# =========================================================

@app.get(
    "/home-planner",
    response_class=HTMLResponse
)
async def home_planner(request: Request):

    redirect = login_required(request)

    if redirect:
        return redirect


    content = """

    <section class="form-section">

        <div class="form-header">

            <div class="large-icon">
                🏠
            </div>

            <span class="eyebrow">
                HOME PLANNER
            </span>

            <h1>
                Plan Your Home
            </h1>

            <p>
                Tell us what you need and
                your budget. PocketSmart AI
                will create a practical plan.
            </p>

        </div>


        <div class="form-container">

            <form
                method="post"
                action="/generate-home"
            >

                <label>
                    Room Type
                </label>

                <select
                    name="room_type"
                    required
                >

                    <option value="">
                        Select room
                    </option>

                    <option value="Bedroom">
                        Bedroom
                    </option>

                    <option value="Living Room">
                        Living Room
                    </option>

                    <option value="Study Room">
                        Study Room
                    </option>

                    <option value="Kitchen">
                        Kitchen
                    </option>

                </select>


                <label>
                    Budget
                </label>

                <div class="input-prefix">
                    <span>₹</span>

                    <input
                        type="number"
                        name="budget"
                        min="1"
                        placeholder="Enter your budget"
                        required
                    >
                </div>


                <div class="two-column">

                    <div>

                        <label>
                            Number of Lights
                        </label>

                        <input
                            type="number"
                            name="lights"
                            min="0"
                            value="1"
                        >

                    </div>


                    <div>

                        <label>
                            Number of Fans
                        </label>

                        <input
                            type="number"
                            name="fans"
                            min="0"
                            value="1"
                        >

                    </div>

                </div>


                <label>
                    Number of Tables
                </label>

                <input
                    type="number"
                    name="tables"
                    min="0"
                    value="1"
                >


                <button
                    type="submit"
                    class="btn full-btn"
                >
                    Generate Recommendation ✨
                </button>

            </form>

        </div>

    </section>

    """

    return HTMLResponse(
        page_template(
            request,
            "Home Planner",
            content
        )
    )


# =========================================================
# GENERATE HOME
# =========================================================

@app.post(
    "/generate-home",
    response_class=HTMLResponse
)
async def generate_home(
    request: Request,
    room_type: str = Form(...),
    budget: float = Form(...),
    lights: int = Form(...),
    fans: int = Form(...),
    tables: int = Form(...)
):

    redirect = login_required(request)

    if redirect:
        return redirect


    prompt = f"""
Home planning request.

Room type: {room_type}

Budget: Rs. {budget}

Number of lights: {lights}

Number of fans: {fans}

Number of tables: {tables}

Create a practical and budget-friendly
home recommendation.

Include:
1. Suggested items
2. Approximate budget allocation
3. Priorities
4. Money-saving suggestions
5. Final summary
"""


    recommendation = generate_recommendation(
        prompt
    )


    user_input = (
        f"Room Type: {room_type}\n"
        f"Budget: Rs. {budget}\n"
        f"Lights: {lights}\n"
        f"Fans: {fans}\n"
        f"Tables: {tables}"
    )


    save_history(
        current_user(request),
        "Home Planner",
        user_input,
        recommendation
    )


    content = recommendation_result(
        request,
        "🏠",
        "Home Recommendation",
        recommendation,
        "🛒 Explore Home Platforms"
    )


    return HTMLResponse(
        page_template(
            request,
            "Home Recommendation",
            content
        )
    )


# =========================================================
# PARTY PLANNER
# =========================================================

@app.get(
    "/party-planner",
    response_class=HTMLResponse
)
async def party_planner(request: Request):

    redirect = login_required(request)

    if redirect:
        return redirect


    content = """

    <section class="form-section">

        <div class="form-header">

            <div class="large-icon">
                🎉
            </div>

            <span class="eyebrow">
                PARTY PLANNER
            </span>

            <h1>
                Plan Your Event
            </h1>

            <p>
                Build a complete event plan
                without losing control of your budget.
            </p>

        </div>


        <div class="form-container">

            <form
                method="post"
                action="/generate-party"
            >

                <label>
                    Budget
                </label>

                <div class="input-prefix">

                    <span>₹</span>

                    <input
                        type="number"
                        name="budget"
                        min="1"
                        placeholder="Enter your budget"
                        required
                    >

                </div>


                <label>
                    Number of Guests
                </label>

                <input
                    type="number"
                    name="guests"
                    min="1"
                    placeholder="Example: 50"
                    required
                >


                <label>
                    Event Type
                </label>

                <input
                    type="text"
                    name="event_type"
                    placeholder="Birthday, Wedding, Anniversary..."
                    required
                >


                <label>
                    Venue
                </label>

                <input
                    type="text"
                    name="venue"
                    placeholder="Home, Hall, Hotel..."
                    required
                >


                <label>
                    Food / Catering
                </label>

                <input
                    type="text"
                    name="food"
                    placeholder="Vegetarian, Buffet, Snacks..."
                >


                <label>
                    Decoration
                </label>

                <input
                    type="text"
                    name="decoration"
                    placeholder="Simple, Elegant, Premium..."
                >


                <label>
                    Entertainment
                </label>

                <input
                    type="text"
                    name="entertainment"
                    placeholder="Music, Games, DJ..."
                >


                <button
                    type="submit"
                    class="btn full-btn"
                >
                    Generate Recommendation ✨
                </button>

            </form>

        </div>

    </section>

    """

    return HTMLResponse(
        page_template(
            request,
            "Party Planner",
            content
        )
    )


# =========================================================
# GENERATE PARTY
# =========================================================

@app.post(
    "/generate-party",
    response_class=HTMLResponse
)
async def generate_party(
    request: Request,
    budget: float = Form(...),
    guests: int = Form(...),
    event_type: str = Form(...),
    venue: str = Form(...),
    food: str = Form(""),
    decoration: str = Form(""),
    entertainment: str = Form("")
):

    redirect = login_required(request)

    if redirect:
        return redirect


    prompt = f"""
Party planning request.

Event type: {event_type}

Budget: Rs. {budget}

Number of guests: {guests}

Venue: {venue}

Food/Catering: {food}

Decoration: {decoration}

Entertainment: {entertainment}

Create a practical and budget-friendly
party recommendation.

Include:
1. Budget allocation
2. Food planning
3. Decoration
4. Entertainment
5. Money-saving suggestions
6. Final estimated summary
"""


    recommendation = generate_recommendation(
        prompt
    )


    user_input = (
        f"Budget: Rs. {budget}\n"
        f"Guests: {guests}\n"
        f"Event Type: {event_type}\n"
        f"Venue: {venue}\n"
        f"Food/Catering: {food}\n"
        f"Decoration: {decoration}\n"
        f"Entertainment: {entertainment}"
    )


    save_history(
        current_user(request),
        "Party Planner",
        user_input,
        recommendation
    )


    content = recommendation_result(
        request,
        "🎉",
        "Party Recommendation",
        recommendation,
        "🍽️ Explore Party Platforms"
    )


    return HTMLResponse(
        page_template(
            request,
            "Party Recommendation",
            content
        )
    )


# =========================================================
# JEWELRY PLANNER
# =========================================================

@app.get(
    "/jewelry-planner",
    response_class=HTMLResponse
)
async def jewelry_planner(request: Request):

    redirect = login_required(request)

    if redirect:
        return redirect


    content = """

    <section class="form-section">

        <div class="form-header">

            <div class="large-icon">
                💎
            </div>

            <span class="eyebrow">
                JEWELRY PLANNER
            </span>

            <h1>
                Find Your Jewelry Style
            </h1>

            <p>
                Tell us your budget, occasion
                and preferred style. You can
                also upload an outfit image.
            </p>

        </div>


        <div class="form-container">

            <form
                method="post"
                action="/generate-jewelry"
                enctype="multipart/form-data"
            >

                <label>
                    Budget
                </label>

                <div class="input-prefix">

                    <span>₹</span>

                    <input
                        type="number"
                        name="budget"
                        min="1"
                        placeholder="Enter your budget"
                        required
                    >

                </div>


                <label>
                    Occasion
                </label>

                <select
                    name="occasion"
                    required
                >

                    <option value="">
                        Select occasion
                    </option>

                    <option value="Wedding">
                        Wedding
                    </option>

                    <option value="Birthday">
                        Birthday
                    </option>

                    <option value="Festival">
                        Festival
                    </option>

                    <option value="Party">
                        Party
                    </option>

                    <option value="Casual">
                        Casual
                    </option>

                </select>


                <label>
                    Jewelry Style
                </label>

                <select
                    name="style"
                    required
                >

                    <option value="">
                        Select style
                    </option>

                    <option value="Traditional">
                        Traditional
                    </option>

                    <option value="Modern">
                        Modern
                    </option>

                    <option value="Elegant">
                        Elegant
                    </option>

                    <option value="Minimal">
                        Minimal
                    </option>

                </select>


                <label>
                    Upload Outfit Image
                    <small>
                        Optional
                    </small>
                </label>

                <input
                    type="file"
                    name="outfit_image"
                    id="outfit_image"
                    accept=".jpg,.jpeg,.png,.webp"
                >


                <div
                    id="image-preview-container"
                    class="image-preview-box"
                >

                    <p>
                        Image Preview
                    </p>

                    <img
                        id="image-preview"
                        alt="Outfit preview"
                    >

                </div>


                <button
                    type="submit"
                    class="btn full-btn"
                >
                    Generate Recommendation ✨
                </button>

            </form>

        </div>

    </section>


    <script>

        const imageInput =
            document.getElementById("outfit_image");

        const previewContainer =
            document.getElementById(
                "image-preview-container"
            );

        const preview =
            document.getElementById("image-preview");


        imageInput.addEventListener(
            "change",
            function () {

                const file = this.files[0];

                if (!file) {

                    previewContainer.style.display =
                        "none";

                    return;
                }


                const allowedTypes = [
                    "image/jpeg",
                    "image/png",
                    "image/webp"
                ];


                if (
                    !allowedTypes.includes(
                        file.type
                    )
                ) {

                    alert(
                        "Please select a JPG, PNG or WEBP image."
                    );

                    this.value = "";

                    previewContainer.style.display =
                        "none";

                    return;
                }


                preview.src =
                    URL.createObjectURL(file);

                previewContainer.style.display =
                    "block";
            }
        );

    </script>

    """

    return HTMLResponse(
        page_template(
            request,
            "Jewelry Planner",
            content
        )
    )


# =========================================================
# GENERATE JEWELRY
# =========================================================

@app.post(
    "/generate-jewelry",
    response_class=HTMLResponse
)
async def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form(...),
    outfit_image: UploadFile | None = File(None)
):

    redirect = login_required(request)

    if redirect:
        return redirect


    username = current_user(request)

    saved_filename = None
    image_path = None


    # -----------------------------------------------------
    # SAVE IMAGE
    # -----------------------------------------------------

    if outfit_image and outfit_image.filename:

        extension = os.path.splitext(
            outfit_image.filename
        )[1].lower()


        allowed_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        }


        if extension not in allowed_extensions:

            content = """

            <section class="result-section">

                <div class="result-card">

                    <div class="result-icon">
                        ⚠️
                    </div>

                    <h1>
                        Invalid Image
                    </h1>

                    <p>
                        Please upload a JPG,
                        JPEG, PNG or WEBP image.
                    </p>

                    <a
                        href="/jewelry-planner"
                        class="btn"
                    >
                        Try Again
                    </a>

                </div>

            </section>

            """

            return HTMLResponse(
                page_template(
                    request,
                    "Invalid Image",
                    content
                )
            )


        saved_filename = (
            str(uuid.uuid4())
            + extension
        )


        image_path = os.path.join(
            "uploads",
            saved_filename
        )


        image_bytes = await outfit_image.read()


        with open(
            image_path,
            "wb"
        ) as image_file:

            image_file.write(
                image_bytes
            )


    # -----------------------------------------------------
    # PROMPT
    # -----------------------------------------------------

    prompt = f"""
Jewelry planning request.

Budget: Rs. {budget}

Occasion: {occasion}

Preferred style: {style}

Create a practical jewelry recommendation.

Include:
1. Jewelry types
2. Style suggestions
3. Budget allocation
4. Matching suggestions
5. Practical shopping advice
"""


    # -----------------------------------------------------
    # AI RECOMMENDATION
    # -----------------------------------------------------

    if image_path:

        recommendation = (
            generate_image_recommendation(
                image_path,
                prompt
            )
        )

    else:

        recommendation = (
            generate_recommendation(
                prompt +
                "\nNo outfit image was uploaded."
            )
        )


    # -----------------------------------------------------
    # SAVE HISTORY
    # -----------------------------------------------------

    user_input = (
        f"Budget: Rs. {budget}\n"
        f"Occasion: {occasion}\n"
        f"Style: {style}\n"
    )


    if saved_filename:

        user_input += (
            f"Outfit image uploaded: "
            f"{saved_filename}\n"
        )

    else:

        user_input += (
            "Outfit image uploaded: None\n"
        )


    save_history(
        username,
        "Jewelry Planner",
        user_input,
        recommendation
    )


    # -----------------------------------------------------
    # IMAGE
    # -----------------------------------------------------

    image_html = ""


    if saved_filename:

        safe_filename = html.escape(
            saved_filename
        )

        image_html = f"""

        <div class="uploaded-image-card">

            <div class="uploaded-image-title">
                🖼️ Your Outfit
            </div>

            <img
                src="/uploads/{safe_filename}"
                alt="Uploaded outfit"
                class="result-outfit-image"
            >

        </div>

        """


    # -----------------------------------------------------
    # RESULT
    # -----------------------------------------------------

    content = f"""

    <section class="result-section">

        <div class="result-card">

            <div class="result-top">

                <div class="result-icon">
                    💎
                </div>

                <div>

                    <span class="eyebrow">
                        AI GENERATED
                    </span>

                    <h1>
                        Jewelry Recommendation
                    </h1>

                    <p>
                        Personalized for your
                        budget and preferences.
                    </p>

                </div>

            </div>


            <div class="result-summary">

                <div>
                    <small>Budget</small>
                    <strong>
                        ₹{budget:,.0f}
                    </strong>
                </div>

                <div>
                    <small>Occasion</small>
                    <strong>
                        {html.escape(occasion)}
                    </strong>
                </div>

                <div>
                    <small>Style</small>
                    <strong>
                        {html.escape(style)}
                    </strong>
                </div>

            </div>


            {image_html}


            <div class="recommendation-box">

                <div class="recommendation-heading">
                    ✨ AI Recommendation
                </div>

                <pre>{html.escape(
                    recommendation
                )}</pre>

            </div>


            <div class="result-actions">

                <a
                    href="/recommendations-details"
                    class="btn"
                >
                    💎 Explore Jewelry Platforms
                </a>

                <a
                    href="/dashboard"
                    class="btn secondary-btn"
                >
                    Back to Dashboard
                </a>

            </div>

        </div>

    </section>

    """

    return HTMLResponse(
        page_template(
            request,
            "Jewelry Recommendation",
            content
        )
    )


# =========================================================
# RECOMMENDATION RESULT HELPER
# =========================================================
# =========================================================
# RECOMMENDATION RESULT HELPER
# =========================================================

def recommendation_result(
    request: Request,
    icon: str,
    title: str,
    recommendation: str,
    platform_text: str
):

    safe_title = html.escape(
        str(title)
    )

    safe_recommendation = html.escape(
        str(recommendation)
    )

    return f"""

    <section class="result-section">

        <div class="result-card">

            <!-- =========================================
                 RESULT HEADER
                 ========================================= -->

            <div class="result-top">

                <div class="result-icon">
                    {icon}
                </div>

                <div>

                    <span class="eyebrow">
                        AI GENERATED
                    </span>

                    <h1>
                        {safe_title}
                    </h1>

                    <p>
                        Your personalized
                        PocketSmart AI plan is ready.
                    </p>

                </div>

            </div>


            <!-- =========================================
                 AI RECOMMENDATION
                 ========================================= -->

            <div class="recommendation-box">

                <div class="recommendation-heading">

                    <span>
                        ✨
                    </span>

                    <span>
                        AI Recommendation
                    </span>

                </div>


                <div class="recommendation-content">

                    <pre>{safe_recommendation}</pre>

                </div>

            </div>


            <!-- =========================================
                 QUICK INFORMATION
                 ========================================= -->

            <div class="result-info-grid">

                <div class="result-info-card">

                    <div class="result-info-icon">
                        🤖
                    </div>

                    <div>

                        <strong>
                            AI Powered
                        </strong>

                        <span>
                            Personalized recommendation
                        </span>

                    </div>

                </div>


                <div class="result-info-card">

                    <div class="result-info-icon">
                        💰
                    </div>

                    <div>

                        <strong>
                            Budget Focused
                        </strong>

                        <span>
                            Planned around your budget
                        </span>

                    </div>

                </div>


                <div class="result-info-card">

                    <div class="result-info-icon">
                        💡
                    </div>

                    <div>

                        <strong>
                            Practical Tips
                        </strong>

                        <span>
                            Designed to help save money
                        </span>

                    </div>

                </div>

            </div>


            <!-- =========================================
                 ACTIONS
                 ========================================= -->

            <div class="result-actions">

                <a
                    href="/recommendations-details"
                    class="btn"
                >
                    {platform_text}
                </a>


                <a
                    href="/history"
                    class="btn secondary-btn"
                >
                    📜 View History
                </a>


                <a
                    href="/dashboard"
                    class="btn secondary-btn"
                >
                    ← Dashboard
                </a>

            </div>


            <!-- =========================================
                 DISCLAIMER
                 ========================================= -->

            <div class="result-note">

                <span>
                    ℹ️
                </span>

                <p>
                    Recommendations and estimated
                    prices are generated for planning
                    purposes. Actual prices,
                    availability and offers may vary.
                </p>

            </div>

        </div>

    </section>

    """


    return f"""

    <section class="result-section">

        <div class="result-card">

            <div class="result-top">

                <div class="result-icon">
                    {icon}
                </div>

                <div>

                    <span class="eyebrow">
                        AI GENERATED
                    </span>

                    <h1>
                        {html.escape(title)}
                    </h1>

                    <p>
                        Your personalized
                        PocketSmart AI plan is ready.
                    </p>

                </div>

            </div>


            <div class="recommendation-box">

                <div class="recommendation-heading">
                    ✨ AI Recommendation
                </div>

                <pre>{html.escape(
                    recommendation
                )}</pre>

            </div>


            <div class="result-actions">

                <a
                    href="/recommendations-details"
                    class="btn"
                >
                    {platform_text}
                </a>

                <a
                    href="/dashboard"
                    class="btn secondary-btn"
                >
                    Back to Dashboard
                </a>

            </div>

        </div>

    </section>

    """


# =========================================================
# HISTORY
# =========================================================

@app.get(
    "/history",
    response_class=HTMLResponse
)
async def history(request: Request):

    redirect = login_required(request)

    if redirect:
        return redirect


    username = current_user(request)

    history_items = get_history(
        username
    )


    cards = ""


    if not history_items:

        cards = """

        <div class="empty-state">

            <div class="empty-icon">
                📜
            </div>

            <h2>
                No History Yet
            </h2>

            <p>
                Create your first recommendation
                and it will appear here.
            </p>

            <a
                href="/dashboard"
                class="btn"
            >
                Create Recommendation
            </a>

        </div>

        """


    else:

        for item in history_items:

            user_input = item["user_input"]
            recommendation = item["recommendation"]
            planner_type = item["planner_type"]
            created_at = item["created_at"]


            image_filename = None

            marker = "Outfit image uploaded:"


            if marker in user_input:

                image_value = (
                    user_input
                    .split(marker, 1)[1]
                    .strip()
                )

                if image_value:

                    image_filename = (
                        image_value.split()[0]
                    )


            image_html = ""


            if (
                image_filename
                and image_filename.lower()
                != "none"
            ):

                safe_filename = html.escape(
                    image_filename
                )

                image_html = f"""

                <div class="history-image">

                    <h4>
                        🖼️ Outfit Image
                    </h4>

                    <img
                        src="/uploads/{safe_filename}"
                        alt="Outfit image"
                    >

                </div>

                """


            cards += f"""

            <article class="history-card">

                <div class="history-card-header">

                    <div>

                        <span class="eyebrow">
                            SAVED PLAN
                        </span>

                        <h2>
                            {html.escape(
                                planner_type
                            )}
                        </h2>

                    </div>

                    <span class="history-date">
                        {html.escape(
                            str(created_at)
                        )}
                    </span>

                </div>


                <div class="history-input">

                    <h4>
                        Your Input
                    </h4>

                    <pre>{html.escape(
                        user_input
                    )}</pre>

                </div>


                {image_html}


                <div class="history-recommendation">

                    <h4>
                        ✨ AI Recommendation
                    </h4>

                    <pre>{html.escape(
                        recommendation
                    )}</pre>

                </div>

            </article>

            """


    content = f"""

    <section class="section">

        <div class="section-heading">

            <span class="eyebrow">
                YOUR RECORDS
            </span>

            <h1 class="section-title">
                Recommendation History
            </h1>

            <p>
                Review your previous PocketSmart
                AI planning sessions.
            </p>

        </div>


        <div class="history-list">

            {cards}

        </div>

    </section>

    """


    return HTMLResponse(
        page_template(
            request,
            "History",
            content
        )
    )


# =========================================================
# RECOMMENDATION DETAILS
# =========================================================

@app.get(
    "/recommendations-details",
    response_class=HTMLResponse
)
async def recommendations_details(
    request: Request
):

    redirect = login_required(request)

    if redirect:
        return redirect


    content = """

    <section class="section">

        <div class="section-heading">

            <span class="eyebrow">
                EXPLORE
            </span>

            <h1 class="section-title">
                Recommended Platforms
            </h1>

            <p>
                Explore external platforms that
                may help you continue your planning.
            </p>

        </div>


        <!-- HOME -->

        <div class="platform-section">

            <div class="platform-section-header">

                <div class="platform-section-icon">
                    🏠
                </div>

                <div>

                    <h2>
                        Home & Shopping
                    </h2>

                    <p>
                        Products and furniture
                        for your home.
                    </p>

                </div>

            </div>


            <div class="platform-grid">

                <a
                    href="https://www.amazon.in/"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="platform-card"
                >

                    <div class="platform-logo amazon">
                        A
                    </div>

                    <div class="platform-info">

                        <strong>
                            Amazon
                        </strong>

                        <span>
                            Shopping & products
                        </span>

                    </div>

                    <span class="external-icon">
                        ↗
                    </span>

                </a>


                <a
                    href="https://www.ikea.com/in/en/"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="platform-card"
                >

                    <div class="platform-logo ikea">
                        I
                    </div>

                    <div class="platform-info">

                        <strong>
                            IKEA
                        </strong>

                        <span>
                            Furniture & home
                        </span>

                    </div>

                    <span class="external-icon">
                        ↗
                    </span>

                </a>


                <a
                    href="https://www.flipkart.com/"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="platform-card"
                >

                    <div class="platform-logo flipkart">
                        F
                    </div>

                    <div class="platform-info">

                        <strong>
                            Flipkart
                        </strong>

                        <span>
                            Online shopping
                        </span>

                    </div>

                    <span class="external-icon">
                        ↗
                    </span>

                </a>

            </div>

        </div>


        <!-- PARTY -->

        <div class="platform-section">

            <div class="platform-section-header">

                <div class="platform-section-icon">
                    🎉
                </div>

                <div>

                    <h2>
                        Party & Food
                    </h2>

                    <p>
                        Food, delivery and
                        event-related services.
                    </p>

                </div>

            </div>


            <div class="platform-grid">

                <a
                    href="https://www.swiggy.com/"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="platform-card"
                >

                    <div class="platform-logo swiggy">
                        S
                    </div>

                    <div class="platform-info">

                        <strong>
                            Swiggy
                        </strong>

                        <span>
                            Food & delivery
                        </span>

                    </div>

                    <span class="external-icon">
                        ↗
                    </span>

                </a>


                <a
                    href="https://www.zomato.com/"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="platform-card"
                >

                    <div class="platform-logo zomato">
                        Z
                    </div>

                    <div class="platform-info">

                        <strong>
                            Zomato
                        </strong>

                        <span>
                            Food & restaurants
                        </span>

                    </div>

                    <span class="external-icon">
                        ↗
                    </span>

                </a>


                <a
                    href="https://www.oyorooms.com/"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="platform-card"
                >

                    <div class="platform-logo oyo">
                        O
                    </div>

                    <div class="platform-info">

                        <strong>
                            OYO
                        </strong>

                        <span>
                            Hotels & stays
                        </span>

                    </div>

                    <span class="external-icon">
                        ↗
                    </span>

                </a>

            </div>

        </div>


        <!-- JEWELRY -->

        <div class="platform-section">

            <div class="platform-section-header">

                <div class="platform-section-icon">
                    💎
                </div>

                <div>

                    <h2>
                        Jewelry
                    </h2>

                    <p>
                        Explore jewelry collections
                        and styles.
                    </p>

                </div>

            </div>


            <div class="platform-grid">

                <a
                    href="https://www.tanishq.co.in/"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="platform-card"
                >

                    <div class="platform-logo tanishq">
                        T
                    </div>

                    <div class="platform-info">

                        <strong>
                            Tanishq
                        </strong>

                        <span>
                            Jewelry collections
                        </span>

                    </div>

                    <span class="external-icon">
                        ↗
                    </span>

                </a>


                <a
                    href="https://www.caratlane.com/"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="platform-card"
                >

                    <div class="platform-logo caratlane">
                        C
                    </div>

                    <div class="platform-info">

                        <strong>
                            CaratLane
                        </strong>

                        <span>
                            Jewelry & diamonds
                        </span>

                    </div>

                    <span class="external-icon">
                        ↗
                    </span>

                </a>


                <a
                    href="https://www.bluestone.com/"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="platform-card"
                >

                    <div class="platform-logo bluestone">
                        B
                    </div>

                    <div class="platform-info">

                        <strong>
                            BlueStone
                        </strong>

                        <span>
                            Online jewelry
                        </span>

                    </div>

                    <span class="external-icon">
                        ↗
                    </span>

                </a>

            </div>

        </div>


        <div class="notice-card">

            <div class="notice-icon">
                ℹ️
            </div>

            <div>

                <h3>
                    Important
                </h3>

                <p>
                    PocketSmart AI provides
                    recommendations and platform
                    suggestions. Product prices,
                    availability and offers may
                    change on external websites.
                </p>

            </div>

        </div>

    </section>

    """


    return HTMLResponse(
        page_template(
            request,
            "Recommendations",
            content
        )
    )


# =========================================================
# HOW IT WORKS
# =========================================================

@app.get(
    "/how-it-works",
    response_class=HTMLResponse
)
async def how_it_works(request: Request):

    content = """

    <section class="section">

        <div class="section-heading">

            <span class="eyebrow">
                SIMPLE PROCESS
            </span>

            <h1 class="section-title">
                How PocketSmart AI Works
            </h1>

            <p>
                Create a plan in a few simple steps.
            </p>

        </div>


        <div class="steps-grid">


            <div class="step-card">

                <div class="step-number">
                    01
                </div>

                <div class="card-icon">
                    👤
                </div>

                <h3>
                    Create an Account
                </h3>

                <p>
                    Register and log in to
                    access your personal
                    planning workspace.
                </p>

            </div>


            <div class="step-card">

                <div class="step-number">
                    02
                </div>

                <div class="card-icon">
                    🎯
                </div>

                <h3>
                    Choose a Planner
                </h3>

                <p>
                    Select Home, Party or
                    Jewelry Planner depending
                    on what you want to plan.
                </p>

            </div>


            <div class="step-card">

                <div class="step-number">
                    03
                </div>

                <div class="card-icon">
                    💰
                </div>

                <h3>
                    Enter Your Budget
                </h3>

                <p>
                    Tell PocketSmart AI how
                    much you want to spend
                    and provide your preferences.
                </p>

            </div>


            <div class="step-card">

                <div class="step-number">
                    04
                </div>

                <div class="card-icon">
                    🤖
                </div>

                <h3>
                    Generate Recommendation
                </h3>

                <p>
                    The AI recommendation
                    engine creates a plan
                    based on your inputs.
                </p>

            </div>


            <div class="step-card">

                <div class="step-number">
                    05
                </div>

                <div class="card-icon">
                    🛍️
                </div>

                <h3>
                    Explore Platforms
                </h3>

                <p>
                    Continue your planning by
                    exploring relevant external
                    platforms.
                </p>

            </div>


            <div class="step-card">

                <div class="step-number">
                    06
                </div>

                <div class="card-icon">
                    📜
                </div>

                <h3>
                    View History
                </h3>

                <p>
                    Your previous recommendations
                    remain available through
                    your History page.
                </p>

            </div>

        </div>


        <div class="ai-info-card">

            <div class="ai-info-icon">
                🤖
            </div>

            <div>

                <span class="eyebrow">
                    AI SYSTEM
                </span>

                <h2>
                    Personalized Recommendations
                </h2>

                <p>
                    PocketSmart AI uses the
                    information you provide to
                    generate recommendations
                    focused on your budget and
                    preferences.
                </p>

            </div>

        </div>

    </section>

    """


    return HTMLResponse(
        page_template(
            request,
            "How It Works",
            content
        )
    )


# =========================================================
# SESSION INFO
# =========================================================

@app.get(
    "/session-info",
    response_class=HTMLResponse
)
async def session_info(request: Request):

    redirect = login_required(request)

    if redirect:
        return redirect


    username = html.escape(
        str(current_user(request))
    )


    content = f"""

    <section class="section">

        <div class="simple-card">

            <h1>
                Session Information
            </h1>

            <p>
                Logged in as:
                <strong>
                    {username}
                </strong>
            </p>

        </div>

    </section>

    """


    return HTMLResponse(
        page_template(
            request,
            "Session Information",
            content
        )
    )


# =========================================================
# SESSION DATA
# =========================================================

@app.get(
    "/session-data",
    response_class=HTMLResponse
)
async def session_data(request: Request):

    redirect = login_required(request)

    if redirect:
        return redirect


    username = html.escape(
        str(current_user(request))
    )


    content = f"""

    <section class="section">

        <div class="simple-card">

            <h1>
                Session Data
            </h1>

            <p>
                Username:
                <strong>
                    {username}
                </strong>
            </p>

        </div>

    </section>

    """


    return HTMLResponse(
        page_template(
            request,
            "Session Data",
            content
        )
    )


# =========================================================
# TOKEN
# =========================================================

@app.get(
    "/token",
    response_class=HTMLResponse
)
async def token(request: Request):

    redirect = login_required(request)

    if redirect:
        return redirect


    content = """

    <section class="section">

        <div class="simple-card">

            <h1>
                Authentication
            </h1>

            <p>
                Session authentication is active.
            </p>

        </div>

    </section>

    """


    return HTMLResponse(
        page_template(
            request,
            "Authentication",
            content
        )
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get(
    "/health",
    response_class=HTMLResponse
)
async def health():

    return HTMLResponse(
        """
        <h2>
            PocketSmart AI is running successfully.
        </h2>
        """
    )