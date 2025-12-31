from librarian.app import Librarian

librarian = Librarian()

def create_curriculum() -> None:
    user_query = input("Enter your learning goals: ")
    plan = librarian.recommend_curriculum(user_query)
    return plan

if __name__ == "__main__":
    create_curriculum()
