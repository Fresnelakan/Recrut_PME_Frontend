document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");

    // 🔐 Connexion
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const email = document.getElementById("login-email").value;
            const password = document.getElementById("login-password").value;
            const role = document.getElementById("login-role").value;

            try {
                const response = await fetch("http://127.0.0.1:8001/api/auth/login/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ email, password, role }),
                });

                const data = await response.json();

                if (response.ok) {
                    alert("Connexion réussie !");
                    // Tu peux stocker le token ici
                    localStorage.setItem("auth_token", data.token);
                    window.location.href = "/dashboard/"; // redirection
                } else {
                    alert(data.message || "Échec de connexion.");
                }
            } catch (err) {
                console.error(err);
                alert("Erreur réseau.");
            }
        });
    }

    // 📝 Inscription
    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();

            const email = document.getElementById("register-email").value;
            const password = document.getElementById("register-password").value;
            const role = document.getElementById("register-role").value;

            try {
                const response = await fetch("http://127.0.0.1:8001/api/auth/register/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ email, password, role }),
                });

                const data = await response.json();

                if (response.ok) {
                    alert("Inscription réussie !");
                    window.location.href = "/login.html";
                } else {
                    alert(data.message || "Échec de l’inscription.");
                }
            } catch (err) {
                console.error(err);
                alert("Erreur réseau.");
            }
        });
    }
});
