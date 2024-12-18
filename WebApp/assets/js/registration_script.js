document.addEventListener('DOMContentLoaded', async function () {
    const form = document.getElementById('studentRegistrationForm');
    const emergencyContactsContainer = document.querySelector(".emergency.contacts .fields");

    if (!emergencyContactsContainer) {
        console.error("Emergency contacts container not found.");
        return;
    }

    // Add button to create new emergency contact
    const addEmergencyContactBtn = document.createElement('button');
    addEmergencyContactBtn.type = 'button';
    addEmergencyContactBtn.textContent = 'Add Emergency Contact';
    addEmergencyContactBtn.classList.add('add-emergency-contact');
    emergencyContactsContainer.appendChild(addEmergencyContactBtn);

    // Event listener for adding emergency contacts
    addEmergencyContactBtn.addEventListener('click', () => {
        addEmergencyContactField(emergencyContactsContainer);
    });

    // Populate programs dropdown
    await populateProgramsDropdown();

    // Handle form submission
    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the default form submission
        await handleStudentRegister(form);
    });
});


// Populate programs dropdown
async function populateProgramsDropdown() {
    const programSelect = document.getElementById('programs');
    if (!programSelect) {
        console.error("Programs dropdown not found.");
        return;
    }

    const loadingOption = document.createElement('option');
    loadingOption.textContent = 'Loading programs...';
    programSelect.appendChild(loadingOption);

    try {
        const response = await fetch('http://127.0.0.1:8000/programs/program_id_names');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const programs = await response.json();

        programSelect.innerHTML = '<option disabled selected>Select Program</option>';
        programs.forEach(program => {
            const option = document.createElement('option');
            option.value = program.id;
            option.textContent = program.program_name;
            programSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching programs:', error);
        programSelect.innerHTML = '<option disabled selected>Error loading programs</option>';
        alert('Error loading programs. Please refresh the page.');
    }
}

// Add emergency contact field
function addEmergencyContactField(container) {
    const newContactDiv = document.createElement('div');
    newContactDiv.classList.add('multiple-emergency-contact');
    newContactDiv.innerHTML = `
        <div class="input-field">
            <label>Contact Name</label>
            <input type="text" placeholder="Enter contact's name">
        </div>
        <div class="input-field">
            <label>Relationship</label>
            <input type="text" placeholder="Mother, Father...">
        </div>
        <div class="input-field">
            <label>Contact Number</label>
            <input type="number" placeholder="Enter contact number">
        </div>
        <button type="button" class="remove-contact">Remove Contact</button>
    `;

    newContactDiv.querySelector('.remove-contact').addEventListener('click', () => {
        container.removeChild(newContactDiv);
    });

    container.appendChild(newContactDiv);
}


// Handle form submission
async function handleStudentRegister(form) {
    const formData = new FormData(form);
    const emergencyContacts = Array.from(document.querySelectorAll('.multiple-emergency-contact')).map(contactDiv => ({
        contact_person_name: contactDiv.querySelector('input[placeholder="Enter contact\'s name"]').value,
        relation: contactDiv.querySelector('input[placeholder="Mother, Father..."]').value,
        contact_number: contactDiv.querySelector('input[placeholder="Enter contact number"]').value,
    }));

    const studentData = {
        first_name: formData.get('first_name'),
        middle_name: formData.get('middle_name'),
        last_name: formData.get('last_name'),
        program_of_study_id: formData.get('programs'),
        contact_details: {
            personal_email: formData.get('personal_email'),
            mobile_number: formData.get('mobile_number'),
            home_number: formData.get('home_number'),
            work_number: formData.get('work_number'),
            home_address: formData.get('home_address'),
        },
        student_credentials: {
            password: formData.get('password'),
        },
        emergency_contacts: emergencyContacts,
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/students/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(studentData),
        });

        if (response.ok) {
            const result = await response.json();
            alert('Student registered successfully!');
            console.log('Registration successful:', result);
        } else {
            const errorResponse = await response.json();
            console.error('Error registering student:', errorResponse);
            alert(`Error: ${errorResponse.detail || 'An error occurred during registration.'}`);
        }
    } catch (error) {
        console.error('Error during registration:', error);
        alert('An error occurred. Please try again later.');
    }
}