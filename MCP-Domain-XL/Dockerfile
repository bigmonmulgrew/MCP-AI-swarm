# syntax=docker/dockerfile:1.7

# Use the official Python 3.12 slim image
FROM python:3.12-slim

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get upgrade

# # TODO Putting this here for reference, pip does not report these installed in freeze so need to investigate if they are still in use
# Install system dependencies for OCR + PDFs
RUN apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    ghostscript \
    pngquant \
    && rm -rf /var/lib/apt/lists/*

# Optional: language packs (add only what you need)
RUN apt-get install -y tesseract-ocr-eng
# RUN apt-get install -y tesseract-ocr-deu

# Confirm Python and pip versions
RUN python --version && pip --version

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools
# TODO move this to requirements

# Set working directory
WORKDIR /app


# Copy common package and install it
COPY ./common /common
RUN pip install /common

# Copy the app itself
COPY ./MCP-Domain-XL /app
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8041

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:main", "--host", "0.0.0.0", "--port", "8041"]
