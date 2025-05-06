/**
 * popup.js
 *
 * Shows either:
 *  - A login/register form, or
 *  - A “you’re logged in” view with logout.
 */

const BACKEND_BASE_URL = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", () => {
  const form      = document.getElementById("authForm");
  const feedback  = document.getElementById("feedback");
  const loggedIn  = document.getElementById("loggedIn");
  const userEmail = document.getElementById("userEmail");
  const logoutBtn = document.getElementById("logoutBtn");

  // Switch to logged-in view
  function showLoggedIn(email) {
    form.style.display = "none";
    feedback.textContent = "";
    userEmail.textContent = email;
    loggedIn.style.display = "block";
  }

  // Switch to auth form
  function showLoginForm() {
    loggedIn.style.display = "none";
    form.style.display = "block";
  }

  // Check if we have a token stored
  chrome.storage.local.get(["token","user_id","email"], ({ token, user_id, email }) => {
    if (token && user_id && email) {
      showLoggedIn(email);
    } else {
      showLoginForm();
    }
  });

  // Handle logout
  logoutBtn.addEventListener("click", () => {
    chrome.storage.local.clear(() => {
      showLoginForm();
    });
  });

  // Handle login/register form submit
  form.addEventListener("submit", async event => {
    event.preventDefault();
    feedback.textContent = "Processing…";

    const emailVal    = form.email.value.trim();
    const passwordVal = form.password.value;
    if (!emailVal || !passwordVal) {
      feedback.textContent = "Please enter both email and password.";
      return;
    }

    try {
      // 1) Login
      let resp = await fetch(`${BACKEND_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: emailVal, password: passwordVal })
      });

      // 2) If 401, register and re-login
      if (resp.status === 401) {
        const regResp = await fetch(`${BACKEND_BASE_URL}/auth/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: emailVal, password: passwordVal })
        });
        // If register fails for another reason, throw
        if (!regResp.ok) {
          const errText = await regResp.text();
          if (!errText.includes("already exists")) {
            throw new Error(`Register failed: ${errText}`);
          }
        }
        // Re-login
        resp = await fetch(`${BACKEND_BASE_URL}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: emailVal, password: passwordVal })
        });
      }

      if (!resp.ok) {
        throw new Error(`Login failed (${resp.status})`);
      }

      // 3) Parse out token, user_id, email
      const { access_token, user_id } = await resp.json();
      if (!access_token || !user_id) {
        throw new Error("Login did not return both access_token and user_id");
      }

      // 4) Store for SW
      chrome.storage.local.set(
        { token: access_token, user_id: user_id, email: emailVal },
        () => {
          showLoggedIn(emailVal);
        }
      );

    } catch (err) {
      console.error(err);
      feedback.textContent = `Error: ${err.message}`;
    }
  });
});
