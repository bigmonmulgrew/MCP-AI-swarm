# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy common package and install it
COPY ./common /common
RUN pip install /common

# Copy the app itself
COPY ./MCP-Data /app
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8050

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8050"]
