FROM python:3.10
WORKDIR /code
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
# Fill the gaps before building the container
# ENV DEEPL_AUTH_KEY=
# ENV SERPER_API_KEY=
# ENV ELEVEN_API_KEY=
# ENV OPENAI_API_KEY=
# ENV LLAMA_CLOUD_API_KEY=
# ENV AWS_ACCESS_KEY_ID=
# ENV AWS_SECRET_ACCESS_KEY=
COPY requirements.txt requirements.txt
RUN pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run", "--host=0.0.0.0"]