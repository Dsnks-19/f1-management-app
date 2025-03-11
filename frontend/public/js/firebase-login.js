// Get auth instance
const auth = firebase.auth();

// Check auth state
auth.onAuthStateChanged(user => {
  const loginStatus = document.getElementById('login-status');
  const loginForm = document.getElementById('login-form');
  const logoutBtn = document.getElementById('logout-btn');
  const authRequiredElements = document.querySelectorAll('.auth-required');
  
  if (user) {
    // User is signed in
    if (loginStatus) {
      loginStatus.textContent = `Logged in as: ${user.email}`;
    }
    
    if (loginForm) {
      loginForm.style.display = 'none';
    }
    
    if (logoutBtn) {
      logoutBtn.style.display = 'block';
    }
    
    // Show auth required elements
    authRequiredElements.forEach(el => {
      el.style.display = 'block';
    });
    
    // Store the token in localStorage for API calls
    user.getIdToken().then(token => {
      localStorage.setItem('authToken', token);
    });
    
  } else {
    // User is signed out
    if (loginStatus) {
      loginStatus.textContent = 'Not logged in';
    }
    
    if (loginForm) {
      loginForm.style.display = 'block';
    }
    
    if (logoutBtn) {
      logoutBtn.style.display = 'none';
    }
    
    // Hide auth required elements
    authRequiredElements.forEach(el => {
      el.style.display = 'none';
    });
    
    // Remove token from localStorage
    localStorage.removeItem('authToken');
  }
});

// Sign in function
function signIn(email, password) {
  return auth.signInWithEmailAndPassword(email, password)
    .catch(error => {
      console.error("Error signing in:", error);
      throw error;
    });
}

// Sign up function
function signUp(email, password) {
  return auth.createUserWithEmailAndPassword(email, password)
    .catch(error => {
      console.error("Error signing up:", error);
      throw error;
    });
}

// Sign out function
function signOut() {
  return auth.signOut()
    .catch(error => {
      console.error("Error signing out:", error);
      throw error;
    });
}

// Event listeners for forms (if they exist on the page)
document.addEventListener('DOMContentLoaded', () => {
  const loginFormElement = document.getElementById('login-form');
  
  if (loginFormElement) {
    loginFormElement.addEventListener('submit', e => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const isSignUp = document.getElementById('signup-mode').checked;
      
      if (isSignUp) {
        signUp(email, password)
          .then(() => {
            alert('Account created successfully!');
          })
          .catch(error => {
            alert(`Error: ${error.message}`);
          });
      } else {
        signIn(email, password)
          .then(() => {
            window.location.href = '/index.html';
          })
          .catch(error => {
            alert(`Error: ${error.message}`);
          });
      }
    });
  }
  
  const logoutBtn = document.getElementById('logout-btn');
  
  if (logoutBtn) {
    logoutBtn.addEventListener('click', () => {
      signOut()
        .then(() => {
          window.location.href = '/login.html';
        })
        .catch(error => {
          alert(`Error: ${error.message}`);
        });
    });
  }
});