# Student Performance Analysis using ML 
# by C223205_Afra and C223215_Sumaiya

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Styling
plt.style.use("dark_background")
sns.set_palette("bright")
st.set_page_config(page_title="Student Performance Analysis", layout="wide")
st.title("Student Performance Analysis using Machine Learning")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("StudentsPerformance.csv")
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]

    df["average_score"] = df[["math_score", "reading_score", "writing_score"]].mean(axis=1)
    df["total_score"] = df[["math_score", "reading_score", "writing_score"]].sum(axis=1)

    bins = [0, 40, 50, 55, 60, 65, 70, 75, 80, 101]
    labels = ["F", "D", "C", "C+", "B", "B+", "A-", "A", "A+"]
    df["grade"] = pd.cut(df["average_score"], bins=bins, labels=labels, right=False)

    df.dropna(subset=["grade"], inplace=True)

    df["prep_completed"] = df["test_preparation_course"] == "completed"
    df["standard_lunch"] = df["lunch"] == "standard"
    return df


df = load_data()

# Sidebar Navigation
view_option = st.sidebar.selectbox(
    "Choose View", ["Dashboard", "Exploratory Data Analysis", "Model", "Predict"]
)

# ----------------------- DASHBOARD ------------------------
if view_option == "Dashboard":
    st.sidebar.header("Select Student Criteria")
    gender_filter = st.sidebar.multiselect("Gender", df.gender.unique(), df.gender.unique())
    lunch_filter = st.sidebar.multiselect("Lunch Type", df.lunch.unique(), df.lunch.unique())
    edu_filter = st.sidebar.multiselect(
        "Parental Level of Education", df.parental_level_of_education.unique(),
        df.parental_level_of_education.unique()
    )

    filtered_df = df[
        df.gender.isin(gender_filter)
        & df.lunch.isin(lunch_filter)
        & df.parental_level_of_education.isin(edu_filter)
    ]

    st.subheader(f"Student Information ({len(filtered_df)})")
    st.dataframe(filtered_df.head(50), use_container_width=True, hide_index=True)

# ----------------------- EDA ------------------------
elif view_option == "Exploratory Data Analysis":
    st.header("Exploratory Data Analysis")

    eda_option = st.sidebar.multiselect(
        "Select EDA Insights to View",
        options=[
            "Does Gender Influence Performance?",
            "Does Lunch Type Affect Scores?",
            "Is Test Preparation Effective?",
            "Trend: Parental Education vs Avg Score",
            "Overall Grade Distribution",
            "Students per Grade",
            "Feature Correlation",
            "Score Distribution by Test Preparation",
        ],
        default=["Does Gender Influence Performance?"],
    )

    filtered_df = df

    if "Does Gender Influence Performance?" in eda_option:
        st.subheader("Average Score by Gender")
        fig, ax = plt.subplots()
        sns.barplot(data=filtered_df, x="gender", y="average_score", palette="crest", ax=ax)
        st.pyplot(fig)

    if "Does Lunch Type Affect Scores?" in eda_option:
        st.subheader("Average Score by Lunch Type")
        fig, ax = plt.subplots()
        sns.barplot(data=filtered_df, x="lunch", y="average_score", palette="crest", ax=ax)
        st.pyplot(fig)

    if "Is Test Preparation Effective?" in eda_option:
        st.subheader("Impact of Test Preparation Course")
        fig, ax = plt.subplots()
        sns.barplot(data=filtered_df, x="test_preparation_course", y="average_score", palette="crest", ax=ax)
        st.pyplot(fig)

    if "Trend: Parental Education vs Avg Score" in eda_option:
        st.subheader("Average Score vs Parental Education")
        fig, ax = plt.subplots(figsize=(10, 5))
        order = [
            "some high school", "high school", "some college",
            "associate's degree", "bachelor's degree", "master's degree"
        ]
        sns.lineplot(
            data=df.groupby("parental_level_of_education")["average_score"].mean().reindex(order),
            marker="o", color="#00ffea", ax=ax
        )
        ax.set_xlabel("Parental Education Level")
        ax.set_ylabel("Average Score")
        st.pyplot(fig)

    if "Overall Grade Distribution" in eda_option:
        st.subheader("Grade Distribution")
        fig, ax = plt.subplots()
        counts = filtered_df.grade.value_counts().sort_index()
        ax.pie(
            counts, labels=counts.index, autopct="%1.1f%%", startangle=140,
            wedgeprops={"edgecolor": "black"},
            colors=sns.color_palette("crest", n_colors=len(counts)),
        )
        ax.axis("equal")
        st.pyplot(fig)

    if "Students per Grade" in eda_option:
        st.subheader("Number of Students per Grade")
        fig, ax = plt.subplots()
        grade_counts = filtered_df.grade.value_counts().sort_index()
        sns.barplot(x=grade_counts.index, y=grade_counts.values, palette="crest", ax=ax)
        ax.set_xlabel("Grade")
        ax.set_ylabel("Number of Students")
        st.pyplot(fig)

    if "Feature Correlation" in eda_option:
        st.subheader("Correlation (Pastel Theme)")
        fig, ax = plt.subplots(figsize=(7, 5))
        corr = df[["math_score", "reading_score", "writing_score", "average_score"]].corr()
        pastel_cmap = plt.get_cmap("crest")
        sns.heatmap(corr, annot=True, cmap=pastel_cmap, linewidths=0.3, linecolor="#222", ax=ax)
        st.pyplot(fig)

    if "Score Distribution by Test Preparation" in eda_option:
        st.subheader("Score Distribution by Test Preparation")
        fig, ax = plt.subplots()
        sns.boxplot(data=filtered_df, x="test_preparation_course", y="average_score", palette="crest", ax=ax)
        st.pyplot(fig)

# ----------------------- MODEL ------------------------
elif view_option == "Model":
    st.header("Model Training and Evaluation")

    model_insights = st.sidebar.multiselect(
        "Select Model Insights",
        options=["Model Accuracy", "Feature Importance", "Classification Report"],
        default=["Model Accuracy"],
    )

    @st.cache_resource
    def build_model(df_train):
        df_mod = df_train.copy()
        enc = {}
        for col in ["gender", "race/ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]:
            le = LabelEncoder()
            df_mod[col] = le.fit_transform(df_mod[col])
            enc[col] = le

        X = df_mod.drop(["grade", "average_score"], axis=1)
        y = df_mod["grade"]
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
        mdl = RandomForestClassifier(n_estimators=120, random_state=42)
        mdl.fit(X_tr, y_tr)
        y_pred = mdl.predict(X_te)
        return mdl, enc, X.columns, X_te, y_te, y_pred

    mdl, encoders, feat_cols, X_test, y_test, y_pred = build_model(df)

    if "Model Accuracy" in model_insights:
        st.success(f"Model Accuracy: **{accuracy_score(y_test, y_pred):.4f}**")

    if "Feature Importance" in model_insights:
        st.subheader("Feature Importance")
        fig, ax = plt.subplots(figsize=(8, 6))
        importances = pd.Series(mdl.feature_importances_, index=feat_cols).sort_values()
        importances.plot(kind="barh", color="cyan", ax=ax)
        st.pyplot(fig)

    if "Classification Report" in model_insights:
        st.subheader("Classification Report")
        st.dataframe(
            pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).T.round(2),
            use_container_width=True,
        )

# ----------------------- PREDICT ------------------------
elif view_option == "Predict":
    st.header("Predict a Student's Grade")

    @st.cache_resource
    def build_predict_model(df_train):
        df_mod = df_train.copy()
        enc = {}
        for col in ["gender", "race/ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]:
            le = LabelEncoder()
            df_mod[col] = le.fit_transform(df_mod[col])
            enc[col] = le

        X = df_mod.drop(["grade", "average_score"], axis=1)
        y = df_mod["grade"]
        mdl = RandomForestClassifier(n_estimators=100, random_state=42)
        mdl.fit(X, y)
        return mdl, enc, X.columns

    mdl, encoders, feat_cols = build_predict_model(df)

    if "show_popup" not in st.session_state:
        st.session_state.show_popup = False

    pred = None

    with st.form("grade_form"):
        col1, col2 = st.columns(2)
        with col1:
            gender = st.selectbox("Gender", df.gender.unique())
            lunch = st.selectbox("Lunch Type", df.lunch.unique())
            test_prep = st.selectbox("Test Preparation", df.test_preparation_course.unique())
        with col2:
            race = st.selectbox("Race/Ethnicity", df["race/ethnicity"].unique())
            parent_edu = st.selectbox("Parental Level of Education", df.parental_level_of_education.unique())

        math = st.slider("Math Score", 0, 100, 75)
        reading = st.slider("Reading Score", 0, 100, 75)
        writing = st.slider("Writing Score", 0, 100, 75)

        submit = st.form_submit_button("Predict Grade")

    if submit:
        inp = pd.DataFrame({
            "gender": [gender],
            "race/ethnicity": [race],
            "parental_level_of_education": [parent_edu],
            "lunch": [lunch],
            "test_preparation_course": [test_prep],
            "math_score": [math],
            "reading_score": [reading],
            "writing_score": [writing],
            "total_score": [math + reading + writing],
            "average_score": [(math + reading + writing) / 3],
            "prep_completed": [test_prep == "completed"],
            "standard_lunch": [lunch == "standard"],
        })

        for col in ["gender", "race/ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]:
            inp[col] = encoders[col].transform(inp[col])

        pred = mdl.predict(inp[feat_cols])[0]
        st.session_state.show_popup = True

    if st.session_state.show_popup and pred is not None:
        col_left, col_mid, col_right = st.columns([1, 4, 1])
        with col_mid:
            st.markdown(
                f"""
                <div style="background-color:#111111cc; border-radius:15px; color:#00ffff;
                    font-size:24px; font-weight:bold; text-align:center; padding:20px;">
                    Predicted Grade: <span style='color:#00ffff;'>{pred}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            btn_left, btn_mid, btn_right = st.columns([1, 2, 1])
            with btn_mid:
                if st.button("Close", key="close_popup"):
                    st.session_state.show_popup = False

        st.balloons()
