run: uvicorn api:app

req: curl --location --request GET 'http://localhost:8000/'
