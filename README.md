# Resume2Web

#### Video Demo: <URL HERE>

#### Description:

Resume2Web is a web application that allows users to turn a résumé into a clean, shareable website. Users can create an account, log in, enter their résumé information, and generate a webpage that can optionally be published using a unique share link.

The motivation for this project came from noticing that many résumé builders either cost money or require technical knowledge. This tool keeps things simple and free, while still giving control to the user.

The application is built using Flask (Python), SQLite for storage, HTML/CSS/Bootstrap for styling, and Jinja templates for rendering pages dynamically.

---

### Features

- User registration and login
- Secure password hashing
- Ability to create multiple résumés per user
- Dashboard displaying user résumés
- Public shareable résumé links
- Session-based authentication
- Clean Bootstrap UI

---

### Technical Design

The database contains two main tables:

- `users` — stores accounts and hashed passwords
- `resumes` — stores résumé data and references users via `user_id`

Flask handles routing, sessions, and form submissions.
Templates in the `templates/` folder render content dynamically.

Key files:

- `app.py` – main Flask application and routes
- `resume.db` – SQLite database
- `templates/` – all HTML templates
- `requirements.txt` – dependencies list

I debated storing résumé sections in separate normalized tables for education/experience, but chose a simpler single-table design for clarity and speed.

---

### AI Acknowledgment

AI tools were used occasionally for debugging help and idea brainstorming. All code was reviewed, modified, and understood by me.
