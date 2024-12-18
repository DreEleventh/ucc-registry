// let menuicn = document.querySelector(".menuicn");
// let nav = document.querySelector(".navcontainer");

// menuicn.addEventListener("click", () => {
//     nav.classList.toggle("navclose");
// })


// function loadContent(page) {
//     const contentArea = document.getElementById('content');
//     if (page === 'dashboard') {
//         contentArea.innerHTML =`<div class="searchbar2">
//                 <input type="text" 
//                        name="" 
//                        id="" 
//                        placeholder="Search">
//                 <div class="searchbtn">
//                   <img src="https://media.geeksforgeeks.org/wp-content/uploads/20221210180758/Untitled-design-(28).png"
//                         class="icn srchicn" 
//                         alt="search-button">
//                   </div>
//             </div>

//             <div class="box-container">

//                 <div class="box box1">
//                     <div class="text">
//                         <h2 class="topic-heading">Andre McKenzie</h2>
//                         <h2 class="topic">Lecturer</h2>
//                     </div>

//                     <!-- <img src="https://media.geeksforgeeks.org/wp-content/uploads/20221210184645/Untitled-design-(31).png"
//                         alt="Views"> -->
//                 </div>

//                 <div class="box box2">
//                     <div class="text">
//                         <h2 class="topic-heading">I T</h2>
//                         <h2 class="topic">Department</h2>
//                     </div>

//                     <!-- <img src="https://media.geeksforgeeks.org/wp-content/uploads/20221210185030/14.png" 
//                          alt="likes"> -->
//                 </div>

//                 <div class="box box3">
//                     <div class="text">
//                         <h2 class="topic-heading">2</h2>
//                         <h2 class="topic">Courses Taught</h2>
//                     </div>

//                     <!-- <img src="https://media.geeksforgeeks.org/wp-content/uploads/20221210184645/Untitled-design-(32).png"

//                         alt="comments"> -->
//                 </div>
//                 </div>
//             </div>
// <br><br><br>




// <div class="profile-card">
//         <div class="tab-nav">
//             <a href="#" class="active" id="tab-profile">Profile</a>
//             <a href="#" id="tab-emergency">Emergency Contacts</a>
//             <a href="#" id="tab-program">Department Information</a>
//         </div>

//         <div class="profile-section" id="profile-section">
//             <h2>Personal Information</h2>
//             <div class="info-row">
//                 <div class="info-label">First Name:</div>
//                 <div class="info-value">Andre</div>
//             </div>
//             <div class="info-row">
//                 <div class="info-label">Last Name:</div>
//                 <div class="info-value">McKenzie</div>
//             </div>
//             <div class="info-row">
//                 <div class="info-label">Email:</div>
//                 <div class="info-value">andre@example.com</div>
//             </div>
//             <div class="info-row">
//                 <div class="info-label">Phone:</div>
//                 <div class="info-value">123-456-7890</div>
//             </div>
//             <div class="info-row">
//                 <div class="info-label">Address:</div>
//                 <div class="info-value">123 Drive</div>
//             </div>
//         </div>

//         <div class="profile-section" id="emergency-section" style="display: none;">
//             <h2>Emergency Contacts</h2>
//              <div class="info-row">
//             <div class="info-label">Name:</div>
//             <div class="info-value">Jane Doe</div>
//         </div>
//         <div class="info-row">
//             <div class="info-label">Contact:</div>
//             <div class="info-value">987-654-3210</div>
//         </div>
//         <div class="info-row">
//             <div class="info-label">Relationship:</div>
//             <div class="info-value">Sister</div>
//         </div>
//         </div>

//         <div class="profile-section" id="program-section" style="display: none;">
//             <h2>Department Information</h2>
//             <div class="info-row">
//             <div class="info-label">Department:</div>
//             <div class="info-value">Information  Technologye</div>
//         </div>
//         <div class="info-row">
//             <div class="info-label">Head of Department:</div>
//             <div class="info-value">Otis Osbourne</div>
//         </div>
//         <div class="info-row">
//             <div class="info-label">Start Date:</div>
//             <div class="info-value">September 1, 2022</div>
//         </div>
//         <div class="info-row">
//             <div class="info-label">Dean:</div>
//             <div class="info-value">John Doe</div>
//     </div>

//         </div>
//     </div>

// <br>









//             <!-- DataTable Section -->
//             <div class="dataTable-container">
//                 <h2>Andre's Courses</h2>
//                 <table id="classSchedule">
//                     <thead>
//                         <tr>
//                             <th>Course</th>
//                             <th>Code</th>
//                             <th>Day</th>
//                             <th>Time</th>
//                             <th>Student</th>
//                         </tr>
//                     </thead>
//                     <tbody>
//                         <tr>
//                             <td>Introduction to Programming</td>
//                             <td>CS101</td>
//                             <td>Mon</td>                            
//                             <td>09:00 AM</td>
//                             <td>30</td>
//                         </tr>
//                         <tr>
//                             <td>Software Engineering</td>
//                             <td>CS303</td>
//                             <td>Wed</td>
//                             <td>01:00 PM</td>
//                             <td>25</td>
//                         </tr>
//                     </tbody>
//                 </table>
//             </div>`
       
//         $(document).ready(function () {
//             $('#classSchedule').DataTable();
//         });

              
    

//         // Add tab functionality
//         document.getElementById('tab-profile').addEventListener('click', function () {
//             showSection('profile-section');
//             setActiveTab(this);
//         });

//         document.getElementById('tab-emergency').addEventListener('click', function () {
//             showSection('emergency-section');
//             setActiveTab(this);
//         });

//         document.getElementById('tab-program').addEventListener('click', function () {
//             showSection('program-section');
//             setActiveTab(this);
//         });
//     }
// }

//     // Function to display the correct section
//     function showSection(sectionId) {
//         document.querySelectorAll('.profile-section').forEach(function (section) {
//             section.style.display = 'none';
//         });
//         document.getElementById(sectionId).style.display = 'block';
//     }

//     // Function to highlight the active tab
//     function setActiveTab(tab) {
//         document.querySelectorAll('.tab-nav a').forEach(function (tab) {
//             tab.classList.remove('active');
//         });
//         tab.classList.add('active');
//     }




//     function openGradeInput(courseCode) {
//         const contentArea = document.getElementById("content");
//         contentArea.innerHTML = `
//             <div class="dataTable-container">
//                 <h2>Enter Grades for <span id="course-code"></span></h2>
//                 <table id="gradeTable">
//                     <thead>
//                         <tr>
//                             <th>Student ID</th>
//                             <th>Name</th>
//                             <th>Grade</th>
//                         </tr>
//                     </thead>
//                     <tbody>
//                         <tr>
//                             <td>2021001</td>
//                             <td>John Doe</td>
//                             <td><input type="text" placeholder="Enter grade" /></td>
//                         </tr>
//                         <tr>
//                             <td>2021002</td>
//                             <td>Jane Smith</td>
//                             <td><input type="text" placeholder="Enter grade" /></td>
//                         </tr>
//                     </tbody>
//                 </table>
//                 <button onclick="submitGrades()">Submit Grades</button>
//                 <button onclick="loadContent('dashboard')">Cancel</button>
//             </div>
//         `;
    
//         document.getElementById("course-code").innerText = courseCode;
    
//         $(document).ready(function () {
//             $('#gradeTable').DataTable();
//         });
//     }
    




// function submitGrades() {
//     alert("Grades submitted successfully!");
//     loadContent('dashboard'); // Return to dashboard after submission
// }

// // Initialize with Dashboard content
// loadContent('dashboard');