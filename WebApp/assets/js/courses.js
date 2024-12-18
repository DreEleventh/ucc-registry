

document.addEventListener("DOMContentLoaded", async function () {
    const coursesTableBody = document.querySelector("#coursesTable tbody");

    // Mapping of degree level IDs to codes
    const degreeLevelMapping = {
        1: "UG", // Undergraduate
        2: "GR", // Graduate
        3: "DR"  // Doctorate
    };

    // Function to fetch courses and populate the table
    async function fetchAndPopulateCourses() {
        try {
            console.log("Fetching courses...");
            const response = await fetch("http://127.0.0.1:8000/courses/get_courses");
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const courses = await response.json();
            console.log("Courses fetched:", courses);

            // Clear existing rows
            coursesTableBody.innerHTML = "";

            // Populate the table with fetched data
            courses.forEach(course => {
                const degreeLevelCode = degreeLevelMapping[course.degree_level_id] || "Unknown"; // Fallback for unmapped IDs

                const row = document.createElement("tr");
                
                row.innerHTML = `
                    <td>${course.id}</td>
                    <td>${course.course_code}</td>
                    <td>${course.course_title}</td>
                    <td>${course.course_credits}</td>
                    <td>${degreeLevelCode}</td> <!-- Translated degree level -->
                    <td>${course.description}</td>
                    <td>${course.active}</td>
                    <td>${new Date(course.date_added).toLocaleDateString()}</td>
                `;

                coursesTableBody.appendChild(row);
            });
        } catch (error) {
            console.error("Error fetching courses:", error);
            alert("There was an error loading courses. Please try again later.");
        }
    }

    // Fetch and populate courses on page load
    await fetchAndPopulateCourses();
});
