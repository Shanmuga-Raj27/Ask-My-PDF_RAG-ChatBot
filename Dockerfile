# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Set the working directory
WORKDIR /code

# Copy the requirements file and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Create a non-root user for security (Hugging Face best practice)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home
WORKDIR $HOME/app

# Copy the rest of your application code
COPY --chown=user . $HOME/app

# Expose port 7860 (HF default)
EXPOSE 7860

# Command to run the Streamlit app
# --server.port=7860 and --server.address=0.0.0.0 are mandatory
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]