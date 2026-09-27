import os
import time
import mimetypes

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================
# GEMINI CLIENT
# ============================================================

client = None

if API_KEY:
    try:
        client = genai.Client(
            api_key=API_KEY
        )
    except Exception:
        client = None


# ============================================================
# SETTINGS
# ============================================================

USE_GEMINI = False

MODEL_NAME = "gemini-3.8-flash"


# ============================================================
# DEMO RECOMMENDATION
# ============================================================

def demo_recommendation(prompt):

    text = str(prompt).lower()


    # ========================================================
    # HOME
    # ========================================================

    if "room type" in text or "home" in text:

        return """
POCKETSMART AI
==============================

🏠 HOME BUDGET PLAN

RECOMMENDED ITEMS
------------------------------

1. LED Lights
   Estimated Cost: ₹1,500
   Priority: High

2. Ceiling Fan
   Estimated Cost: ₹2,500
   Priority: High

3. Study / Side Table
   Estimated Cost: ₹3,000
   Priority: Medium

4. Curtains
   Estimated Cost: ₹2,000
   Priority: Medium

5. Wall Decoration
   Estimated Cost: ₹1,500
   Priority: Low


💰 BUDGET ALLOCATION
------------------------------

Essential Items: ₹4,000
Furniture: ₹3,000
Decoration: ₹3,500

Estimated Total: ₹10,500


💡 MONEY-SAVING TIPS
------------------------------

• Prioritize essential items first.
• Compare prices from multiple sellers.
• Choose energy-efficient products.
• Avoid unnecessary decorative purchases.
• Keep some money as an emergency reserve.


🛍️ SHOPPING IDEAS
------------------------------

• Amazon
• IKEA
• Flipkart


📝 FINAL SUMMARY
------------------------------

Start with essential items and gradually
add decorative items according to the
remaining budget.

NOTE:
Prices are sample estimates and may vary.
"""


    # ========================================================
    # PARTY
    # ========================================================

    if "event type" in text or "party" in text:

        return """
POCKETSMART AI
==============================

🎉 PARTY BUDGET PLAN


🍽️ FOOD / CATERING
------------------------------

Suggested allocation:
₹2,000 - ₹5,000

Priority: High

Suggestions:
• Simple buffet
• Local catering
• Compare catering packages
• Choose a menu based on guest count


🎈 DECORATION
------------------------------

Suggested allocation:
₹1,000 - ₹3,000

Priority: Medium

Suggestions:
• Balloons
• Simple backdrop
• Table decoration
• LED decorative lights


🎵 ENTERTAINMENT
------------------------------

Suggested allocation:
₹1,000 - ₹3,000

Priority: Medium

Suggestions:
• Music playlist
• Simple games
• Speaker setup


💰 BUDGET STRATEGY
------------------------------

1. Calculate food cost first.
2. Keep decoration simple.
3. Consider DIY decorations.
4. Avoid unnecessary entertainment expenses.
5. Keep an emergency amount.


💡 MONEY-SAVING TIPS
------------------------------

• Compare local catering services.
• Buy decorations in reusable sets.
• Use existing speakers when possible.
• Plan the guest list carefully.


📝 FINAL SUMMARY
------------------------------

Food should receive the highest priority,
followed by decoration and entertainment.

NOTE:
Prices are sample estimates and may vary.
"""


    # ========================================================
    # JEWELRY
    # ========================================================

    if (
        "jewelry" in text
        or "jewellery" in text
    ):

        return """
POCKETSMART AI
==============================

💎 JEWELRY PLAN


✨ JEWELRY IDEAS
------------------------------

• Necklace
• Earrings
• Bracelet
• Ring
• Pendant


👗 STYLE SUGGESTIONS
------------------------------

TRADITIONAL
• Jhumka-style earrings
• Traditional necklace
• Classic bangles

MODERN
• Minimal pendant
• Geometric earrings
• Simple bracelet

ELEGANT
• Lightweight necklace
• Matching earrings
• Simple ring


💰 BUDGET STRATEGY
------------------------------

Necklace: 40%
Earrings: 25%
Bracelet: 15%
Ring / Pendant: 20%


💡 SHOPPING TIPS
------------------------------

• Compare multiple sellers.
• Check material and purity information.
• Check making charges.
• Check taxes and additional fees.
• Consider lightweight designs.
• Verify return and exchange policies.


📝 FINAL SUMMARY
------------------------------

Choose jewelry according to the occasion,
style preference and available budget.

IMAGE ANALYSIS
------------------------------

Demo mode does not analyze uploaded images.

The image upload and preview can still work.

NOTE:
Jewelry prices can vary depending on
material, weight, purity, making charges
and taxes.
"""


    # ========================================================
    # DEFAULT
    # ========================================================

    return """
POCKETSMART AI
==============================

DEMO RECOMMENDATION

Your request has been received.

The demo recommendation system is currently
being used.

Enable Gemini AI to receive a personalized
AI-generated recommendation.
"""


# ============================================================
# REAL GEMINI TEXT RECOMMENDATION
# ============================================================

def gemini_recommendation(prompt):

    if client is None:

        return """
GEMINI AI ERROR
==============================

Gemini AI is not configured.

Please check your .env file and make sure
GEMINI_API_KEY is present.

The application itself is still running.
"""


    try:

        full_prompt = f"""
You are PocketSmart AI, a smart budget planning
and recommendation assistant.

Your job is to create practical recommendations
based strictly on the user's provided information.

USER REQUEST
============

{prompt}


IMPORTANT RULES
===============

1. Respect the user's stated budget.
2. Do not invent exact product prices.
3. Use approximate prices only when useful.
4. Clearly label prices as estimates.
5. Prioritize essential items before optional items.
6. Avoid recommending unnecessary purchases.
7. Give realistic money-saving suggestions.
8. Keep the recommendation easy for a normal user
   to understand.
9. Do not claim that prices are guaranteed.
10. If information is missing, make a reasonable
    general suggestion and clearly indicate it.


OUTPUT FORMAT
=============

POCKETSMART AI
Budget Recommendation
------------------------------

🎯 PLAN OVERVIEW

Give a short explanation of the recommended plan.

🛍️ RECOMMENDED ITEMS

For each important item include:

• Item
• Purpose
• Estimated cost or cost range
• Priority

💰 BUDGET BREAKDOWN

Show how the available budget can be divided.

Example:

Essential items: ₹____
Optional items: ₹____
Reserve: ₹____
Estimated total: ₹____

💡 MONEY-SAVING TIPS

Give 3-5 practical suggestions.

⚠️ IMPORTANT CONSIDERATIONS

Mention anything the user should check before
spending money.

📝 FINAL SUMMARY

Give a short final recommendation.

Keep the response organized and readable.
"""


        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=full_prompt
        )


        if response is None:

            return "Gemini returned an empty response."


        result = getattr(
            response,
            "text",
            None
        )


        if result:

            return result


        return "Gemini returned no text response."


    except Exception as error:

        error_text = str(error)


        # ====================================================
        # RATE LIMIT
        # ====================================================

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            return """
GEMINI AI TEMPORARILY UNAVAILABLE
=================================

The Gemini API request limit has
been reached.

Please try again later.

PocketSmart AI can continue using
demo recommendations.
"""


        # ====================================================
        # TEMPORARY SERVER ERROR
        # ====================================================

        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
        ):

            for attempt in range(2):

                try:

                    time.sleep(2)


                    response = (
                        client.models.generate_content(
                            model=MODEL_NAME,
                            contents=full_prompt
                        )
                    )


                    result = getattr(
                        response,
                        "text",
                        None
                    )


                    if result:

                        return result


                except Exception:

                    continue


            return """
GEMINI AI TEMPORARILY BUSY
===========================

Gemini AI is temporarily unavailable.

Please try again in a moment.
"""


        # ====================================================
        # OTHER ERROR
        # ====================================================

        return f"""
GEMINI AI SERVICE ERROR
=======================

PocketSmart AI could not complete
the Gemini request.

The application is still running.

Error:
{error_text}
"""


# ============================================================
# REAL GEMINI IMAGE ANALYSIS
# ============================================================

def gemini_image_recommendation(
    image_path,
    prompt
):

    if client is None:

        return """
GEMINI IMAGE AI ERROR
=====================

Gemini AI is not configured.

Please check your GEMINI_API_KEY
in the .env file.
"""


    try:

        if not image_path:

            return "No image was provided."


        if not os.path.exists(image_path):

            return f"""
IMAGE ERROR
===========

The uploaded image could not be found.

Path:
{image_path}
"""


        # ====================================================
        # DETECT IMAGE TYPE
        # ====================================================

        mime_type, _ = mimetypes.guess_type(
            image_path
        )


        if not mime_type:

            mime_type = "image/jpeg"


        # ====================================================
        # READ IMAGE
        # ====================================================

        with open(
            image_path,
            "rb"
        ) as image_file:

            image_bytes = image_file.read()


        # ====================================================
        # CREATE IMAGE PART
        # ====================================================

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )


        # ====================================================
        # IMAGE AI PROMPT
        # ====================================================

        full_prompt = f"""
You are PocketSmart AI, a budget and
jewelry recommendation assistant.

Analyze the uploaded outfit image.

USER REQUIREMENTS
=================

{prompt}


IMPORTANT PRIVACY RULES
=======================

Analyze only the visible clothing,
outfit and fashion details.

Do NOT identify the person.

Do NOT infer personal identity,
age, religion, ethnicity or other
sensitive personal information.


ANALYSIS
========

Describe only details that are reasonably
visible in the image.

If something cannot be determined,
say that clearly instead of guessing.


OUTPUT FORMAT
=============

💎 JEWELRY RECOMMENDATION
------------------------------

👗 OUTFIT OBSERVATION

• Main visible color
• Outfit style
• Visible patterns or design
• Overall fashion style


✨ JEWELRY STYLE

Recommend suitable jewelry based on
the visible outfit.


📿 NECKLACE

Give suitable necklace types and explain why.


👂 EARRINGS

Give suitable earring styles and explain why.


💫 BRACELET

Give suitable bracelet or bangle styles.


💍 RING

Give suitable ring styles.


🌸 TRADITIONAL OR MODERN

Explain whether traditional, modern,
minimal or mixed styles may work well.


💰 BUDGET OPTIONS

Give budget-friendly choices.

Do not claim exact prices.
Use approximate ranges when appropriate.


🛍️ SHOPPING CONSIDERATIONS

Mention useful things to check before buying,
such as material, quality, size, making charges,
taxes or return policies when relevant.


📝 FINAL SUMMARY

Give a short practical recommendation.

Mention that prices are estimates and
may vary.
"""


        # ====================================================
        # GEMINI MULTIMODAL REQUEST
        # ====================================================

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                image_part,
                full_prompt
            ]
        )


        if response is None:

            return (
                "Gemini returned an empty "
                "image-analysis response."
            )


        result = getattr(
            response,
            "text",
            None
        )


        if result:

            return result


        return (
            "Gemini could not generate "
            "an image-analysis response."
        )


    except Exception as error:

        error_text = str(error)


        # ====================================================
        # RATE LIMIT
        # ====================================================

        if (
            "429" in error_text
            or "RESOURCE_EXHAUSTED" in error_text
            or "quota" in error_text.lower()
        ):

            return """
GEMINI IMAGE AI TEMPORARILY UNAVAILABLE
========================================

The Gemini API request limit has
been reached.

The image was uploaded successfully,
but AI analysis cannot be completed
right now.

Please try again later.
"""


        # ====================================================
        # TEMPORARY SERVER ERROR
        # ====================================================

        if (
            "503" in error_text
            or "UNAVAILABLE" in error_text
        ):

            return """
GEMINI IMAGE AI TEMPORARILY BUSY
================================

Gemini is temporarily unavailable.

Please try the image analysis again
in a moment.
"""


        # ====================================================
        # OTHER ERROR
        # ====================================================

        return f"""
IMAGE AI ANALYSIS ERROR
=======================

The image was uploaded, but Gemini
could not analyze it.

Error:
{error_text}
"""


# ============================================================
# MAIN TEXT RECOMMENDATION FUNCTION
# ============================================================

def generate_recommendation(prompt):

    if USE_GEMINI and client is not None:

        return gemini_recommendation(
            prompt
        )

    return demo_recommendation(
        prompt
    )


# ============================================================
# MAIN IMAGE RECOMMENDATION FUNCTION
# ============================================================

def generate_image_recommendation(
    image_path,
    prompt
):

    if USE_GEMINI and client is not None:

        return gemini_image_recommendation(
            image_path,
            prompt
        )

    return demo_recommendation(
        prompt
    )
