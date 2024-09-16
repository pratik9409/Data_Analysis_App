# Data Analysis App 📊



Welcome to the **SaaS Analytics Platform**! This platform offers robust data analysis features, visualization tools, and subscription management through **Stripe** for advanced users. Built using **Streamlit**, this platform integrates multiple APIs such as **OpenAI** and **spaCy** for enhanced user experience. 


https://github.com/user-attachments/assets/3dd29dbd-c55b-4f0b-9831-82dcbecf1647


## Features

- **Authentication**: Secure login and signup with Firebase authentication.
- **Subscription Plans**: Manage user subscriptions via Stripe. Users can choose between Free and Premium plans.
- **Data Upload & Analysis**: 
  - Upload CSV, Excel, or image files for analysis.
  - Preview datasets, describe statistical summaries, and analyze data through group-by operations.
  - Visualize data using various plots such as bar, line, pie, and scatter plots.
- **Natural Language Processing (NLP)**: 
  - Named Entity Recognition (NER) using **spaCy**.
- **LLM Integration**: Query the platform using **OpenAI's GPT-4** for advanced analysis.
- **Premium Features**: Premium users gain access to advanced analytics such as correlation matrices, distribution plots, and additional visualization options.

## Getting Started

### Prerequisites

- Python 3.9+
- Firebase account for authentication
- Stripe account for subscription management
- OpenAI API Key
- Docker (optional, for containerization)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/saas-analytics-platform.git
   cd saas-analytics-platform
2. **Install dependencies: Ensure you have the required dependencies listed in requirements.txt.**
   ```bash
   pip install -r requirements.txt
3. **Set environment variables: Set up your API keys and configuration:**
    * OPENAI_API_KEY
    * STRIPE_API_KEY
    * FIREBASE_API_KEY
4. **Run the application:**
   ```bash
   streamlit run app.py

## Usage
1. **Login or Sign Up:** Create an account or log in using your email and password.
2. **Upload Data:** Upload a CSV, Excel, or image file to begin analyzing your data.
3. **Subscription Management:** Free users can upgrade to a Premium plan for access to advanced features.
4. **Data Analysis & Visualization:**
   * View dataset summaries, count values in specific columns, and group data using custom operations.
   * Generate visualizations such as bar charts, pie charts, scatter plots, etc.
5. **LLM Integration:** Premium users can ask questions to the LLM for data insights and NLP tasks.

## Future Improvements
* **Real-time Data Analysis:** Enable real-time streaming data analytics for continuous monitoring.
* **Advanced AI Capabilities:** Integrate sentiment analysis, text summarization, and language translation using OpenAI and spaCy.
* **User Dashboard:** Create personalized dashboards for users to save analysis and access history.
* **Custom Visualization:** Allow users to customize plots with themes, color schemes, and annotations.
* **Collaboration Features:** Implement a feature for users to share datasets and analyses with other users securely.
* **Enhanced Security:** Add two-factor authentication (2FA) for user accounts.
* **Data Export:** Enable exporting of processed data and visualizations in various formats (CSV, PDF, PNG).
* **Multi-language Support:** Add multi-language support for international users.
* **Auto-Scaling for Large Datasets:** Improve performance for handling large datasets through batch processing and distributed computation.
