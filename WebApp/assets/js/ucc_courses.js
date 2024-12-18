document.addEventListener('DOMContentLoaded', function () {
    // Initialize DataTable
    const table = $('#coursesTable').DataTable({
        pageLength: 10,
        lengthMenu: [5, 10, 20, 50],
        responsive: true,
        language: {
            search: "Search Courses:",
            lengthMenu: "Show _MENU_ rows per page",
        }
    });

    // Fetch courses and populate the table
    async function fetchCourses() {
        try {
            const response = await fetch('http://127.0.0.1:8000/courses/get_courses');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const courses = await response.json();
            console.log("Fetched Courses:", courses);

            // Populate DataTable
            courses.forEach(course => {
                table.row.add([
                    course.id,
                    course.course_code,
                    course.course_title,
                    course.course_credits,
                    course.degree_level_id,
                    course.description,
                    course.active,
                    course.date_added
                ]).draw(false);
            });
        } catch (error) {
            console.error("Error fetching courses:", error);
            alert("Failed to load courses. Please try again.");
        }
    }

    // Show Add Course Modal
    window.showAddCourseForm = function () {
        document.getElementById("addCourseModal").style.display = "block";
    };

    // Close Modal
    window.closeModal = function () {
        document.getElementById("addCourseModal").style.display = "none";
    };

    // Add Course Functionality
    window.addCourse = function () {
        const courseCode = document.getElementById("courseCode").value;
        const courseName = document.getElementById("courseName").value;
        const credits = document.getElementById("credits").value;
        const degreeLevel = document.getElementById("degreeLevel").value;
        const prerequisites = document.getElementById("prerequisites").value;

        if (courseCode && courseName && credits && degreeLevel) {
            table.row.add([
                'New', // Temporary ID
                courseCode,
                courseName,
                credits,
                degreeLevel,
                prerequisites,
                'Yes',
                new Date().toLocaleDateString()
            ]).draw(false);

            alert("Course added successfully!");
            closeModal();
        } else {
            alert("Please fill out all required fields.");
        }
    };

    // Close modal when clicking outside
    window.onclick = function (event) {
        const modal = document.getElementById("addCourseModal");
        if (event.target === modal) {
            closeModal();
        }
    };

    // Fetch courses on load
    fetchCourses();
});
