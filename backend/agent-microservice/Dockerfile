FROM python:3.10
WORKDIR /usr/src/app
COPY requirements.txt ./
# Use the cpu version of torch to reduce the image size!
RUN pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
RUN pip3 install -r requirements.txt
EXPOSE 5000

# Define API keys before building!
# ENV FLASK_APP=src/app.py
# ENV DEEPL_AUTH_KEY
# ENV SERPER_API_KEY
# ENV ELEVEN_API_KEY
# ENV OPENAI_API_KEY
# ENV LLAMA_CLOUD_API_KEY
# ENV AWS_ACCESS_KEY_ID
# ENV AWS_SECRET_ACCESS_KEY
# ENV RAPIDAPI_KEY


CMD ["flask", "run", "--host=0.0.0.0"]