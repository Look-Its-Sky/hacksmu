FROM python:3.11

ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

COPY . /app
WORKDIR /app

RUN /root/.cargo/bin/uv pip install --system --no-cache -r requirements.txt
# RUN /root/.cargo/bin/uv pip install --system --no-cache opencv-contrib-python-headless

CMD ["python", "main.py"]
