# 🔁 Initial Setup
chmod +x setup.sh && ./setup.sh

# 📦 Scan folders
./autopilot_dev.sh --scan

# 🧠 Complete a found repo
./autopilot_dev.sh --complete "/Users/you/Projects/dead_repo"

# 📄 Open UI at http://localhost:3000
cd frontend && python3 -m http.server 3000
