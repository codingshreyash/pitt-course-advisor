
import httpx
from bs4 import BeautifulSoup
from backend.database.courses_db import CoursesDatabase
from backend.database.models import Course, CourseSource, DataConflict

def scrape_official_site():
    """Scrapes course information from the official SCI website."""
    print("Starting official site scrape...")

    db = CoursesDatabase()
    session = db.get_session()

    courses_to_scrape = session.query(Course).filter(Course.sci_href != None).all()

    if not courses_to_scrape:
        print("No courses with sci_href found in the database.")
        return

    print(f"Found {len(courses_to_scrape)} courses to scrape from the official site.")

    for course in courses_to_scrape:
        print(f"Scraping {course.code} from {course.sci_href}")
        try:
            response = httpx.get(course.sci_href, follow_redirects=True)
            response.raise_for_status()
        except httpx.RequestError as exc:
            print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            continue
        except httpx.HTTPStatusError as exc:
            print(f"Error response {exc.response.status_code} while requesting {exc.request.url!r}: {exc.response.text}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        h1 = soup.find('h1')
        if h1:
            update_field(session, course, 'title', h1.text.strip(), 'official')

        # Extract description
        description_p = h1.find_next_sibling('p')
        if description_p and description_p.p:
            update_field(session, course, 'description', description_p.p.text.strip(), 'official')

        # Extract other details
        details_p = description_p.find_next_sibling('p')
        if details_p:
            for span in details_p.find_all('span', style="font-weight:bold"):
                field_name = span.text.strip()
                field_value = span.next_sibling.strip() if span.next_sibling else None
                if field_value:
                    if "Course Requirements:" in field_name:
                        update_field(session, course, 'prerequisites', field_value, 'official')
                    elif "Minimum Credits:" in field_name:
                        update_field(session, course, 'credits_min', int(field_value), 'official')
                    elif "Maximum Credits:" in field_name:
                        update_field(session, course, 'credits_max', int(field_value), 'official')

    session.commit()
    session.close()
    print("Official site scrape completed.")


def update_field(session, course, field_name, new_value, new_source):
    """Helper function to update a field, log conflicts, and update the source."""
    existing_value = getattr(course, field_name)
    existing_source_obj = session.query(CourseSource).filter_by(course_id=course.id, field_name=field_name).first()
    existing_source = existing_source_obj.source if existing_source_obj else None

    print(f"    Updating field: {field_name}")
    print(f"      Existing value: {existing_value} (Source: {existing_source})")
    print(f"      New value: {new_value} (Source: {new_source})")

    if existing_source != new_source and str(existing_value) != str(new_value):
        print(f"      Conflict detected for {course.code} - {field_name}.")
        conflict = DataConflict(
            course_id=course.id,
            field_name=field_name,
            wiki_value=str(existing_value) if existing_source == 'wiki' else None,
            official_value=str(new_value) if new_source == 'official' else None,
        )
        session.add(conflict)

    setattr(course, field_name, new_value)
    if not existing_source_obj:
        existing_source_obj = CourseSource(course_id=course.id, field_name=field_name, source=new_source)
        session.add(existing_source_obj)
    else:
        existing_source_obj.source = new_source

if __name__ == '__main__':
    scrape_official_site()
