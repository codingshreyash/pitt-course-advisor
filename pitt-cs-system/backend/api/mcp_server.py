
from fastapi import FastAPI
from backend.database.courses_db import CoursesDatabase
from backend.database.models import Course
from sqlalchemy import or_

app = FastAPI(
    title="Pitt CS Course Advisor - MCP Server",
    description="An MCP server for providing AI-powered course advice.",
    version="1.0.0",
)

db = CoursesDatabase()

@app.get("/search/courses")
def search_courses(query: str):
    """Search for courses by title or description."""
    session = db.get_session()
    search_term = f"%{query}%"
    courses = session.query(Course).filter(
        or_(
            Course.title.ilike(search_term),
            Course.description.ilike(search_term)
        )
    ).all()
    session.close()
    return courses

@app.get("/courses/{course_code}/prerequisites")
def get_prerequisites(course_code: str):
    """Get the prerequisites for a specific course."""
    session = db.get_session()
    course = session.query(Course).filter_by(code=course_code.upper()).first()
    session.close()
    if course:
        return {"course_code": course.code, "prerequisites": course.prerequisites}
    else:
        return {"error": "Course not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
