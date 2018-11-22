FROM python:2.7

WORKDIR '/app'
COPY ./ ./
RUN pip install pipenv
RUN pipenv install
CMD ["pipenv", "run",  "python", "./parse_cisco_pcrf.py", "./rawdata"]
