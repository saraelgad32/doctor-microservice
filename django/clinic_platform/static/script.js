document.addEventListener('DOMContentLoaded', function() {
    // User management functions
    function getUsers() {
        const users = localStorage.getItem('users');
        return users ? JSON.parse(users) : {};
    }

    function saveUsers(users) {
        localStorage.setItem('users', JSON.stringify(users));
    }

    function getCurrentUser() {
        return localStorage.getItem('currentUser');
    }

    function setCurrentUser(email) {
        localStorage.setItem('currentUser', email);
    }

    function logout() {
        localStorage.removeItem('currentUser');
        updateAuthLinks();
        window.location.href = 'index.html';
    }

    function updateAuthLinks() {
        const authLinks = document.getElementById('auth-links');
        if (authLinks) {
            const currentUser = getCurrentUser();
            if (currentUser) {
                authLinks.innerHTML = '<a class="nav-link" href="profile.html">Profil</a> <a class="nav-link" href="#" id="logout-link">Déconnexion</a>';
                document.getElementById('logout-link').addEventListener('click', function(e) {
                    e.preventDefault();
                    logout();
                });
            } else {
                authLinks.innerHTML = '<a class="nav-link" href="login.html">Connexion</a>';
            }
        }
    }

    // Auth form on reservation.html
    const authForm = document.getElementById('authForm');
    if (authForm) {
        let isNewUser = false;
        authForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const email = document.getElementById('authEmail').value;
            const users = getUsers();

            if (!users[email]) {
                // New user: show password field to create account
                document.getElementById('password-field').style.display = 'block';
                document.getElementById('auth-button').textContent = 'Créer Compte';
                isNewUser = true;
                alert('Email non trouvé. Veuillez entrer un mot de passe pour créer un compte.');
            } else {
                // Existing user: show password field to login
                document.getElementById('password-field').style.display = 'block';
                document.getElementById('auth-button').textContent = 'Se connecter';
                isNewUser = false;
            }
        });

        // Handle password submission
        document.getElementById('authPassword').addEventListener('input', function() {
            if (this.value.length > 0) {
                document.getElementById('auth-button').textContent = isNewUser ? 'Créer Compte' : 'Se connecter';
            }
        });

        // Re-submit after password
        authForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const email = document.getElementById('authEmail').value;
            const password = document.getElementById('authPassword').value;
            const users = getUsers();

            if (isNewUser) {
                // Create new account
                users[email] = { password: password, name: '', phone: '' };
                saveUsers(users);
                setCurrentUser(email);
                alert('Compte créé avec succès!');
                document.getElementById('auth-section').style.display = 'none';
                document.getElementById('booking-section').style.display = 'block';
                updateAuthLinks();
            } else {
                // Login existing user
                if (users[email] && users[email].password === password) {
                    setCurrentUser(email);
                    alert('Connexion réussie!');
                    document.getElementById('auth-section').style.display = 'none';
                    document.getElementById('booking-section').style.display = 'block';
                    updateAuthLinks();
                } else {
                    alert('Mot de passe incorrect.');
                }
            }
        });
    }

    // Profile page
    if (window.location.pathname.includes('profile.html')) {
        const currentUser = getCurrentUser();
        if (!currentUser) {
            window.location.href = 'login.html';
        } else {
            const users = getUsers();
            const user = users[currentUser];
            const profileInfo = document.getElementById('profile-info');
            profileInfo.innerHTML = `
                <h3>Informations du Profil</h3>
                <p><strong>Email:</strong> ${currentUser}</p>
                <p><strong>Nom:</strong> ${user.name || 'Non défini'}</p>
                <p><strong>Téléphone:</strong> ${user.phone || 'Non défini'}</p>
                <h4 class="mt-4">Historique des Rendez-vous</h4>
            `;
            if (user.appointments && user.appointments.length > 0) {
                profileInfo.innerHTML += '<ul class="list-group">';
                user.appointments.forEach((appt, index) => {
                    profileInfo.innerHTML += `
                        <li class="list-group-item">
                            <strong>${appt.doctor}</strong> - ${appt.date} à ${appt.time}<br>
                            <small class="text-muted">${appt.reason}</small>
                            <span class="badge bg-${appt.status === 'confirmed' ? 'success' : 'secondary'}">${appt.status}</span>
                        </li>
                    `;
                });
                profileInfo.innerHTML += '</ul>';
            } else {
                profileInfo.innerHTML += '<p>Aucun rendez-vous passé.</p>';
            }
        }
    }

    // Update auth links on page load
    updateAuthLinks();

    // Quick booking form on home page
    const quickBookingForm = document.getElementById('quickBookingForm');
    if (quickBookingForm) {
        quickBookingForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const name = document.getElementById('quickName').value;
            const email = document.getElementById('quickEmail').value;
            const phone = document.getElementById('quickPhone').value;
            const doctor = document.getElementById('quickDoctor').value;
            const date = document.getElementById('quickDate').value;
            const time = document.getElementById('quickTime').value;

            if (!name || !email || !phone || !doctor || !date || !time) {
                alert('Veuillez remplir tous les champs.');
                return;
            }

            alert(`Rendez-vous réservé avec succès!\n\nNom: ${name}\nEmail: ${email}\nTéléphone: ${phone}\nMédecin: ${doctor}\nDate: ${date}\nHeure: ${time}`);
            quickBookingForm.reset();
        });
    }

    // Full booking form on reservation page
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const phone = document.getElementById('phone').value;
            const doctor = document.getElementById('doctor').value;
            const date = document.getElementById('date').value;
            const time = document.getElementById('time').value;
            const currentUser = getCurrentUser();

            if (!name || !email || !phone || !doctor || !date || !time) {
                alert('Veuillez remplir tous les champs.');
                return;
            }

            // Update user profile with booking info
            const users = getUsers();
            if (users[currentUser]) {
                users[currentUser].name = name;
                users[currentUser].phone = phone;
                saveUsers(users);
            }

            alert(`Rendez-vous réservé avec succès!\n\nNom: ${name}\nEmail: ${email}\nTéléphone: ${phone}\nMédecin: ${doctor}\nDate: ${date}\nHeure: ${time}`);
            bookingForm.reset();
        });
    }

    // Contact form
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            alert('Merci pour votre message. Nous vous contacterons bientôt!');
            contactForm.reset();
        });
    }
});
