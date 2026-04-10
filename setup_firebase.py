import os, glob, re

# Firebase replacement strings
firebase_scripts = """    <!-- Firebase -->
    <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore-compat.js"></script>
    <script src="js/app.js"></script>"""

# Update HTML files
html_files = glob.glob("*.html")
for f in html_files:
    with open(f, "r") as file:
        content = file.read()
    
    # Replace the existing app.js script tag if Firebase is not already added
    if "firebase-app-compat.js" not in content:
        content = re.sub(r'[ \t]*<script src="js/app\.js"></script>', firebase_scripts, content)
        with open(f, "w") as file:
            file.write(content)
        print(f"Updated {f}")

# Update JS files to listen to custom 'db-ready' event instead of DOMContentLoaded
# This ensures that pages wait for Firebase to load before rendering
js_files = glob.glob("js/*.js")
for f in js_files:
    if "app.js" in f or "navbar.js" in f or "chatbot.js" in f:
        continue
    with open(f, "r") as file:
        content = file.read()
    
    if "db-ready" not in content:
        content = content.replace("document.addEventListener('DOMContentLoaded', () => {", "window.addEventListener('db-ready', () => {")
        with open(f, "w") as file:
            file.write(content)
        print(f"Updated {f}")

print("Batch update complete.")
