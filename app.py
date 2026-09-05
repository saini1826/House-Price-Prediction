import streamlit as st
import pandas as pd
import numpy as np
import joblib
import base64


model = joblib.load("house_model.pkl")

# Page Configuration

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="🏠",
    layout="wide"
)

def add_banner():
    with open("banner.jpg", "rb") as image:
        encoded = base64.b64encode(image.read()).decode()

    st.markdown(
        f"""
        <style>
        .banner {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            height: 200px;
            border-radius: 15px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 30px;
        }}

        .banner h1 {{
            color: white;
            font-size: 80px;
            font-weight: bold;
            background: rgba(0,0,0,0.55);
            padding: 15px 30px;
            border-radius: 35px;
            text-shadow: 2px 2px 8px black;
        }}
        </style>

        <div class="banner">
            <h1> House Price Prediction </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

add_banner()


with st.sidebar:

    st.header("🏠 Project Information")

    st.write(
        """
        This Machine Learning application predicts
        the estimated price of a house based on
        property features.
        """
    )

    st.divider()

    st.subheader("🛠 Technologies")

    st.write(
        """
        • Python  
        • Pandas  
        • Scikit-learn  
        • Joblib  
        • Streamlit  
        """
    )

    st.divider()

    st.info(
        "Enter accurate property information for a better prediction."
    )


# ============================================================
# PROPERTY DETAILS
# ============================================================

st.header("🏡 Property Details")

col1, col2, col3 = st.columns(3)


# ============================================================
# COLUMN 1
# ============================================================

with col1:

    bedrooms = st.number_input(
        "🛏 Number of Bedrooms",
        min_value=1,
        max_value=20,
        value=3,
        step=1
    )

    bathrooms = st.number_input(
        "🛁 Number of Bathrooms",
        min_value=0.5,
        max_value=20.0,
        value=2.0,
        step=0.5
    )

    living_area = st.number_input(
        "📐 Living Area (sq ft)",
        min_value=100,
        max_value=100000,
        value=1500,
        step=50
    )

    lot_area = st.number_input(
        "🌳 Lot Area (sq ft)",
        min_value=100,
        max_value=1000000,
        value=3000,
        step=100
    )


# ============================================================
# COLUMN 2
# ============================================================

with col2:

    floors = st.number_input(
        "🏢 Number of Floors",
        min_value=1.0,
        max_value=20.0,
        value=1.0,
        step=0.5
    )

    waterfront = st.selectbox(
        "🌊 Waterfront Present",
        options=[0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    views = st.number_input(
        "👁 Number of Views",
        min_value=0,
        max_value=20,
        value=0,
        step=1
    )

    condition = st.slider(
        "⭐ Condition of the House",
        min_value=1,
        max_value=5,
        value=3
    )


# ============================================================
# COLUMN 3
# ============================================================

with col3:

    area_excluding_basement = st.number_input(
        "🏠 Area of House (excluding basement) (sq ft)",
        min_value=100,
        max_value=100000,
        value=1500,
        step=50
    )

    schools_nearby = st.number_input(
        "🏫 Number of Schools Nearby",
        min_value=0,
        max_value=50,
        value=2,
        step=1
    )

    basement_area = st.number_input(
        "⬇️ Area of Basement (sq ft)",
        min_value=0,
        max_value=50000,
        value=0,
        step=50
    )

    airport_distance = st.number_input(
        "✈️ Distance from Airport (km)",
        min_value=0.0,
        max_value=1000.0,
        value=10.0,
        step=0.5
    )


# ============================================================
# PROPERTY SUMMARY
# ============================================================

st.divider()

st.header("📋 Property Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.write(f"**Bedrooms:** {bedrooms}")
    st.write(f"**Bathrooms:** {bathrooms}")
    st.write(f"**Living Area:** {living_area:,} sq ft")
    st.write(f"**Lot Area:** {lot_area:,} sq ft")
    st.write(f"**Floors:** {floors}")
    st.write(
        f"**Waterfront:** {'Yes' if waterfront == 1 else 'No'}"
    )

with summary_col2:

    st.write(f"**Views:** {views}")
    st.write(f"**Condition:** {condition}/5")
    st.write(
        f"**House Area:** {area_excluding_basement:,} sq ft"
    )
    st.write(f"**Schools Nearby:** {schools_nearby}")
    st.write(f"**Basement Area:** {basement_area:,} sq ft")
    st.write(
        f"**Airport Distance:** {airport_distance:.1f} km"
    )


# ============================================================
# PREDICTION BUTTON
# ============================================================

st.divider()

predict = st.button(
    "🔮 Predict House Price",
    type="primary",
    use_container_width=True
)


# ============================================================
# PREDICTION
# ============================================================

if predict:

    try:

        # ----------------------------------------------------
        # CREATE INPUT DATAFRAME
        # ----------------------------------------------------

        input_data = pd.DataFrame({

            "number of bedrooms": [bedrooms],

            "number of bathrooms": [bathrooms],

            "living area": [living_area],

            "lot area": [lot_area],

            "number of floors": [floors],

            "waterfront present": [waterfront],

            "number of views": [views],

            "condition of the house": [condition],

            "Area of the house(excluding basement)": [
                area_excluding_basement
            ],

            "Number of schools nearby": [
                schools_nearby
            ],

            "Area of the basement": [
                basement_area
            ],

            "Distance from the airport": [
                airport_distance
            ]
        })


        # ----------------------------------------------------
        # PREDICTION
        # ----------------------------------------------------

        prediction = model.predict(input_data)

        predicted_price = float(prediction[0])


        # ----------------------------------------------------
        # PRICE RESULT
        # ----------------------------------------------------

        st.success("✅ House price successfully predicted!")

        st.divider()

        st.header("💰 Estimated House Price")

        price_col1, price_col2, price_col3 = st.columns(3)

        with price_col1:

            st.metric(
                "Estimated Price",
                f"₹{predicted_price:,.0f}"
            )

        with price_col2:

            st.metric(
                "Price in Lakhs",
                f"₹{predicted_price / 100000:,.2f} Lakh"
            )

        with price_col3:

            st.metric(
                "Price in Crores",
                f"₹{predicted_price / 10000000:,.2f} Cr"
            )


        # ----------------------------------------------------
        # DETAILED RESULT
        # ----------------------------------------------------

        st.divider()

        st.subheader("🏠 Prediction Result")

        st.write(
            f"""
            Based on the property details entered, the estimated
            market price of this house is:
            """
        )

        st.markdown(
            f"""
            <div style="
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                background-color: #f0f2f6;
                border: 1px solid #d0d0d0;
            ">

            <h1>₹{predicted_price:,.0f}</h1>

            <p style="font-size:18px;">
            Estimated House Price
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # INPUT DATA TABLE
        # ----------------------------------------------------

        st.divider()

        st.subheader("📊 Entered Property Details")

        display_data = pd.DataFrame({

            "Property Feature": [
                "Number of Bedrooms",
                "Number of Bathrooms",
                "Living Area",
                "Lot Area",
                "Number of Floors",
                "Waterfront",
                "Number of Views",
                "House Condition",
                "House Area",
                "Schools Nearby",
                "Basement Area",
                "Airport Distance"
            ],

            "Value": [
                bedrooms,
                bathrooms,
                f"{living_area:,} sq ft",
                f"{lot_area:,} sq ft",
                floors,
                "Yes" if waterfront == 1 else "No",
                views,
                f"{condition}/5",
                f"{area_excluding_basement:,} sq ft",
                schools_nearby,
                f"{basement_area:,} sq ft",
                f"{airport_distance:.1f} km"
            ]
        })

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

    except Exception as e:
        st.code(str(e))


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🏠 India House Price Prediction | "
    "Machine Learning + Streamlit"
)