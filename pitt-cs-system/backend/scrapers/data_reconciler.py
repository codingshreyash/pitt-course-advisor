
from backend.database.courses_db import CoursesDatabase
from backend.database.models import Course, DataConflict

def reconcile_data():
    """Reconciles data from different sources based on predefined rules."""
    print("Starting data reconciliation...")

    db = CoursesDatabase()
    session = db.get_session()

    unresolved_conflicts = session.query(DataConflict).filter_by(resolved=False).all()

    if not unresolved_conflicts:
        print("No unresolved conflicts found.")
        return

    print(f"Found {len(unresolved_conflicts)} unresolved conflicts to reconcile.")

    for conflict in unresolved_conflicts:
        course = session.query(Course).filter_by(id=conflict.course_id).first()
        if not course:
            print(f"  Skipping conflict for non-existent course with id {conflict.course_id}")
            continue

        print(f"  Reconciling {conflict.field_name} for {course.code}")

        winning_source = None
        winning_value = None

        # Apply reconciliation rules from README.md
        if conflict.field_name in ['credits_min', 'credits_max', 'prerequisites', 'title']:
            winning_source = 'official'
            winning_value = conflict.official_value
        elif conflict.field_name == 'description':
            winning_source = 'wiki'
            winning_value = conflict.wiki_value
        else:
            # Default to official source if no rule is defined
            winning_source = 'official'
            winning_value = conflict.official_value

        if winning_value is not None:
            print(f"    Winning source: {winning_source}, Value: {winning_value}")
            setattr(course, conflict.field_name, winning_value)
        
        conflict.resolved = True

    session.commit()
    session.close()
    print("Data reconciliation completed.")

if __name__ == '__main__':
    reconcile_data()
