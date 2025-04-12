function signup(event) {
  event.preventDefault();

  const partner1 = document.getElementById("newPartner1").value;
  const partner2 = document.getElementById("newPartner2").value;
  const password = document.getElementById("newPassword").value;

  // Store user (just for demo – in real use, send to backend securely)
  localStorage.setItem(
    "gfai_user",
    JSON.stringify({ partner1, partner2, password })
  );

  document.getElementById("signupMessage").textContent =
    "Account created! You can now log in 💘";

  // Redirect after short delay (optional)
  setTimeout(() => {
    window.location.href = "index.html";
  }, 1500);
}
