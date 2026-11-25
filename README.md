# AI Customer Feedback Analyzer

## Project Overview

AI Customer Feedback Analyzer is an AI-powered web application that helps businesses understand and analyze customer feedback.

The application uses Google's Gemini AI to analyze customer reviews, identify sentiment, extract positive and negative feedback, generate summaries, and suggest improvements.

It supports both individual review analysis and bulk review uploads through CSV files. All analyzed reviews are stored in a database and displayed through an analytics dashboard.

## Key Features

- **Single Review Analysis:** Analyze individual customer reviews using Gemini AI.
- **Bulk CSV Upload:** Upload multiple customer reviews using a CSV file.
- **Sentiment Analysis:** Classify reviews as Positive, Negative, or Neutral.
- **Feedback Extraction:** Identify positive points, negative points, and important topics.
- **AI-Generated Summaries:** Generate short summaries of customer feedback.
- **Improvement Suggestions:** Get practical recommendations based on customer reviews.
- **Analytics Dashboard:** View customer sentiment statistics and feedback insights.
- **Database Storage:** Store and retrieve analyzed customer reviews.
- **AI Business Insights:** Generate summaries of common complaints, business strengths, and recommendations.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| FastAPI | Backend application and REST API development |
| PostgreSQL | Store customer reviews and analysis results |
| SQLAlchemy | Database operations and ORM |
| Pandas | CSV file processing and bulk review handling |
| Google Gemini API | AI-powered customer feedback analysis |
| HTML | Dashboard structure |
| CSS | Dashboard styling |
| JavaScript | Frontend interactions and API communication |

## Application Workflow

1. The user submits an individual customer review or uploads a CSV file.
2. FastAPI receives and validates the submitted data.
3. The application sends the review text to Google's Gemini API.
4. Gemini analyzes the review and returns structured JSON results.
5. The application processes the AI response and stores the analysis in PostgreSQL.
6. The dashboard retrieves stored reviews and displays analytics.
7. Users can generate AI-powered business insights from collected feedback.

## Project Objective

The main objective of this project is to demonstrate how Python, REST APIs, databases, data processing, and Generative AI can be combined to build a practical business application that converts unstructured customer feedback into meaningful business insights.