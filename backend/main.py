from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from contextlib import asynccontextmanager

database = Database("sqlite:///./backend/cat_facts.db")

# database connect/disconnect setup
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can limit this to http://localhost:3000 if preferred
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Cat Facts!"}

@app.get("/catfacts")
async def get_cat_facts():
    query = "SELECT * FROM cat_facts"
    results = await database.fetch_all(query = query)
    return results

@app.get("/catfacts/random")
async def get_random_cat_fact():
    query = "SELECT * FROM cat_facts ORDER BY RANDOM() LIMIT 1"
    results = await database.fetch_all(query = query)
    return results

@app.post("/catfacts")
async def post_cat_fact(cat_fact: str):
    if not cat_fact:
        return {"message": "No fact provided!"}

    try:
        query = "INSERT INTO cat_facts (fact) VALUES (:fact)"
        await database.execute(query=query, values={"fact": cat_fact})
        return {"message": "Fact added to database!"}

    except Exception:
        return {"message": "Fact cannot be added to database!"}
