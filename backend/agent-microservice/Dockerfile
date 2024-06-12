FROM python:3.10
WORKDIR /usr/src/app
COPY requirements.txt ./
# Use the cpu version of torch to reduce the image size!
RUN pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu
RUN pip3 install -r requirements.txt
EXPOSE 5000

# Define API keys before building!
ENV FLASK_APP=src/app.py
ENV LLAMA_CLOUD_API_KEY="llx-fXFuX5RKEN1UdIslUkexVjUAhRnbzrGFeoMV17bCCl5Fk2Gu"
ENV DEEPL_AUTH_KEY="5482dc3f-0ae0-44aa-878f-b2ec0627199e:fx"
ENV SERPER_API_KEY="4df1d7be47c85eb1f682266c4bf4467c4a7bb475"
ENV ELEVEN_API_KEY="fd1c954a1727025d938dc63bad73cf59"
ENV AWS_ACCESS_KEY_ID="AKIA6ODU2MC35K6X7GUH"
ENV AWS_SECRET_ACCESS_KEY="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"
ENV RAPIDAPI_KEY="df3eb765afmsh0a6eb117c21ff4ep12e383jsnb13d7de552a7"
ENV RUNPOD_URL="https://hud7poriedy9c2-11434.proxy.runpod.net/api/generate"


CMD ["flask", "run", "--host=0.0.0.0"]