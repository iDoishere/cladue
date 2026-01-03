skills_data = {
    "frontend": [
        {"name": "JavaScript", "level": 95, "category": "frontend"},
        {"name": "Vue.js", "level": 90, "category": "frontend"},
        {"name": "React", "level": 85, "category": "frontend"},
        {"name": "HTML", "level": 95, "category": "frontend"},
        {"name": "CSS/SASS", "level": 90, "category": "frontend"},
        {"name": "Redux", "level": 75, "category": "frontend"}
    ],
    "backend": [
        {"name": "Node.js", "level": 80, "category": "backend"},
        {"name": "Express", "level": 75, "category": "backend"},
        {"name": "REST APIs", "level": 85, "category": "backend"},
        {"name": "Socket.io", "level": 70, "category": "backend"},
        {"name": "Firebase", "level": 75, "category": "backend"}
    ],
    "tools": [
        {"name": "Git", "level": 85, "category": "tools"},
        {"name": "Vite", "level": 80, "category": "tools"},
        {"name": "TypeScript", "level": 85, "category": "tools"}
    ]
}

# Flat list of all skills for easy searching
all_skills = skills_data["frontend"] + skills_data["backend"] + skills_data["tools"]
