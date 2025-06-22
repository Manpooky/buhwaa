## Backend Setup:

1. Navigate to the backend directory:
```bash
cd backend
```

2. Setup virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
**may need to use python3 instead of python**

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install llama-api-client
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Ensure other enivronment variables are set in the .env file

6. Run the application:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
