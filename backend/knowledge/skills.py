from knowledge.models import Skill

skills_data = {
    "frontend": [
        Skill(name="JavaScript", level=95, category="frontend"),
        Skill(name="Vue.js", level=90, category="frontend"),
        Skill(name="Vue 3 / Composition API", level=90, category="frontend"),
        Skill(name="React", level=85, category="frontend"),
        Skill(name="TypeScript", level=85, category="frontend"),
        Skill(name="HTML5", level=95, category="frontend"),
        Skill(name="CSS3 / SASS", level=90, category="frontend"),
        Skill(name="Nuxt.js", level=75, category="frontend"),
        Skill(name="Redux", level=75, category="frontend"),
        Skill(name="Responsive Web Design", level=90, category="frontend"),
    ],
    "backend": [
        Skill(name="Node.js", level=80, category="backend"),
        Skill(name="Express.js", level=75, category="backend"),
        Skill(name="REST APIs", level=85, category="backend"),
        Skill(name="Socket.io", level=70, category="backend"),
        Skill(name="Firebase", level=75, category="backend"),
        Skill(name="MongoDB", level=75, category="backend"),
        Skill(name="MySQL", level=70, category="backend"),
    ],
    "tools": [
        Skill(name="Git / GitHub", level=90, category="tools"),
        Skill(name="Vite", level=85, category="tools"),
        Skill(name="Webpack", level=80, category="tools"),
        Skill(name="Pinia", level=85, category="tools"),
        Skill(name="PrimeVue", level=80, category="tools"),
        Skill(name="Docker", level=70, category="tools"),
        Skill(name="Figma", level=75, category="tools"),
    ]
}

# Flat list of all skills for easy searching
all_skills = skills_data["frontend"] + skills_data["backend"] + skills_data["tools"]
