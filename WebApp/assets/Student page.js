let menuicn = document.querySelector(".menuicn");
let nav = document.querySelector(".navcontainer");

menuicn.addEventListener("click", () => {
    nav.classList.toggle("navclose");
})



function loadContent(page) {
    const contentArea = document.getElementById('content');



    if (page === 'option1') {
        contentArea.innerHTML =
        `<div class="searchbar2">
            <input type="text" 
                name="" 
                id="" 
                placeholder="Search">
            <div class="searchbtn">
                <img src="https://media.geeksforgeeks.org/wp-content/uploads/20221210180758/Untitled-design-(28).png"
                class="icn srchicn" 
                lt="search-button">
                </div>
            </div>

            <div class="box-container">

                <div class="box box1">
                    <div class="text">
                        <h2 class="topic-heading">John Doe</h2>
                        <h2 class="topic">Student</h2>
                    </div>

                    <!-- <img src="https://media.geeksforgeeks.org/wp-content/uploads/20221210184645/Untitled-design-(31).png"
                        alt="Views"> -->
                </div>

                <div class="box box2">
                    <div class="text">
                        <h2 class="topic-heading">Computer Science</h2>
                        <h2 class="topic">Program</h2>
                    </div>

                    <!-- <img src="https://media.geeksforgeeks.org/wp-content/uploads/20221210185030/14.png" 
                         alt="likes"> -->
                </div>

                <div class="box box3">
                    <div class="text">
                        <h2 class="topic-heading">3.6</h2>
                        <h2 class="topic">GPA</h2>
                    </div>

                    <!-- <img src="https://media.geeksforgeeks.org/wp-content/uploads/20221210184645/Untitled-design-(32).png"

                        alt="comments"> -->
                </div>

                <div class="box box4">
                    <div class="text">
                        <h2 class="topic-heading">3</h2>
                        <h2 class="topic">Current Classes</h2>
                    </div>
                </div>
            </div>
<br>

<div class="profile-card">
            <div class="tab-nav">
                <a href="#" class="active" id="tab-profile">Profile</a>
                <a href="#" id="tab-emergency">Emergency Contacts</a>
                <a href="#" id="tab-program">Program Details</a>
            </div>

            <div class="profile-section" id="profile-section">
                <h2>Personal Information</h2>
                <div class="info-row">
                    <div class="info-label">First Name:</div>
                    <div class="info-value">John</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Last Name:</div>
                    <div class="info-value">Doe</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Email:</div>
                    <div class="info-value">john.doe@example.com</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Phone:</div>
                    <div class="info-value">123-456-7890</div>
                </div>
                <div class="info-row">
                    <div class="info-label">Address:</div>
                    <div class="info-value">123 Drive</div>
                </div>
               
            </div>

            <div class="profile-section" id="emergency-section" style="display: none;">
                <h2>Emergency Contacts</h2>
                 <div class="info-row">
                <div class="info-label">Name:</div>
                <div class="info-value">Jane Doe</div>
            </div>
            <div class="info-row">
                <div class="info-label">Contact:</div>
                <div class="info-value">987-654-3210</div>
            </div>
            <div class="info-row">
                <div class="info-label">Relationship:</div>
                <div class="info-value">Sister</div>
            </div>
            </div>

            <div class="profile-section" id="program-section" style="display: none;">
                <h2>Program Details</h2>
                <div class="info-row">
                <div class="info-label">Program Name:</div>
                <div class="info-value">Computer Science</div>
            </div>
            <div class="info-row">
                <div class="info-label">Advisor:</div>
                <div class="info-value">Dr. Smith</div>
            </div>
            <div class="info-row">
                <div class="info-label">Start Date:</div>
                <div class="info-value">September 1, 2022</div>
            </div>
            <div class="info-row">
                <div class="info-label">GPA:</div>
                <div class="info-value">3.8</div>
        </div>

            </div>
        </div>

<br>


            <!-- DataTable Section -->
            <div class="dataTable-container">
                <h2>Class Schedule</h2>
                <table id="classSchedule">
                    <thead>
                        <tr>
                            <th>Course</th>
                            <th>Code</th>
                            <th>Lecturer</th>
                            <th>Day</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Introduction to Programming</td>
                            <td>CS101</td>
                            <td>Dr. Jane Smith</td>
                            <td>Mon</td>
                            <td>09:00 AM</td>
                        </tr>
                        <tr>
                            <td>Database Systems</td>
                            <td>CS202</td>
                            <td>Dr. John Doe</td>
                            <td>Tue</td>
                            <td>10:30 AM</td>
                        </tr>
                        <tr>
                            <td>Software Engineering</td>
                            <td>CS303</td>
                            <td>Prof. Emily Clark</td>
                            <td>Wed</td>
                            <td>01:00 PM</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>`
        $(document).ready(function () {
            $('#classSchedule').DataTable();


            // Add tab functionality
        document.getElementById('tab-profile').addEventListener('click', function () {
            showSection('profile-section');
            setActiveTab(this);
        });

        document.getElementById('tab-emergency').addEventListener('click', function () {
            showSection('emergency-section');
            setActiveTab(this);
        });

        document.getElementById('tab-program').addEventListener('click', function () {
            showSection('program-section');
            setActiveTab(this);
        });
        });
    
    }
        // Add tab functionality
        document.getElementById('tab-profile').addEventListener('click', function () {
            showSection('profile-section');
            setActiveTab(this);
        });

        document.getElementById('tab-emergency').addEventListener('click', function () {
            showSection('emergency-section');
            setActiveTab(this);
        });

        document.getElementById('tab-program').addEventListener('click', function () {
            showSection('program-section');
            setActiveTab(this);
        });
    }


// Function to display the correct section
function showSection(sectionId) {
    document.querySelectorAll('.profile-section').forEach(function (section) {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

// Function to highlight the active tab
function setActiveTab(tab) {
    document.querySelectorAll('.tab-nav a').forEach(function (tab) {
        tab.classList.remove('active');
    });
    tab.classList.add('active');
}


// Initialize with Dashboard content
loadContent('dashboard');