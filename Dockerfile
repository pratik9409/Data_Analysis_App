# Use Python image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py"]
