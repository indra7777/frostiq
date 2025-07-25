main
# Frostiq BakeryBackend

## Overview
Frostiq's BakeryBackend is a FastAPI-based backend service for managing user favorites in a bakery application. It supports adding, listing, and deleting favorite items for users, with robust validation and access control.

## Features
- Add, list, and delete user favorites
- Duplicate detection to prevent redundant entries
- Input validation for item names
- Resource-level authorization for deletion
- SQLite database (file always stored in `BakeryBackend/`)
- Ready for unit/integration testing with pytest

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd frostiq
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   uvicorn BakeryBackend.main:app --reload
   ```
   The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Running Tests
1. **Ensure pytest is installed:**
   ```bash
   pip install pytest
   ```
2. **Run the tests:**
   ```bash
   pytest BakeryBackend/routers/test_favorites.py
   ```

## Project Structure
```
frostiq/
├── BakeryBackend/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── routers/
│   │   ├── favorites.py
│   │   └── test_favorites.py
│   ├── schemas.py
│   └── favorites.db
├── requirements.txt
└── README.md
```

## API Endpoints
- `POST /favorites/` — Add a favorite
- `GET /favorites/{user_id}` — List favorites for a user
- `DELETE /favorites/{favorite_id}?user_id=...` — Delete a favorite (only by owner)

## Notes
- The database file is always created in the `BakeryBackend` directory for consistency.
- The codebase is structured for easy extension and testing.

---

Made with ❤️ 
=======
# FrostIQ

A collection of collaborative projects featuring various web applications and platforms.

## 📋 Project Structure

FrostIQ is a monorepo containing multiple independent projects:

1. **BakeryBackend** - Backend services for bakery management system
   - GitHub: [RoshanAli339/BakeryBackend](https://github.com/RoshanAli339/BakeryBackend)

2. **Bakery Frontend** - User interface for the bakery management system
   - GitHub: [ashanmukhasairam/bakery](https://github.com/ashanmukhasairam/bakery)

3. **Hackmela** - Platform for hackathon events
   - GitHub: [indra7777/Hackmela](https://github.com/indra7777/Hackmela)

4. **Torto-Forto** - Web application project
   - GitHub: [kvnrajasekhar/torto-forto](https://github.com/kvnrajasekhar/torto-forto)

## 🚀 Getting Started

### Prerequisites
- Git
- Node.js (v14 or higher) - for most subprojects
- Python (if any subproject requires it)
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository with submodules**
   ```bash
   git clone --recurse-submodules https://github.com/yourusername/frostiq.git
   cd frostiq
   ```

   If you've already cloned without submodules:
   ```bash
   git submodule update --init --recursive
   ```

2. **Set up individual projects**
   Each subproject is independent and has its own setup instructions. Navigate to each project's directory and follow their respective README files:
   
   ```bash
   # Example for BakeryBackend
   cd BakeryBackend
   # Follow README instructions in that directory
   
   # Similarly for other projects
   cd ../bakery
   # Follow README instructions
   ```

### Running the Applications

Each subproject has its own setup and running instructions. Please refer to their respective README files for the most accurate information. Here's a general overview:

#### BakeryBackend
```bash
cd BakeryBackend
# Check the project's README for specific setup instructions
# Typically involves installing dependencies and starting the server
# Example (may vary):
# npm install
# npm start
```

#### Bakery Frontend
```bash
cd bakery
# Check the project's README for specific setup instructions
# Typically involves installing dependencies and starting the development server
# Example (may vary):
# npm install
# npm run dev
```

#### Hackmela & Torto-Forto
Navigate to each directory and follow their respective README files for specific instructions.

## 🛠️ Technologies Used

Each subproject may use different technologies. Here are the main technologies used across the projects:

- **BakeryBackend**: 
  - Backend framework (Node.js/Express, Python/Flask, etc.)
  - Database (MongoDB, PostgreSQL, etc.)
  - API standards (REST/GraphQL)

- **Bakery Frontend**: 
  - Frontend framework (React, Vue, Angular, etc.)
  - State management (Redux, Context API, etc.)
  - Styling (CSS, SASS, Tailwind, etc.)

- **Hackmela & Torto-Forto**:
  - Check respective READMEs for specific technologies

**Common Tools**:
- Git for version control
- npm/yarn for package management
- Docker (if containerization is used)

## 🤝 Contributing

We welcome contributions to any of the subprojects! Here's how you can contribute:

### General Guidelines
1. Fork the main repository and clone it with submodules:
   ```bash
   git clone --recurse-submodules git@github.com:yourusername/frostiq.git
   ```

2. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes in the appropriate subproject directory

4. Commit your changes with a clear message:
   ```bash
   git commit -m "feat(subproject): brief description of changes"
   ```

5. Push your changes and create a Pull Request

### Subproject-Specific Contributions
Each subproject may have its own contribution guidelines. Please check the `CONTRIBUTING.md` or `README.md` in each subproject directory for specific instructions.

### Code Style
- Follow the coding style of each subproject
- Write clear commit messages following conventional commits
- Include relevant documentation updates with your changes
- Add tests for new features when possible

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For any questions or feedback, please open an issue in the repository.

---

*Note: This README is a template. Please update the sections with actual project-specific information.*
main
