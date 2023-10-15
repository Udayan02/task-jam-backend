# FastAPI is a Python class that provides all the functionality for your API.
from fastapi import FastAPI
from models import Todo

# FIREBASE:
import firebase_admin
from firebase_admin import credentials
# This is what we're gonna use to communicate with firestore database
from firebase_admin import firestore

# Creating a certificate containing our credentials
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Stores the client to our firestore database and what we'll use to talk to our database.
db = firestore.client()

# Data with auto-IDs
data = {"task": "Drink too much alcohol"}
db.collection("todos").add({"id": 3, "todo": "Brush your teeth"})

# Data with manually set IDs. For this, we use .set() instead of .add()
data2 = {"task": "Fuck a lot, moan even more"}
db.collection("todos").document("1").set(data2)  # Creates a document reference
# Using .set() again with the same id will just replace the existing one, not add a new on.

# Merging:
db.collection("todos").document("1").set(
    {"timeframe": ""}, merge=True)  # Last step is important or
# else all the data will just be overwritten.

# db.collection("users").document("User1")
# db.collection("users").document("User2")
# db.collection("users").document("User3")

# Here the app variable will be an "instance" of the class FastAPI.
# This app is the same one referred by uvicorn in the command: uvicorn main:app --reload

user_array = list()
ref = db.collection("users").get()

for u in ref:
    print(u.to_dict()["friends"])

app = FastAPI(description="This is a backend server for our DubHacks project.",
              title="DubHacks23Project")


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Storing todos as a list, instead of a database rn:
todos = list()

# GET ALL TODOS:


@app.get("/todos")
async def get_all_todos():
    return {"todos": todos}


# GET A SINGLE Todo
# We can get a single todo by passing its id as a parameter
# Read "Path Parameters" on FastAPI Documentation
@app.get("/todos/{todo_id}")
# If we don't declare the type as an int, Python would assume
async def get_todo(todo_id: int):
    # it to be a string.
    for todo in todos:
        if todo.id == todo_id:  # todo.id because todo is an object of class Todo which has a field id
            return {"todo": todo}
    return {"message": "No Todos found :("}


# CREATE A Todo:
@app.post("/todos")
# The todo item now has to follow the Data model outlined in the Todo class.
async def create_todo(todo: Todo):
    # Basically, todo is an object of type Todo, like int and str
    # MODIFY WHEN USING DATABASE. FOR EXAMPLE: database.write()
    todos.append(todo)
    return {"message": "Todo successfully added"}


# DELETE A Todo:
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            return {"message": "Todo successfully removed! Good job!"}
    return {"message": "No Todos to delete :("}


# UPDATE A Todo:
# Put updates whole objects, and Patch updates parts of an object
# Since we're only dealing with two fields, id and item, we can use Put.
@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, new_todo: Todo):
    # todo_id is the id of the todo to update;
    # new_todo is the new todo that we want to replace the old one with
    for todo in todos:
        if todo.id == todo_id:
            todo.id = todo_id
            # new_todo is still an object of type Todo, we need to specify we're changing
            todo.item = new_todo.item
            # only its item field.
            return {"todo": todo}
    return {"message": "Oops, no such todo found"}


@app.post("/login")
async def create_access_token():
    pass


@app.post("/ping")  # Validating
async def validate_token():
    pass
