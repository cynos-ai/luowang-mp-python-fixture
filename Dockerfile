FROM docker.m.daocloud.io/library/python:3.13-slim@sha256:8d9d0b8bcf6506481eae4907c18f5e3e7902e629f5f6d684f9e7c32e85e3ddf0
ARG PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir --index-url "${PIP_INDEX_URL}" -r requirements.txt \
    && useradd --uid 1000 --create-home app \
    && mkdir -p /data \
    && chown app:app /data
COPY app.py ./
USER app
ENV APP_DATA_DIR=/data PORT=3100
EXPOSE 3100
HEALTHCHECK --interval=20s --timeout=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:3100/health', timeout=3)"
CMD ["python", "app.py"]
