#  Smart Travel Planner – Machine Learning Project

##  Project Overview

The **Smart Travel Planner** is a machine learning-based web application designed to help users plan their trips based on their budget, travel duration, number of travellers, travel type, and destination preferences.

The application recommends suitable travel destinations and helps users organize their trips with estimated expenses, accommodation requirements, weather information, and travel itineraries.

It aims to make travel planning easier, smarter, and more convenient through data analysis and machine learning techniques.

##  Project Objectives

- Recommend suitable travel destinations based on user preferences.
- Analyze travel budgets and estimated trip expenses.
- Suggest destinations according to travel type.
- Provide weather information for selected destinations.
- Generate personalized trip packages.
- Help users manage their travel expenses effectively.

##  Key Features

### 1. Destination Recommendations
- Personalized destination recommendations.
- Budget-based destination filtering.
- Travel duration and preference-based suggestions.
- Supports Solo, Couple, Family, and Friends travel types.
- India and Worldwide destination options.

### 2. My Trip Package
- Selected destination details.
- Estimated travel expenses.
- Accommodation suggestions.
- Food and transportation budgets.
- Local sightseeing and activities.
- Daily travel itinerary.
- Live weather information and travel advice.

### 3. Budget Planner
- Total estimated trip cost.
- Accommodation budget.
- Food expenses.
- Transportation expenses.
- Activities and sightseeing expenses.
- Emergency expense allocation.
- Per-person cost calculation.

### 4. Weather Information
- Fetches current weather information using the Open-Meteo API.
- Displays temperature, wind speed, and rainfall probability.
- Provides simple weather-based travel advice.

##  Machine Learning Approach

The project uses **TF-IDF Vectorization and Cosine Similarity** to recommend destinations based on user preferences.

### Machine Learning Techniques

- **TF-IDF Vectorization:** Converts destination descriptions and related features into numerical representations.
- **Cosine Similarity:** Measures the similarity between user preferences and available destinations.
- **Recommendation Scoring:** Combines similarity, category matching, and travel-type matching to rank destinations.

### Recommendation Factors

- Destination category
- Travel type
- User preferences
- Available budget
- Number of travel days

##  Technologies Used

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Data Analysis | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Recommendation Technique | TF-IDF, Cosine Similarity |
| Data Visualization | Matplotlib |
| API Integration | Open-Meteo API |
| Data Storage | CSV |
| Development Environment | VS Code |

##  Project Structure

```text
smart_travel_planner/
│
├── app/
│   └── app.py
│
├── data/
│   └── destinations_cleaned.csv
│
├── src/
│   ├── live_data.py
│   ├── recommendation_model.py
│   └── trip_planner.py
│
├── data_preprocessing.py
│
├── requirements.txt
│
└── README.md
```

##  Installation and Setup

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### Step 2: Navigate to the Project Folder

```bash
cd smart_travel_planner
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### Step 5: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 6: Run the Application

```bash
streamlit run app/app.py
```

The application will open in your default web browser.

##  API Integration

The project integrates the **Open-Meteo API** to retrieve live weather information for selected destinations.

Weather information includes:
- Current temperature
- Wind speed
- Rainfall probability
- Weather-based travel suggestions

**Note:** Weather information is fetched live through the API. Destination recommendations, estimated prices, and budget calculations are based on the available dataset and application logic.

##  Dataset

The project uses a destination dataset containing information such as:

- Destination name
- State
- Category
- Ideal travel type
- Estimated daily budget
- Minimum travel days
- Best travel season
- Destination description

The dataset is cleaned and preprocessed before being used in the recommendation system.

##  Future Enhancements

- Integration with real-time hotel and flight booking platforms.
- More comprehensive international destination datasets.
- Advanced recommendation algorithms.
- Interactive maps and destination visualization.
- Real-time transportation price estimation.
- User accounts and saved travel plans.

##  Developed By

**Fathima Rana**

Data Analyst Trainee | Machine Learning Enthusiast

**Project:** Smart Travel Planner

---

 If you find this project interesting, feel free to explore the repository!
