
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response


from bson import ObjectId
from pymongo import ReturnDocument
from api.models import *
from api.routers import users, dashboard, kafka, widgets

from api.dependencies import get_logger, init_mongo, app


app.include_router(users.router)
app.include_router(dashboard.router)
app.include_router(kafka.router)
app.include_router(widgets.router)









# @app.get(
#     "/students/{id}",
#     response_description="Get a single student",
#     response_model=StudentModel,
#     response_model_by_alias=False,
# )
# async def show_student(id: str):
#     """
#     Get the record for a specific student, looked up by `id`.
#     """
#     if (
#         student := await student_collection.find_one({"_id": ObjectId(id)})
#     ) is not None:
#         return student

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")


# @app.put(
#     "/students/{id}",
#     response_description="Update a student",
#     response_model=StudentModel,
#     response_model_by_alias=False,
# )
# async def update_student(id: str, student: UpdateStudentModel = Body(...)):
#     """
#     Update individual fields of an existing student record.

#     Only the provided fields will be updated.
#     Any missing or `null` fields will be ignored.
#     """
#     student = {
#         k: v for k, v in student.model_dump(by_alias=True).items() if v is not None
#     }

#     if len(student) >= 1:
#         update_result = await student_collection.find_one_and_update(
#             {"_id": ObjectId(id)},
#             {"$set": student},
#             return_document=ReturnDocument.AFTER,
#         )
#         if update_result is not None:
#             return update_result
#         else:
#             raise HTTPException(status_code=404, detail=f"Student {id} not found")

#     # The update is empty, but we should still return the matching document:
#     if (existing_student := await student_collection.find_one({"_id": id})) is not None:
#         return existing_student

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")


# @app.delete("/students/{id}", response_description="Delete a student")
# async def delete_student(id: str):
#     """
#     Remove a single student record from the database.
#     """
#     delete_result = await student_collection.delete_one({"_id": ObjectId(id)})

#     if delete_result.deleted_count == 1:
#         return Response(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")