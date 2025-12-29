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
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 32px;
  padding: 50px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(0, 0, 0, 0.04);
}

.section-title {
  font-size: 38px;
  font-weight: 900;
  background: linear-gradient(135deg, #1e293b 0%, #475569 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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
  background: linear-gradient(135deg, #fafafa 0%, #ffffff 100%);
  border: 2px solid transparent;
  background-clip: padding-box;
  border-radius: 24px;
  position: relative;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.project-card::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 24px;
  padding: 2px;
  background: linear-gradient(135deg, #e0f2fe, #ddd6fe, #fce7f3);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.4s;
}

.project-card:hover::before {
  opacity: 1;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
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
  color: #111827;
  margin: 0;
}

.project-description {
  font-size: 15px;
  line-height: 1.7;
  color: #374151;
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
  color: #6b7280;
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
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  font-size: 12px;
  font-weight: 500;
  color: #374151;
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
  color: #4b5563;
}

/* Scrollbar styling */
.projects-view::-webkit-scrollbar {
  width: 8px;
}

.projects-view::-webkit-scrollbar-track {
  background: #f8f9fa;
  border-radius: 4px;
}

.projects-view::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
}

.projects-view::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
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
