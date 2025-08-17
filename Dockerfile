# Use a slim, specific Python version as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's layer caching
COPY requirements.txt .

# Install the Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY . .

# --- ADD THIS LINE ---
# Run the training script to create a compatible model.pkl file
RUN python retrain.py
# ---------------------

# Expose the correct port that the Flask app runs on
EXPOSE 5000

# Specify the command to run when the container starts
CMD ["python", "app.py"]
