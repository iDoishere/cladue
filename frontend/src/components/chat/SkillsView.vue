<script setup lang="ts">
import { skillsByCategory } from '../../data/skills'
</script>

<template>
  <div class="skills-view">
    <div class="skills-container">
      <h2 class="section-title">My Skills</h2>

      <div class="skills-sections">
        <!-- Frontend Skills -->
        <div class="skill-category">
          <h3 class="category-title">
            <span class="category-icon">🎨</span>
            Frontend Development
          </h3>
          <div class="skills-list">
            <div v-for="skill in skillsByCategory.frontend" :key="skill.name" class="skill-item">
              <div class="skill-header">
                <span class="skill-name">{{ skill.name }}</span>
                <span class="skill-percentage">{{ skill.level }}%</span>
              </div>
              <div class="progress-bar">
                <div
                  class="progress-fill frontend-color"
                  :style="{ width: skill.level + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Backend Skills -->
        <div class="skill-category">
          <h3 class="category-title">
            <span class="category-icon">⚙️</span>
            Backend Development
          </h3>
          <div class="skills-list">
            <div v-for="skill in skillsByCategory.backend" :key="skill.name" class="skill-item">
              <div class="skill-header">
                <span class="skill-name">{{ skill.name }}</span>
                <span class="skill-percentage">{{ skill.level }}%</span>
              </div>
              <div class="progress-bar">
                <div
                  class="progress-fill backend-color"
                  :style="{ width: skill.level + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tools & Others -->
        <div class="skill-category">
          <h3 class="category-title">
            <span class="category-icon">🛠️</span>
            Tools & Technologies
          </h3>
          <div class="skills-list">
            <div v-for="skill in skillsByCategory.tools" :key="skill.name" class="skill-item">
              <div class="skill-header">
                <span class="skill-name">{{ skill.name }}</span>
                <span class="skill-percentage">{{ skill.level }}%</span>
              </div>
              <div class="progress-bar">
                <div
                  class="progress-fill tools-color"
                  :style="{ width: skill.level + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.skills-view {
  width: 100%;
  max-width: 1100px;
  height: 100%;
  overflow-y: auto;
  animation: fadeIn 0.5s ease-out;
}

.skills-container {
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

.skills-sections {
  display: flex;
  flex-direction: column;
  gap: 35px;
}

.skill-category {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.category-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.category-icon {
  font-size: 24px;
}

.skills-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.skill-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skill-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.skill-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-secondary);
}

.skill-percentage {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-tertiary);
}

.progress-bar {
  width: 100%;
  height: 12px;
  background: var(--bg-tertiary);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: inset 0 2px 6px var(--shadow-color);
  position: relative;
  transition: background-color 0.3s ease;
}

.progress-fill {
  height: 100%;
  border-radius: 12px;
  transition: width 1.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.3) 50%,
    transparent 100%
  );
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

.frontend-color {
  background: linear-gradient(90deg, #3b82f6 0%, #2563eb 50%, #1d4ed8 100%);
}

.backend-color {
  background: linear-gradient(90deg, #10b981 0%, #059669 50%, #047857 100%);
}

.tools-color {
  background: linear-gradient(90deg, #a855f7 0%, #9333ea 50%, #7e22ce 100%);
}

/* Scrollbar styling */
.skills-view::-webkit-scrollbar {
  width: 8px;
}

.skills-view::-webkit-scrollbar-track {
  background: var(--bg-tertiary);
  border-radius: 4px;
}

.skills-view::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

.skills-view::-webkit-scrollbar-thumb:hover {
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
  .skills-container {
    padding: 30px;
  }

  .section-title {
    font-size: 28px;
  }
}

@media (max-width: 768px) {
  .skills-container {
    padding: 24px;
  }

  .section-title {
    font-size: 24px;
  }

  .category-title {
    font-size: 18px;
  }

  .skill-name {
    font-size: 14px;
  }
}
</style>
