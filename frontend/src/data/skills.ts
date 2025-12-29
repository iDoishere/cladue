export interface Skill {
  name: string
  level: number // 0-100
  category: 'frontend' | 'backend' | 'tools'
}

export const skills: Skill[] = [
  // Frontend
  { name: 'JavaScript', level: 95, category: 'frontend' },
  { name: 'Vue.js', level: 90, category: 'frontend' },
  { name: 'React', level: 85, category: 'frontend' },
  { name: 'HTML', level: 95, category: 'frontend' },
  { name: 'CSS/SASS', level: 90, category: 'frontend' },
  { name: 'Redux', level: 75, category: 'frontend' },

  // Backend
  { name: 'Node.js', level: 80, category: 'backend' },
  { name: 'Express', level: 75, category: 'backend' },
  { name: 'REST APIs', level: 85, category: 'backend' },
  { name: 'Socket.io', level: 70, category: 'backend' },
  { name: 'Firebase', level: 75, category: 'backend' },

  // Tools
  { name: 'Git', level: 85, category: 'tools' },
  { name: 'Vite', level: 80, category: 'tools' },
  { name: 'TypeScript', level: 85, category: 'tools' }
]

export const skillsByCategory = {
  frontend: skills.filter(s => s.category === 'frontend'),
  backend: skills.filter(s => s.category === 'backend'),
  tools: skills.filter(s => s.category === 'tools')
}
