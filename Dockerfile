# Use a slim version of Python 3.9 as the base image.
FROM python:3.9-slim

# Set the working directory inside the container.
WORKDIR /app

# Copy the requirements file into the container.
COPY requirements.txt .

# Upgrade pip and install the required packages.
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of your application code into the container.
COPY . .

# Expose the port that Streamlit uses (default is 8501).
EXPOSE 8501

# Set the entrypoint to run your Streamlit app.
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
