




import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import openai
import spacy
import stripe
from auth import login, signup
from database import check_user_subscription, update_user_subscription

# Initialize Stripe API Key (replace with your own secret key)
stripe.api_key = "stripe_api_key"

# Initialize NLP model (spaCy)
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    st.error(f"Error loading spaCy model: {str(e)}")
    nlp = None

# OpenAI API setup
openai.api_key = "open_api_key"

st.set_page_config(page_title="SaaS Analytics Platform", page_icon="📊")

# Function to check login state
def check_login_state():
    if 'user' not in st.session_state:
        st.session_state.user = None
    return st.session_state.user

# Login or Signup
if 'user' not in st.session_state or st.session_state.user is None:
    user = login()
    if user:
        st.session_state.user = user
    else:
        signup()

user = check_login_state()

if user:
    try:
        subscription_level = check_user_subscription(user["localId"])
    except Exception as e:
        st.error(f"Error checking subscription: {str(e)}")
        subscription_level = "free"

    # Display subscription info
    if subscription_level == "free":
        st.warning("Free Plan: LLM and advanced analytics are restricted.")
    elif subscription_level == "premium":
        st.success("Premium Plan Access")
else:
    st.warning("Please log in to access the platform features.")

# Function to create a Stripe checkout session
def create_checkout_session(email, plan_type):
    price_id_map = {
        'monthly': 'price_id',  # Replace with your Stripe price ID for monthly
        'quarterly': 'price_id',  # Replace with your Stripe price ID for quarterly
        'yearly': 'price_id'  # Replace with your Stripe price ID for yearly
    }

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='subscription',
            line_items=[{
                'price': price_id_map[plan_type],
                'quantity': 1,
            }],
            customer_email=email,
            success_url='http://localhost:8501?success=true',
            cancel_url='http://localhost:8501?canceled=true',
        )
        return session.url
    except Exception as e:
        st.error(f"Error creating checkout session: {str(e)}")
        return None

# Subscription Purchase Section
st.subheader("Purchase Subscription Plan")

# Only allow logged-in users to see the subscription options
if user:
    # Debugging statements
    st.write(f"Logged in as: {user['email']}")
    st.write(f"Subscription level: {subscription_level}")

    
    st.warning("You are on the Free Plan. Upgrade to access premium features.")
        
        # Dropdown menu to select plan
    plan = st.selectbox(
        "Choose a subscription plan:",
        options=["Monthly ($10)", "Quarterly ($27)", "Yearly ($100)"],
        index=0  # default selection
    )
    
    # Button to initiate the upgrade process
    if st.button(f"Upgrade to {plan.split(' ')[0]} Plan"):
        plan_type = plan.split(' ')[0].lower()  # Extracts 'monthly', 'quarterly', or 'yearly'
        checkout_url = create_checkout_session(user["email"], plan_type)
        if checkout_url:
            st.markdown(f"[Click here to proceed with payment]({checkout_url})")

    if subscription_level == "premium":
        st.success("You are already subscribed to the Premium Plan!")
else:
    st.warning("Please log in to access the subscription features.")

# Check if the payment was successful or canceled
query_params = st.query_params
if 'success' in query_params:
    st.success("Payment Successful! Your subscription has been upgraded.")
    try:
        update_user_subscription(user["localId"], "premium")
    except Exception as e:
        st.error(f"Error updating subscription: {str(e)}")
elif 'canceled' in query_params:
    st.warning("Payment was canceled. Please try again.")

# File uploader for CSV, Excel, and Images
file = st.file_uploader('Upload a CSV, Excel, or Image file', type=['csv', 'xlsx', 'png', 'jpg'])

if file:
    # Handle CSV and Excel files
    if file.name.endswith(('csv', 'xlsx')):
        try:
            if file.name.endswith('csv'):
                data = pd.read_csv(file)
            else:
                data = pd.read_excel(file)
            
            # Show basic information available for all users
            st.subheader(':rainbow[Dataset Preview]',divider='rainbow')
            st.dataframe(data.head())

            st.subheader(':rainbow[Dataset Shape]',divider='rainbow')
            st.write(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")

            st.subheader(':rainbow[Dataset Description]',divider='rainbow')
            st.dataframe(data.describe())


            st.subheader(':rainbow[Basic information of the dataset]',divider='rainbow')
            tab1,tab2,tab3,tab4 = st.tabs(['Summary','Top and Bottom Rows','Data Types','Columns'])

            with tab1:
                st.write(f'There are {data.shape[0]} rows in dataset and  {data.shape[1]} columns in the dataset')
                st.subheader(':gray[Statistical summary of the dataset]')
                st.dataframe(data.describe())
            with tab2:
                st.subheader(':gray[Top Rows]')
                toprows = st.slider('Number of rows you want',1,data.shape[0],key='topslider')
                st.dataframe(data.head(toprows))
                st.subheader(':gray[Bottom Rows]')
                bottomrows = st.slider('Number of rows you want',1,data.shape[0],key='bottomslider')
                st.dataframe(data.tail(bottomrows))
            with tab3:
                st.subheader(':grey[Data types of column]')
                st.dataframe(data.dtypes)
            with tab4:
                st.subheader('Column Names in Dataset')
                st.write(list(data.columns))
    
            st.subheader(':rainbow[Column Values To Count]',divider='rainbow')
            with st.expander('Value Count'):
                col1,col2 = st.columns(2)
                with col1:
                    column  = st.selectbox('Choose Column name',options=list(data.columns))
                with col2:
                    toprows = st.number_input('Top rows',min_value=1,step=1)
                
                count = st.button('Count')
                if(count==True):
                    result = data[column].value_counts().reset_index().head(toprows)
                    st.dataframe(result)
                    st.subheader('Visualization',divider='gray')
                    fig = px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_white')
                    st.plotly_chart(fig)
                    fig = px.line(data_frame=result,x=column,y='count',text='count',template='plotly_white')
                    st.plotly_chart(fig)
                    fig = px.pie(data_frame=result,names=column,values='count')
                    st.plotly_chart(fig)

            st.subheader(':rainbow[Groupby : Simplify your data analysis]',divider='rainbow')
            st.write('The groupby lets you summarize data by specific categories and groups')
            with st.expander('Group By your columns'):
                col1,col2,col3 = st.columns(3)
                with col1:
                    groupby_cols = st.multiselect('Choose your column to groupby',options = list(data.columns))
                with col2:
                    operation_col = st.selectbox('Choose column for operation',options=list(data.columns))
                with col3:
                    operation = st.selectbox('Choose operation',options=['sum','max','min','mean','median','count'])
        
                if(groupby_cols):
                    result = data.groupby(groupby_cols).agg(
                        newcol = (operation_col,operation)
                    ).reset_index()

                    st.dataframe(result)

                    st.subheader(':gray[Data Visualization]',divider='gray')
                    graphs = st.selectbox('Choose your graphs',options=['line','bar','scatter','pie','sunburst'])
                    if(graphs=='line'):
                        x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                        y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                        color = st.selectbox('Color Information',options= [None] +list(result.columns))
                        fig = px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                        st.plotly_chart(fig)
                    elif(graphs=='bar'):
                        x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                        y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                        color = st.selectbox('Color Information',options= [None] +list(result.columns))
                        facet_col = st.selectbox('Column Information',options=[None] +list(result.columns))
                        fig = px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group')
                        st.plotly_chart(fig)
                    elif(graphs=='scatter'):
                        x_axis = st.selectbox('Choose X axis',options=list(result.columns))
                        y_axis = st.selectbox('Choose Y axis',options=list(result.columns))
                        color = st.selectbox('Color Information',options= [None] +list(result.columns))
                        size = st.selectbox('Size Column',options=[None] + list(result.columns))
                        fig = px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color,size=size)
                        st.plotly_chart(fig)
                    elif(graphs=='pie'):
                        values = st.selectbox('Choose Numerical Values',options=list(result.columns))
                        names = st.selectbox('Choose labels',options=list(result.columns))
                        fig = px.pie(data_frame=result,values=values,names=names)
                        st.plotly_chart(fig)
                    elif(graphs=='sunburst'):
                        path = st.multiselect('Choose your Path',options=list(result.columns))
                        fig = px.sunburst(data_frame=result,path=path,values='newcol')
                        st.plotly_chart(fig)

            # Advanced features for Premium users
            if subscription_level == "premium":
                st.subheader("Advanced Data Analysis")
                st.write("Correlation Matrix")
                st.dataframe(data.corr())

                st.write("Distribution Plot")
                column = st.selectbox('Select a column to visualize', data.columns)
                fig = px.histogram(data, x=column)
                st.plotly_chart(fig)

                # Groupby and Visualization
                st.subheader("Group By Functionality")
                groupby_cols = st.multiselect('Group By Columns', options=list(data.columns))
                operation = st.selectbox('Operation', ['sum', 'mean', 'max', 'min', 'count'])
                if groupby_cols:
                    grouped_data = data.groupby(groupby_cols).agg(operation).reset_index()
                    st.dataframe(grouped_data)

                    # Visualization
                    fig = px.bar(grouped_data, x=groupby_cols[0], y=grouped_data.columns[1])
                    st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error processing CSV/Excel file: {str(e)}")

    # Handle Image files
    elif file.name.endswith(('png', 'jpg')):
        try:
            img = Image.open(file)
            st.image(img, caption='Uploaded Image', use_column_width=True)
            st.subheader("LLM Image Analysis")
            if st.button("Generate Image Caption"):
                prompt = "Describe the content of the image."
                response = openai.Completion.create(model="text-davinci-004", prompt=prompt, max_tokens=100)
                st.write(f"Image Caption: {response.choices[0].text.strip()}")
        except Exception as e:
            st.error(f"Error processing image file: {str(e)}")

# LLM and NLP Integration (for premium users)
st.subheader('Ask the LLM')
query = st.text_input("Enter your query or code:")
if query:
    try:
        if subscription_level == "premium":
            # Call OpenAI API for response
            response = openai.Completion.create(
                model="text-davinci-004",
                prompt=f"Analyze the following: {query}",
                max_tokens=150
            )
            st.write(f"LLM Response: {response.choices[0].text.strip()}")

            # NLP Processing (Named Entity Recognition)
            if nlp:
                st.subheader("NLP Analysis")
                doc = nlp(query)
                for ent in doc.ents:
                    st.write(f"Entity: {ent.text} | Label: {ent.label_}")
            else:
                st.warning("NLP model not available. Please check the spaCy installation.")
        else:
            st.warning("Upgrade to Premium for full LLM access")
    except Exception as e:
        st.error(f"Error in LLM/NLP processing: {str(e)}")

# Peer Review & Feedback
st.subheader("Peer Review Section")
feedback = st.text_area("Enter your feedback")
if st.button("Submit Feedback"):
    st.success("Feedback Submitted!")
