class Course:
    def __init__(self, course_code: str, course_name: str, credit_hours: int, level: str):
        self.course_code = course_code
        self.course_name = course_name
        self.credit_hours = credit_hours
        self.level = level  # "core" or "elective"

    def get_details(self) -> str:
        return (f"Code: {self.course_code} | Name: {self.course_name} | "
                f"Credits: {self.credit_hours} | Level: {self.level.capitalize()}")

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class Graph:
    def __init__(self):
        self.adj_list = {}

    def addVertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def addEdge(self, from_vertex, to_vertex):
        if from_vertex in self.adj_list and to_vertex in self.adj_list:
            if to_vertex not in self.adj_list[from_vertex]:
                self.adj_list[from_vertex].append(to_vertex)

    def listIncomingAdjacentVertex(self, target_vertex):
        incoming = []
        for v in self.adj_list:
            if target_vertex in self.adj_list[v]:
                incoming.append(v)
        return incoming

    def get_outgoing_edges(self, source_vertex):
        if source_vertex in self.adj_list:
            return self.adj_list[source_vertex]
        return []


def setup_prerequisite_system():
    # Create Course Objects
    c101 = Course("CS101", "Introduction to Programming", 3, "core")
    c201 = Course("CS201", "Data Structures", 4, "core")
    c301 = Course("CS301", "Algorithms", 4, "core")
    c302 = Course("CS302", "Database Systems", 3, "core")
    c401 = Course("CS401", "Software Engineering", 3, "core")
    c402 = Course("CS402", "Artificial Intelligence", 3, "elective")

    courses_dict = {
        "CS101": c101, "CS201": c201, "CS301": c301,
        "CS302": c302, "CS401": c401, "CS402": c402
    }

    # Populate Graph Vertices & Directed Edges
    graph = Graph()
    for code in courses_dict:
        graph.addVertex(code)

    # Directed Edge
    graph.addEdge("CS101", "CS201")
    graph.addEdge("CS201", "CS301")
    graph.addEdge("CS201", "CS302")
    graph.addEdge("CS301", "CS401")
    graph.addEdge("CS301", "CS402")

    return graph, courses_dict


def main():
    graph, courses = setup_prerequisite_system()

    while True:
        print("\n==== University Course Prerequisite System ====")
        print("1. View All Courses")
        print("2. View Course Details")
        print("3. View Prerequisites of a Course")
        print("4. View Courses Unlocked by a Course")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            print("\nAvailable Courses:")
            for idx, code in enumerate(courses, 1):
                print(f"{idx}. {courses[code]}")

        elif choice == '2':
            code = input("Enter Course Code: ").strip().upper()
            if code in courses:
                print(f"\nCourse Details:")
                print(courses[code].get_details())
            else:
                print("Course not found!")

        elif choice == '3':
            code = input("Enter Course Code: ").strip().upper()
            if code in courses:
                # Prerequisites
                prereqs = graph.listIncomingAdjacentVertex(code)
                print(f"\nPrerequisites for {courses[code]}:")
                if prereqs:
                    for p_code in prereqs:
                        print(f" - {courses[p_code]}")
                else:
                    print(" - None (No prerequisites required)")
            else:
                print("Course not found!")

        elif choice == '4':
            code = input("Enter Course Code: ").strip().upper()
            if code in courses:
                # Unlocked courses
                unlocked = graph.get_outgoing_edges(code)
                print(f"\nCourses unlocked by {courses[code]}:")
                if unlocked:
                    for u_code in unlocked:
                        print(f" - {courses[u_code]}")
                else:
                    print(" - None (Does not unlock any higher courses)")
            else:
                print("Course not found!")

        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice! Please select 1-5.")


if __name__ == "__main__":
    main()