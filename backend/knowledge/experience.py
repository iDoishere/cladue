from knowledge.models import Experience

experience_data = [
    Experience(
        title="Front-End Developer",
        company="Trackbox.ai",
        location="Ramat Gan, Israel",
        period="2020 - Present",
        current=True,
        responsibilities=[
            "Led migration of Vue 2 codebase to Vue 3 with Composition API and <script setup>, reducing component boilerplate and improving maintainability across 20+ components",
            "Implemented Vite as primary build tool replacing Webpack, significantly improving build times and enabling near-instant hot-reload",
            "Improved page load performance through code splitting, lazy loading, and optimizing CSS architecture",
            "Designed modular architecture with composables for reusable logic, Pinia stores for state management, and a clear component hierarchy",
            "Integrated PrimeVue component library, accelerating UI development while maintaining design consistency",
            "Collaborated with a cross-functional team of 5+ developers, establishing code standards and conducting regular code reviews",
            "Leveraged AI tools (Claude Code) to accelerate development workflows, code reviews, testing, and debugging"
        ],
        technologies=["Vue.js", "Vue 3", "Composition API", "TypeScript", "JavaScript", "Vite", "Webpack", "Pinia", "PrimeVue", "SASS", "HTML5", "CSS3"]
    ),
    Experience(
        title="Shift Supervisor",
        company="Bezeq International",
        location="Petah Tikva, Israel",
        period="2014 - 2016",
        current=False,
        responsibilities=[
            "Managed customer relationships and coordinated a team under high-pressure environments",
            "Onboarded and trained new team members"
        ],
        technologies=[]
    ),
    Experience(
        title="Sales Representative",
        company="Clal Insurance",
        location="Israel",
        period="2012 - 2014",
        current=False,
        responsibilities=[
            "Built and managed client portfolio for health and personal insurance",
            "Delivered responsive service and consistent communication"
        ],
        technologies=[]
    )
]
