# E-Gallery

E-Gallery is a premium, professional art gallery platform built with FastAPI (Python), MongoDB, and Vue.js (using Vite). The platform allows simple users to view and purchase digital art, artists to publish and manage their portfolio, and administrators to govern the community.

## 🎨 Design System: Luxury Minimalist

Following UI/UX best practices, the visual layer has been completely refactored to use a high-end **Luxury Minimalist** design system:
- **Typography:** **Bodoni Moda** (elegant serif) for editorial headers/brand identities, paired with **Jost** (geometric sans-serif) for body text and interactive interfaces.
- **Palette (Gold & Obsidian/Stone):**
  - **Light Mode:** Canvas White (`#fafaf9`), Charcoal (`#1c1917`), and Gold Accents (`#ca8a04`).
  - **Dark Mode (Default):** Obsidian Black (`#0a0a0a`), Off-white (`#f5f5f4`), and Gold Accents (`#eab308`).
- **Aesthetic Elements:** Layered depth, frosted glassmorphism overlays, and smooth transition easing.

---

## ⚡ Key System Features

### 1. Robust Role-Based Access Control (RBAC)
- **Simple User / Collector:** Can browse the gallery, search/filter works, and buy art.
- **Artist:** Access to a personal studio dashboard containing sales metrics (revenue, masterpieces sold, active listings), publishing form, and inventory controls.
- **Admin:** Comprehensive overview of registered members and portal categories.

### 2. Live Commerce/Orders System
- A real transaction registry database is integrated. Buying an artwork makes a POST call to `/orders` and locks the item's state to `is_sold: True`, disabling future purchases.
- Artist dashboard dynamically aggregates incoming orders to show live earnings.

### 3. Dynamic Search & Advanced Filtering
- Full-text search filters artworks by title, description, or artist names on-the-fly.
- Sorting options for newest publications and price ordering (Low-to-High, High-to-Low).

---

## 🔑 Demo Login Credentials

The database is seeded with preset testing accounts. Password for all preset users is formatted below:

| Account Type | Email | Password |
|---|---|---|
| **Collector / User** | `user@egallery.com` | `user123` |
| **Artist / Creator** | `artist@egallery.com` | `artist123` |
| **Administrator** | `admin@egallery.com` | `admin123` |

---

## 🚀 Setup & Installation

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- MongoDB (running on default `mongodb://localhost:27017`) or Docker to host it.

### Database Setup (Docker or Local MongoDB)

#### Option A: Running with Docker (Recommended)
If you don't want to install MongoDB locally, you can boot it in seconds using Docker:
```bash
docker run -d --name egallery-mongo -p 27017:27017 mongo:latest
```

#### Option B: Running without Docker (Local MongoDB Installation)
If you prefer not to use Docker, you can run MongoDB as a local system service:
1. **Download & Install:**
   - **Windows:** Download the installer from the [MongoDB Community Center](https://www.mongodb.com/try/download/community). During installation, check "Install MongoDB as a Service".
   - **macOS:** Install and start MongoDB via Homebrew:
     ```bash
     brew tap mongodb/brew
     brew install mongodb-community
     brew services start mongodb-community
     ```
   - **Linux (Ubuntu):** Install using your package manager and start the systemd service:
     ```bash
     sudo systemctl start mongod
     ```
2. **Verify Port:** Make sure the database is running locally on the default port: `mongodb://localhost:27017`.

#### Option C: Running with MongoDB Atlas (Cloud Database)
If you want to use a cloud-hosted MongoDB Atlas cluster:
1. Create a free account on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) and deploy a cluster.
2. Retrieve your application connection URI.
3. Create a `.env` file in the `backend/` folder and specify the connection URL:
   ```env
   MONGO_URL=mongodb+srv://<username>:<password>@cluster0.xxxx.mongodb.net/egallery?retryWrites=true&w=majority
   ```

#### Seeding the Database
Once your MongoDB instance is running (via Docker, Local, or Cloud), populate it with the pre-configured categories, testing users, and artworks:
```bash
# From the workspace root
python backend/seed.py
```

### Starting the Backend (FastAPI)
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Boot the FastAPI Uvicorn server:
   ```bash
   uvicorn main:app --reload
   ```
   *API Swagger documentation will be available at http://localhost:8000/docs*

### Starting the Frontend (Vue 3 / Vite)
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install packages:
   ```bash
   npm install
   ```
3. Run the Vite development server:
   ```bash
   npm run dev
   ```
   *Frontend interface will be hosted at http://localhost:5173*
