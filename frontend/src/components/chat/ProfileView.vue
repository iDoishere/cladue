<script setup lang="ts">
const tags = [
  'Full-Stack Developer',
  'Vue.js',
  'React',
  'Node.js',
  'Rosh Ashlain'
]
</script>

<template>
  <div class="profile-view">
    <div class="profile-card">
      <div class="profile-header">
        <div class="profile-photo">
          <div class="photo-placeholder">
            <span class="emoji">🧑‍💻</span>
          </div>
        </div>

        <div class="profile-content">
          <h2 class="profile-name">Ido Cohen</h2>
          <p class="profile-meta">Full-Stack Developer • Rosh Ashlain, Israel</p>

          <div class="profile-greeting">
            <p class="greeting-text">Hey 👋</p>
            <p class="intro-text">
              I'm Ido, a Full-Stack Developer based in Rosh Ashlain, Israel. I'm currently working as a Front-End Developer at 42 Paris. I'm passionate about Vue.js, React, and building elegant user experiences with modern web technologies.
            </p>
          </div>

          <div class="tags">
            <span v-for="tag in tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>
      </div>

      <div class="bio-section">
        <p class="bio-text">
          I'm Ido Cohen, a passionate Full-Stack Developer specializing in modern JavaScript frameworks, currently rocking it at Tigloo since 2020. 🚀 Before diving into tech, I had diverse experiences in customer management and sales, which helps me understand user needs better.
        </p>
        <p class="bio-text">
          I'm super passionate about creating web applications that are both powerful and user-friendly, with a special focus on Vue.js and React. I love transforming complex technical concepts into simple, elegant interfaces. Voilà! What about you? What brings you here? 😊
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-view {
  width: 100%;
  max-width: 1100px;
  height: 100%;
  overflow-y: auto;
  animation: fadeIn 0.5s ease-out;
}

.profile-card {
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 32px;
  padding: 50px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(10px);
}

.profile-header {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 50px;
  margin-bottom: 50px;
}

.profile-photo {
  width: 100%;
}

.photo-placeholder {
  width: 100%;
  aspect-ratio: 1;
  background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.emoji {
  font-size: 120px;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.profile-name {
  font-size: 36px;
  font-weight: 800;
  color: #111827;
  margin: 0;
  line-height: 1.2;
}

.profile-meta {
  font-size: 16px;
  color: #6b7280;
  margin: 0;
}

.profile-greeting {
  margin-top: 10px;
}

.greeting-text {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin: 0 0 12px 0;
}

.intro-text {
  font-size: 15px;
  line-height: 1.7;
  color: #374151;
  margin: 0;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.tag {
  padding: 10px 20px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 1.5px solid rgba(14, 165, 233, 0.2);
  border-radius: 24px;
  font-size: 13px;
  font-weight: 600;
  color: #0c4a6e;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.tag::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
  transition: left 0.5s;
}

.tag:hover {
  background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
  color: white;
  border-color: #0ea5e9;
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(14, 165, 233, 0.3);
}

.tag:hover::before {
  left: 100%;
}

.bio-section {
  padding-top: 30px;
  border-top: 1px solid #f3f4f6;
}

.bio-text {
  font-size: 15px;
  line-height: 1.8;
  color: #374151;
  margin: 0 0 20px 0;
}

.bio-text:last-child {
  margin-bottom: 0;
}

/* Scrollbar styling */
.profile-view::-webkit-scrollbar {
  width: 8px;
}

.profile-view::-webkit-scrollbar-track {
  background: #f8f9fa;
  border-radius: 4px;
}

.profile-view::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 4px;
}

.profile-view::-webkit-scrollbar-thumb:hover {
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
  .profile-card {
    padding: 30px;
  }

  .profile-header {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .photo-placeholder {
    max-width: 280px;
    margin: 0 auto;
  }

  .emoji {
    font-size: 100px;
  }

  .profile-name {
    font-size: 28px;
  }
}

@media (max-width: 768px) {
  .profile-card {
    padding: 24px;
  }

  .profile-name {
    font-size: 24px;
  }
}
</style>
