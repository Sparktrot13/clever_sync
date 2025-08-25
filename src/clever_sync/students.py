from oneroster_api import User, Demographics


def build_student_data(user_list: list[User], enrollment_data: list[dict]) -> list[dict]: 
    return [
        {
            "School_id": "", # replace with function
            "Student_id": user.identifier,
            "Student_number": user.sourced_id,
            "State_id": user.state_id,
            "Last_name": user.last_name,
            "Middle_name": user.middle_name,
            "First_name": user.first_name,
            "Preferred_last_name": user.preferred_last_name,
            "Preferred_first_name": user.preferred_first_name,
            "Grade": user.grades,
            "DOB": "", # replace with function
            "Student_email": "", # replace with function
            "Username": ""
        } for user in user_list if user.role == "student"
    ]

def student_data(student: User, enrollment_data: list[dict], demographic_data: list[Demographics]) -> dict:
    student.email = check_email(student.email)