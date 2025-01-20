FROM python:3.12
WORKDIR /app
COPY . /app/
RUN pip install --no-cache-dir -r requirements.txt
# EXPOSE 8502
ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]