# Quick start

```bash
# Clone the repository
git clone https://github.com/ErnestoAizenberg/cakeworld.git

# Enter the project directory
cd cakeworld

# Set up environment variables
cp .env.example .env

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

---

# Platform-specific setup

## 🐧 Linux / macOS

```bash
# Clone repository
git clone https://github.com/ErnestoAizenberg/cakeworld.git
cd cakeworld

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Copy environment configuration
cp .env.example .env

# Install requirements
pip install -r requirements.txt

# Run the application
python run.py
```

## 🪟 Windows (Command Prompt)

```cmd
:: Clone repository
git clone https://github.com/ErnestoAizenberg/cakeworld.git
cd cakeworld

:: Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

:: Copy environment configuration
copy .env.example .env

:: Install requirements
pip install -r requirements.txt

:: Run the application
python run.py
```

## 🪟 Windows (PowerShell)

```powershell
# Clone repository
git clone https://github.com/ErnestoAizenberg/cakeworld.git
cd cakeworld

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Copy environment configuration
Copy-Item .env.example .env

# Install requirements
pip install -r requirements.txt

# Run the application
python flask_app/run.py
```

## 🐳 Docker

```bash
# Clone repository
git clone https://github.com/ErnestoAizenberg/cakeworld.git
cd cakeworld

# Build Docker image
docker build -t cakeworld .

# Run container
docker run -p 5000:5000 --env-file .env cakeworld
```

## 📦 Docker Compose

```bash
# Clone repository
git clone https://github.com/ErnestoAizenberg/cakeworld.git
cd cakeworld

# Copy environment configuration
cp .env.example .env

# Build and run with Docker Compose
docker-compose up --build
```

---

# Detailed Setup Instructions

## 1️⃣ Clone the repository

```bash
git clone https://github.com/ErnestoAizenberg/cakeworld.git
```

## 2️⃣ Navigate to project directory

```bash
cd cakeworld
```

## 3️⃣ Environment configuration

Copy the example environment file and edit it with your settings:

```bash
cp .env.example .env
```

Edit `.env` file with your preferred text editor:
```bash
# Linux/macOS
nano .env

# Windows
notepad .env
```

Required environment variables (if any) should be documented in `.env.example`.

## 4️⃣ Install dependencies

### Using pip (standard)

```bash
pip install -r requirements.txt
```

### Using pip with virtual environment (recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Using conda (alternative)

```bash
conda create -n cakeworld python=3.9
conda activate cakeworld
pip install -r requirements.txt
```

## 5️⃣ Run the application

```bash
python run.py
```

The application should now be running at `http://localhost:5000` (or the port specified in your `.env` file).

---

# Verification

After setup, verify everything is working:

```bash
# Check Python version (3.7+ required)
python --version

# List installed packages
pip list

# Run tests (if available)
pytest tests/
```

---

# Troubleshooting

| Issue | Solution |
|-------|----------|
| `pip: command not found` | Install pip: `python -m ensurepip --upgrade` |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| Port already in use | Change `PORT` variable in `.env` file |
| Permission denied | Use `sudo` (Linux/macOS) or run as Administrator (Windows) |
| Docker build fails | Ensure Docker daemon is running |

---

# Updating

To update to the latest version:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
python run.py
```

---

# Uninstall

```bash
# Remove virtual environment
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# Delete project folder
cd ..
rm -rf cakeworld  # Linux/macOS
rmdir /s cakeworld  # Windows