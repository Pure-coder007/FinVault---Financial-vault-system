# Use a specific version of Python for consistency
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy only requirements first to cache dependencies
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the application port (optional, but good practice)
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "wallet.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
