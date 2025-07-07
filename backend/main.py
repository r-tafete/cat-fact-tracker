from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from contextlib import asynccontextmanager

database = Database("sqlite:///./backend/cat_facts.db")

# database lifespan setup for connect/disconnect
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

# add middleware to connect to frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Root function. Needed for base app to work.
Args: no args
Returns: A message indicating successful load of cat facts app
"""
@app.get("/")
def root():
    return {"message": "Cat Facts!"}

"""
Fetches all cat facts from database.
Args: no args
Returns: results of SQL query (all rows in cat_facts database)
"""
@app.get("/catfacts")
async def get_cat_facts():
    results = await database.fetch_all(query = "SELECT * FROM cat_facts")
    return results

"""
Fetches a random cat fact from database.
Args: no args
Returns: results of SQL query (random row in database)
"""
@app.get("/catfacts/random")
async def get_random_cat_fact():
    results = await database.fetch_one(query = "SELECT * FROM cat_facts ORDER BY RANDOM()")
    return results

"""
Adds a given (unique) cat fact to database.
Args: cat_fact -- taken in from a form in front-end
Returns: a message indicating success or failure in adding fact to database
"""
@app.post("/catfacts")
async def post_cat_fact(cat_fact: str):
    if not cat_fact:
        return {"message": "No fact provided!"}
    
    cat_fact_dict = {"cat_fact": cat_fact}

    try:
        await database.execute(query = "INSERT INTO cat_facts (fact) VALUES (:cat_fact)", values = cat_fact_dict)
        return {"message": "Fact added to database!"}

    # catches and logs errors if fact cannot be added to database (e.g., if provided fact is not unique/already in database)
    except Exception:
        print("Cannot add " + cat_fact)
        return {"message": "Fact cannot be added to database!"}
