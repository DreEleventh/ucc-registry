document.addEventListener("DOMContentLoaded", async function () {
    const studentsTableBody = document.querySelector("#studentsTable tbody");

    // Function to fetch students and populate the table
    async function fetchAndPopulateStudents() {
        try {
            console.log("Fetching students...");
            const response = await fetch("http://127.0.0.1:8000/students/all-student-info");

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const students = await response.json();
            console.log("Students fetched:", students);

            // Clear existing rows
            studentsTableBody.innerHTML = "";

            // Populate the table with fetched data
            students.forEach(student => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${student.student_id}</td>
                    <td>${student.first_name}</td>
                    <td>${student.middle_name || ""}</td>
                    <td>${student.last_name}</td>
                    <td>${new Date(student.date_registered).toLocaleDateString()}</td>
                    <td>${student.gpa !== null ? student.gpa : "N/A"}</td>
                `;

                studentsTableBody.appendChild(row);
            });
        } catch (error) {
            console.error("Error fetching students:", error);
            alert("There was an error loading student data. Please try again later.");
        }
    }

    // Fetch and populate students on page load
    await fetchAndPopulateStudents();
});
