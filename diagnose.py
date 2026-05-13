import re

with open("index.html", "r") as f:
    content = f.read()

# Check for stray </button>
strays = re.findall(r"</li>\s*<svg.*?/button>\s*</ul>", content, re.DOTALL)
if strays:
    print(f"Found {len(strays)} stray buttons in nav-desktop")

# Check if translations is correctly closed
match = re.search(r"const translations = \{.*?\}\s*;\s*let currentLang", content, re.DOTALL)
if match:
    print("Translations object seems correctly structured")
else:
    print("Translations object might be broken")
    # Let's see the end of it
    end_match = re.findall(r"\"footer_rights\": \".*?\"\s*\}\s*\}?\s*;", content, re.DOTALL)
    print(f"Ends found: {end_match}")

# Check for script errors by running node again with better mock
