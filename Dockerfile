FROM python:3.9-slim

# Set working directory
WORKDIR /site

# Copy all files into the container
COPY . /site

# Expose port 10000 for Render
EXPOSE 10000

# Run the simple HTTP server
CMD ["python3", "-m", "http.server", "10000"]