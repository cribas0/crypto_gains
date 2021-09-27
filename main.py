from fastapi import FastAPI, Path, HTTPException, status
from crud import (add_user_db,add_transaction_db,get_user_db,get_user_balance_db,delete_user_db)
from pydantic_models import (
    UserSignUp, AddTransaction,
    StandardResponse,
)

app = FastAPI()

@app.post("/sign_up")
def SignUpUser(RequestBody: UserSignUp): 
    try:
        add_user_db(RequestBody)
    except:
        raise HTTPException (
            status_code = status.HTTP_409_CONFLICT,
            detail = (
                ("The user already exists")
            )
        ) 
    return StandardResponse(code = "Success", message = "User created successfully")
  

@app.post("/add_transaction")
def addTransaction(RequestBody: AddTransaction): 
#    try:
        add_transaction_db(RequestBody)

#    except:
#        return ("Error")
#    return StandardResponse(code = "Success", message = "User created successfully")

@app.get("/get_user_by_id/{user_id}")
def GetUserInfo(user_id: int):
    return(get_user_db(user_id))

@app.get("/get_user_balance_by_id/{user_id}")
def GetUserBalanceInfo(user_id: int):
    return(get_user_balance_db(user_id))


@app.delete("/delete_user_by_id/{user_id}")
def DeleteUserInfo(user_id: int):
    try:
        delete_user_db(user_id)
    except:
        raise HTTPException (
            status_code = status.HTTP_409_CONFLICT,
            detail = ("This User ID does not exist")
        )
    return StandardResponse(code = "Success", message = "User deleted successfully")

""" @app.get("/get-student/{student_id}") 
def get_student(student_id: int = Path(None, description="The ID of the student you want to see", gt=0, lt=3)): 
     return students[student_id]

@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None, test: int): 
   for student_id in students:
       if students[student_id]["name"] == name:
           return students[student_id]
       else: 
           return {"Data": "Not found"}   """

""" @app.post("/create-student/{student_id}")
def create_student(student_id: int, student : Student):
    if student_id in students:
        return {"Error" : "Student already exists"}
    else:
        students[student_id] = student
        return students[student_id]

@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error" : "This student's ID does not exist"}
    else: 
        if student.name != None: 
            students[student_id].name = student.name
        if student.age != None: 
            students[student_id].age = student.age
        if student.year != None: 
            students[student_id].year = student.year

        return students[student_id]
 """

""" @app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error" : "This student's ID does not exist"}
    else:
        del students[student_id]
        return {"Message" : "Student deleted successfully!"} """