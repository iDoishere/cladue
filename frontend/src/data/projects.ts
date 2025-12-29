export interface Project {
  id: string
  title: string
  description: string
  technologies: string[]
  features: string[]
  image?: string
  github?: string
  demo?: string
}

export const projects: Project[] = [
  {
    id: 'android-app',
    title: 'Final Project - Android App',
    description: 'Real-time location-based app with Firebase and Google Maps integration. Features live updates from public places with unique data processing algorithms.',
    technologies: ['Android Studio', 'Java', 'Firebase', 'Google Maps API', 'GPS'],
    features: [
      'Live updates from public places in real time',
      'Google Maps integration with custom markers',
      'GPS location services and tracking',
      'Google Authentication for secure sign-in',
      'Firebase Realtime Database',
      'Unique data processing algorithms'
    ],
    image: '/projects/android-app.jpg'
  },
  {
    id: 'chat-app',
    title: 'Chat App - Full Stack',
    description: 'Real-time chat application built with modern web technologies. Features instant messaging, user authentication, and persistent message history.',
    technologies: ['React', 'Node.js', 'Express', 'Socket.io', 'Redux', 'MongoDB'],
    features: [
      'User registration and authentication',
      'Real-time messaging with Socket.io',
      'Message history and persistence',
      'User sessions and state management',
      'Responsive design for all devices',
      'Online/offline status indicators'
    ],
    image: '/projects/chat-app.jpg'
  }
]
