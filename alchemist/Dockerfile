FROM python:3.9

# 
WORKDIR /code

# 
COPY ./alchemist/requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY  . .

EXPOSE 8080

# 
<<<<<<< HEAD
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
=======
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
>>>>>>> 2bba826 (fix: backend complete implementation)
