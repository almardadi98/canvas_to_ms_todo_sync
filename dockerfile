FROM python:3.9.1
ADD . /canvas_to_ms_todo_sync
WORKDIR /canvas_to_ms_todo_sync
RUN pip install -r requirements.txt
CMD ["python", "./main.py"]