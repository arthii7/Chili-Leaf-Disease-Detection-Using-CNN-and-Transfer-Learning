import streamlit as st
import tensorflow as tf
import numpy as np

# Tensorflow Model Prediction
def model_prediction(test_image):
    model = tf.keras.models.load_model("chiili_model.h5")
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(200, 200))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to batch
    predictions = model.predict(input_arr)
    result_index = np.argmax(predictions)  # Get index of the highest prediction
    
    # Class names for prediction results
    class_names = ['Bacterial Spots', 'Cabai Virus', 'Chili Whitefly', 'Healthy Leaves', 'Leaf Spot Disease', 'Yellowish Spots Disease', 'Leaf Curl Disease']
    pesticide_recommendations = {
        'Bacterial Spots': 'Apply copper-based bactericides. Remove infected leaves.',
        'Cabai Virus': 'Use insecticides for aphid control and remove infected plants.',
        'Chili Whitefly': 'Use insecticides containing neonicotinoids or pyrethroids.',
        'Healthy Leaves': 'Your plants are healthy!',
        'Leaf Spot Disease': 'Apply fungicides containing copper or mancozeb. Remove infected leaves to prevent the spread.',
        'Yellowish Spots Disease': 'Apply appropriate fungicides and remove infected leaves.',
        'Leaf Curl Disease': 'Spray Isogashi - 2.5 ml per 10 liters of water and repeat after 10-15 days interval for better control. You can also spray Aza power plus - 5 ml per liter of water when thrips are low in number.'
    }

    # Pesticide product links
    pesticide_links = {
        'Bacterial Spots': [
            'https://www.bighaat.com/products/tata-rallis-blitox-fungicide',
            'https://www.bighaat.com/products/dupont-kocide-2000-fungicide-bactericide'
        ],
        'Cabai Virus': [
            'https://www.bighaat.com/products/confidor',
            'https://kisancenter.in/product/26145071/Syngenta-Actara-Insecticide--Thiamethoxam-25---WG-'
        ],
        'Chili Whitefly': [
            'https://www.kisanestore.com/index.php?route=product/enquiry&product_id=6751',
            'https://www.badikheti.com/insecticide/pdp/syngenta-cruiser-350-fs-thiamethoxam-30-fs-insecticide/snht7wlm'
        ],
        'Healthy Leaves': [],  # No links needed for healthy leaves
        'Leaf Spot Disease': [
            'https://www.bighaat.com/products/dithane-fungicide',
            'https://www.indofil.com/agro/fungicides/indofil-m-45'
        ],
        'Yellowish Spots Disease': [
            'https://www.indiamart.com/proddetail/dithane-m-45-fungicide-16535410391.html',
            'https://www.bighaat.com/products/amistar-fungicide'
        ],
        'Leaf Curl Disease': [
            'https://www.iffcobazar.in/en/product/isogashi-imidacloprid-17-8-sl#isogashi-500-ml',
            'https://www.bighaat.com/products/isogashi-insecticide'
        ]
    }
    
    disease_name = class_names[result_index]
    pesticide_recommendation = pesticide_recommendations[disease_name]
    product_link = pesticide_links[disease_name]
    
    return disease_name, pesticide_recommendation, product_link
# Sidebar
st.sidebar.title("Dashboard")
home_button = st.sidebar.button("Home")
about_button = st.sidebar.button("About")
disease_recognition_button = st.sidebar.button("Disease Recognition")

# Main Page
if "app_mode" not in st.session_state:
    st.session_state.app_mode = "Home"

# Update app_mode in session state based on button clicks
if home_button:
    st.session_state.app_mode = "Home"
elif about_button:
    st.session_state.app_mode = "About"
elif disease_recognition_button:
    st.session_state.app_mode = "Disease Recognition"

# Home page
if st.session_state.app_mode == "Home":
    
    st.header("ChiliAid")
    st.subheader("Welcome to ChiliAid! 🌿🔍")
    st.image("chili image.jpeg", caption="ChiliAid",use_column_width=True)
    st.markdown("""
    
    ChiliAid is your reliable partner for diagnosing diseases in chili leaves.
    
    Our state-of-the-art machine learning model accurately identifies diseases affecting chili plants. Upload a photo of a chili leaf on the **Disease Recognition** page, and we'll analyze the leaf and provide a diagnosis.

    ### How It Works:
    - **Take a Picture**: Get a clear photo of the chili leaf you want to examine.
    - **Upload the Image**: Submit the photo in the **Disease Recognition** page.
    - **Get Your Diagnosis**: Our model will analyze the image and give you a diagnosis.

    ### Get Started
    Visit the **Disease Recognition** page to begin!

    ### About Us:
    Learn more about the project and our mission on the **About** page.
    """)

# About page
elif st.session_state.app_mode == "About":
    st.header("About")
    st.markdown("""
    #### About ChiliAid
    ChiliAid is an innovative project that leverages machine learning to diagnose diseases in chili leaves. Our mission is to help farmers and gardeners identify and manage plant diseases efficiently and effectively.

    ### About the Dataset
    The dataset includes real-world chili leaf images from Andhra Pradesh and Telangana, covering various conditions and diseases. It consists of thousands of images categorized into different classes. We strive to provide accurate and useful insights for better plant care.

    Thank you for using ChiliAid!
    """)

# Disease Recognition page
elif st.session_state.app_mode == "Disease Recognition":
    st.header("Disease Recognition")
    
    # File uploader
    test_image = st.file_uploader("Choose an Image:")
    
    if "show_image" not in st.session_state:
        st.session_state.show_image = False

    # Show or hide the image based on the state and user actions
    if st.session_state.show_image:
        # Display the uploaded image
        if test_image:
            st.image(test_image, width=400, use_column_width=True)

        # Show "Hide Image" button to hide the image
        if st.button("Hide Image"):
            st.session_state.show_image = False
    else:
        # Show "Show Image" button only if `show_image` is False
        if st.button("Show Image"):
            if test_image:
                st.session_state.show_image = True
            else:
                st.warning("Please upload an image to display.")

    # Predict button
    if st.button("Predict"):
        if test_image:
            disease_name, pesticide_recommendation, product_links = model_prediction(test_image)
            
            # Display the prediction and recommendation
            st.write(f"Model is predicting it's a {disease_name}")
            st.write(f"Pesticide Recommendation: {pesticide_recommendation}")
            
            # Display multiple links for the recommended products
            st.write("Recommended Pesticide Products:")
            for link in product_links:
                st.markdown(f"[Product Link]({link})")
        else:
            st.warning("Please upload an image to make a prediction.")

