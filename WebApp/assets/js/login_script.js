const container = document.querySelector(".container"),
  pwShowHide = document.querySelectorAll(".showHidePw"),
  pwFields = document.querySelectorAll(".password"),
  signUp = document.querySelector(".signup-link"),
  login = document.querySelector(".login-link");

// js code to show/hide password and change icon
pwShowHide.forEach((eyeIcon) => {
  eyeIcon.addEventListener("click", () => {
    pwFields.forEach((pwField) => {
      if (pwField.type === "password") {
        pwField.type = "text";

        pwShowHide.forEach((icon) => {
          icon.classList.replace("uil-eye-slash", "uil-eye");
        });
      } else {
        pwField.type = "password";

        pwShowHide.forEach((icon) => {
          icon.classList.replace("uil-eye", "uil-eye-slash");
        });
      }
    });
  });
});

// js code to appear signup and login form
signUp.addEventListener("click", (e) => {
  e.preventDefault();
  container.classList.add("active");
});

login.addEventListener("click", (e) => {
  e.preventDefault();
  container.classList.remove("active");
});



// Login a donor
// Get the form element
const loginForm = document.getElementById('adminLoginForm');

// Add an event listener for form submission
loginForm.addEventListener('submit', async (event) => {
  event.preventDefault(); // Prevent the default form submission behavior

  // Get the form data
  const formData = new FormData(loginForm);
  const username = formData.get('username');
  const password = formData.get('password');

  try {
    // Send a POST request to the /donor_login endpoint
    const response = await fetch('http://127.0.0.1:8000/admin_login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
    });

    // Check if the response was successful
    if (response.ok) {
      // Parse the response data as JSON
      const data = await response.json();

      // Handle the response data (e.g., store the token, redirect to another page)
      const token = data.access_token;
      console.log('Access Token:', token);
      // You can store the token in localStorage or a cookie for future use
      localStorage.setItem('accessToken', token);

      // Optionally, you can redirect the user to another page after successful login
      window.location.href = 'http://localhost:63342/UCCRegistry/WebApp/UCCRegistryHome.html?_ijt=dhk6fjjm1d3klosgkdkmf7u6ru&_ij_reload=RELOAD_ON_SAVE';
    } else {
      // Handle the error response
      const errorData = await response.json();
      console.error('Login error:', errorData.detail);
      // Display an error message to the user
      alert(errorData.detail);
    }
  } catch (error) {
    console.error('Error occurred during login:', error);
    // Display an error message to the user
    alert('An error occurred during login. Please try again.');
  }
});
