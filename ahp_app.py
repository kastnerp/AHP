import streamlit as st
from ahpy import Compare
import pandas as pd

# Basic Streamlit app layout
st.title("Analytic Hierarchy Process (AHP) App")

st.markdown("""
This app demonstrates a simple implementation of the Analytic Hierarchy Process using the `ahpy` library.
""")

# Input parameters
st.subheader("Input Parameters")

num_criteria = st.number_input("Number of Criteria", min_value=2, max_value=10, value=3, step=1)
num_alternatives = st.number_input("Number of Alternatives", min_value=2, max_value=10, value=3, step=1)

# Criteria data
st.subheader("Criteria")
criteria_data = []

for i in range(num_criteria):
    criteria_data.append(
        st.text_input(f"Criterion {i + 1}", f"Criterion {i + 1}")
    )

# Pairwise comparison matrix
st.subheader("Pairwise Comparison Matrix")

comparison_matrix = {}

for i in range(num_criteria):
    for j in range(i + 1, num_criteria):
        weight = st.number_input(f"{criteria_data[i]} / {criteria_data[j]}", min_value=1.0, max_value=9.0, value=1.0)
        comparison_matrix[(criteria_data[i], criteria_data[j])] = weight

criteria_compare = Compare(name="Criteria", comparisons=comparison_matrix)

# Alternatives data
st.subheader("Alternatives")
alternatives_data = []

for i in range(num_alternatives):
    alternatives_data.append(
        st.text_input(f"Alternative {i + 1}", f"Alternative {i + 1}")
    )

# Alternative comparison matrices
alternative_comparison_matrices = []

for i in range(num_criteria):
    st.subheader(f"Pairwise Comparison Matrix for {criteria_data[i]}")
    comparison_matrix = {}

    for j in range(num_alternatives):
        for k in range(j + 1, num_alternatives):
            weight = st.number_input(f"{alternatives_data[j]} / {alternatives_data[k]} ({criteria_data[i]})", min_value=1.0, max_value=9.0, value=1.0)
            comparison_matrix[(alternatives_data[j], alternatives_data[k])] = weight

    alternative_compare = Compare(name=criteria_data[i], comparisons=comparison_matrix)
    alternative_comparison_matrices.append(alternative_compare)

# Calculate and display results
if st.button("Calculate AHP"):
    criteria_priorities = criteria_compare.target_weights

    alternative_priorities = {}
    for i, compare in enumerate(alternative_comparison_matrices):
        alternative_priorities[criteria_data[i]] = compare.target_weights


    priorities_df = pd.DataFrame(alternative_priorities)
    priorities_df["Overall Priority"] = priorities_df.dot(pd.Series(criteria_priorities))

    st.subheader("Results")
    st.write("Criteria Priorities:")
    st.write(pd.DataFrame(criteria_priorities, index=[0]))

    st.write("Alternative Priorities:")
    st.write(priorities_df)

    winner = priorities_df["Overall Priority"].idxmax()
    st.write(f"The best alternative is: {alternatives_data[winner]}")
