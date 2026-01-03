<script setup lang="ts">
// Contact information for Ido Cohen
</script>

<template>
  <div class="contact-view">
    <div class="contact-container">
      <div class="contact-header">
        <button class="contact-button">Contact me</button>
        <p class="reach-text">You can reach me easily! Just hit me up via:</p>
      </div>

      <div class="contact-links">
        <div class="contact-item">
          <span class="contact-label">Email:</span>
          <a href="mailto:idoisher2@gmail.com" class="contact-link" target="_blank">
            idoisher2@gmail.com
          </a>
        </div>

        <div class="contact-item">
          <span class="contact-label">LinkedIn:</span>
          <a href="https://www.linkedin.com/in/ido-cohen" class="contact-link" target="_blank">
            linkedin.com/in/ido-cohen
          </a>
        </div>

        <div class="contact-item">
          <span class="contact-label">GitHub:</span>
          <a href="https://github.com/idocohen" class="contact-link" target="_blank">
            github.com/idocohen
          </a>
        </div>

        <div class="contact-item">
          <span class="contact-label">Portfolio:</span>
          <a href="https://portfoliolo.firebaseapp.com/" class="contact-link" target="_blank">
            portfoliolo.firebaseapp.com
          </a>
        </div>
      </div>

      <div class="contact-message">
        <p class="message-text">I'm always down to chat! 😊</p>
        <p class="message-details">
          As for projects that would make me say "yes" immediately, I'm all about anything where
          modern web technologies do 99% of the work and I get 100% of the credit! 😄
          Seriously, if it involves Vue.js, React, full-stack development, or building elegant
          user experiences, I'm in! What about you? What kind of projects excite you?
        </p>
      </div>

      <div class="availability-badge">
        <span class="status-dot"></span>
        <span class="status-text">Available for opportunities</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.contact-view {
  width: 100%;
  max-width: 1100px;
  height: 100%;
  overflow-y: auto;
  animation: fadeIn 0.5s ease-out;
}

.contact-container {
  background: var(--card-bg);
  border-radius: 32px;
  padding: 50px;
  box-shadow: var(--shadow-lg), 0 0 0 1px var(--border-color);
  display: flex;
  flex-direction: column;
  gap: 40px;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.contact-header {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.contact-button {
  padding: 16px 48px;
  background: var(--logo-bg);
  color: var(--logo-text);
  border: none;
  border-radius: 50px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-lg);
}

.contact-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 40px var(--shadow-color);
  opacity: 0.9;
}

.contact-button:active {
  transform: translateY(0);
}

.reach-text {
  font-size: 18px;
  color: var(--text-secondary);
  margin: 0;
  font-weight: 500;
}

.contact-links {
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 600px;
  margin: 0 auto;
  width: 100%;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: var(--bg-tertiary);
  border-radius: 16px;
  border: 2px solid var(--border-color);
  transition: all 0.3s;
}

.contact-item:hover {
  border-color: var(--accent-color);
  transform: translateX(8px);
  box-shadow: 0 8px 24px rgba(74, 158, 255, 0.15);
}

.contact-label {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  min-width: 100px;
}

.contact-link {
  font-size: 16px;
  color: var(--accent-color);
  text-decoration: none;
  transition: all 0.2s;
  font-weight: 500;
}

.contact-link:hover {
  color: var(--accent-hover);
  text-decoration: underline;
}

.contact-message {
  background: var(--bg-tertiary);
  border-left: 4px solid var(--accent-color);
  padding: 30px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  transition: background-color 0.3s ease;
}

.message-text {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.message-details {
  font-size: 16px;
  line-height: 1.7;
  color: var(--text-secondary);
  margin: 0;
}

.availability-badge {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: center;
  padding: 16px 32px;
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border-radius: 50px;
  width: fit-content;
  margin: 0 auto;
  border: 2px solid #10b981;
}

.status-dot {
  width: 12px;
  height: 12px;
  background: #10b981;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

.status-text {
  font-size: 15px;
  font-weight: 700;
  color: #065f46;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Scrollbar styling */
.contact-view::-webkit-scrollbar {
  width: 8px;
}

.contact-view::-webkit-scrollbar-track {
  background: var(--bg-tertiary);
  border-radius: 4px;
}

.contact-view::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 4px;
}

.contact-view::-webkit-scrollbar-thumb:hover {
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
  .contact-container {
    padding: 30px;
  }

  .contact-links {
    max-width: 100%;
  }

  .contact-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .contact-label {
    min-width: auto;
  }
}

@media (max-width: 768px) {
  .contact-container {
    padding: 24px;
    gap: 30px;
  }

  .contact-button {
    padding: 14px 36px;
    font-size: 16px;
  }

  .reach-text {
    font-size: 16px;
  }

  .message-text {
    font-size: 18px;
  }

  .message-details {
    font-size: 15px;
  }
}
</style>
