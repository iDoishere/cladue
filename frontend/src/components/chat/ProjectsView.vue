<script setup lang="ts">
import { projects } from '../../data/projects'
</script>

<template>
  <div class="projects-view">
    <div class="projects-container">
      <h2 class="section-title">My Projects</h2>

      <div class="projects-grid">
        <div v-for="project in projects" :key="project.id" class="project-card">
          <div class="project-image">
            <div class="image-placeholder">
              <span class="project-emoji">{{ project.id === 'android-app' ? '📱' : '💬' }}</span>
            </div>
          </div>

          <div class="project-content">
            <h3 class="project-title">{{ project.title }}</h3>
            <p class="project-description">{{ project.description }}</p>

            <div class="technologies">
              <h4 class="tech-heading">Technologies</h4>
              <div class="tech-tags">
                <span v-for="tech in project.technologies" :key="tech" class="tech-tag">
                  {{ tech }}
                </span>
              </div>
            </div>

            <div class="features">
              <h4 class="features-heading">Key Features</h4>
              <ul class="features-list">
                <li v-for="feature in project.features" :key="feature">{{ feature }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.projects-view {
  width: 100%;
  max-width: 1100px;
  height: 100%;
  overflow-y: auto;
  animation: fadeIn 0.5s ease-out;
}

.projects-container {
  background: var(--card-bg);
  border-radius: 32px;
  padding: 50px;
  box-shadow: var(--shadow-lg), 0 0 0 1px var(--border-color);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.section-title {
  font-size: 38px;
  font-weight: 900;
  color: var(--text-primary);
  margin: 0 0 40px 0;
  text-align: center;
  letter-spacing: -0.02em;
}

.projects-grid {
  display: flex;
  flex-direction: column;
  gap: 35px;
}

.project-card {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 40px;
  padding: 32px;
  background: var(--bg-tertiary);
  border: 2px solid var(--border-color);
  border-radius: 24px;
  position: relative;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--accent-color);
}

.project-image {
  width: 100%;
}

.image-placeholder {
  width: 100%;
  aspect-ratio: 16/9;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-sm);
}

.project-emoji {
  font-size: 64px;
}

.project-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.project-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.project-description {
  font-size: 15px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 0;
}

.technologies,
.features {
  margin-top: 8px;
}

.tech-heading,
.features-heading {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-tertiary);
  margin: 0 0 10px 0;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tech-tag {
  padding: 6px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: background-color 0.3s ease, color 0.3s ease;
}

.features-list {
  margin: 0;
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.features-list li {
  font-size: 14px;
  line-height: 1.6;
  color: var(--text-secondary);
}

/* Scrollbar styling */
.projects-view::-webkit-scrollbar {
  width: 8px;
}

.projects-view::-webkit-scrollbar-track {
  background: var(--bg-tertiary);
  border-radius: 4px;
}

.projects-view::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

.projects-view::-webkit-scrollbar-thumb:hover {
  background: var(--text-tertiary);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 968px) {
  .projects-container {
    padding: 30px;
  }

  .project-card {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .image-placeholder {
    max-width: 400px;
    margin: 0 auto;
  }

  .section-title {
    font-size: 28px;
  }
}

@media (max-width: 768px) {
  .projects-container {
    padding: 24px;
  }

  .section-title {
    font-size: 24px;
  }

  .project-card {
    padding: 20px;
  }

  .project-emoji {
    font-size: 48px;
  }
}
</style>
