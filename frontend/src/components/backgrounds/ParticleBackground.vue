<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useTheme } from '../../composables/useTheme'

const { isDark } = useTheme()

const canvasRef = ref<HTMLCanvasElement>()
let animationId: number
let mouseX = 0
let mouseY = 0
let time = 0

interface Particle {
  x: number
  y: number
  vx: number
  vy: number
  size: number
  color: { r: number; g: number; b: number }
  alpha: number
  pulse: number
  pulseSpeed: number
}

interface Orb {
  x: number
  y: number
  baseX: number
  baseY: number
  size: number
  color: { r: number; g: number; b: number }
  pulse: number
  pulseSpeed: number
  orbitSpeed: number
  orbitRadius: number
  phase: number
}

interface Trail {
  x: number
  y: number
  alpha: number
  size: number
  color: { r: number; g: number; b: number }
}

interface ShootingStar {
  x: number
  y: number
  angle: number
  speed: number
  length: number
  alpha: number
  color: { r: number; g: number; b: number }
}

// Dark theme colors
const darkColors = [
  { r: 74, g: 158, b: 255 },   // Blue
  { r: 139, g: 92, b: 246 },   // Purple
  { r: 236, g: 72, b: 153 },   // Pink
  { r: 16, g: 185, b: 129 },   // Green
  { r: 6, g: 182, b: 212 },    // Cyan
  { r: 251, g: 146, b: 60 },   // Orange
]

// Light theme colors (deeper/more saturated for visibility on light bg)
const lightColors = [
  { r: 59, g: 130, b: 246 },   // Blue
  { r: 124, g: 58, b: 237 },   // Purple
  { r: 219, g: 39, b: 119 },   // Pink
  { r: 5, g: 150, b: 105 },    // Green
  { r: 14, g: 165, b: 197 },   // Cyan
  { r: 234, g: 88, b: 12 },    // Orange
]

const getColors = () => isDark.value ? darkColors : lightColors
const getBgColor = () => isDark.value ? 'rgba(10, 10, 26, 0.12)' : 'rgba(255, 255, 255, 0.08)'

let particles: Particle[] = []
let orbs: Orb[] = []
let trails: Trail[] = []
let shootingStars: ShootingStar[] = []
let width = 0
let height = 0

function init() {
  const canvas = canvasRef.value
  if (!canvas) return

  width = canvas.width = window.innerWidth
  height = canvas.height = window.innerHeight

  const colors = getColors()

  // Create MORE particles
  particles = Array.from({ length: 200 }, () => {
    const color = colors[Math.floor(Math.random() * colors.length)]
    return {
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 1.2,
      vy: (Math.random() - 0.5) * 1.2,
      size: Math.random() * 3 + 1,
      color,
      alpha: Math.random() * 0.6 + 0.2,
      pulse: Math.random() * Math.PI * 2,
      pulseSpeed: Math.random() * 0.08 + 0.02
    }
  })

  // Create DRAMATIC floating orbs
  orbs = Array.from({ length: 6 }, (_, i) => {
    const color = colors[i % colors.length]
    return {
      x: Math.random() * width,
      y: Math.random() * height,
      baseX: Math.random() * width,
      baseY: Math.random() * height,
      size: Math.random() * 120 + 80,
      color,
      pulse: Math.random() * Math.PI * 2,
      pulseSpeed: Math.random() * 0.02 + 0.01,
      orbitSpeed: Math.random() * 0.0005 + 0.0002,
      orbitRadius: Math.random() * 100 + 50,
      phase: Math.random() * Math.PI * 2
    }
  })
}

// Re-init when theme changes
watch(isDark, () => {
  init()
})

function animate() {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  time += 16

  // Semi-transparent clear for motion blur effect
  ctx.fillStyle = getBgColor()
  ctx.fillRect(0, 0, width, height)

  // Update and draw orbs with MEGA GLOW
  orbs.forEach(orb => {
    orb.pulse += orb.pulseSpeed
    const t = time * orb.orbitSpeed
    orb.x = orb.baseX + Math.sin(t + orb.phase) * orb.orbitRadius
    orb.y = orb.baseY + Math.cos(t * 0.7 + orb.phase) * orb.orbitRadius * 0.6

    // Slowly drift base position
    orb.baseX += Math.sin(time * 0.0001 + orb.phase) * 0.1
    orb.baseY += Math.cos(time * 0.00015 + orb.phase) * 0.1

    // Wrap around
    if (orb.baseX < -200) orb.baseX = width + 200
    if (orb.baseX > width + 200) orb.baseX = -200
    if (orb.baseY < -200) orb.baseY = height + 200
    if (orb.baseY > height + 200) orb.baseY = -200

    const pulseSize = orb.size + Math.sin(orb.pulse) * 20
    const { r, g, b } = orb.color

    // Multiple glow layers for DRAMATIC effect
    for (let i = 4; i >= 0; i--) {
      const layerSize = pulseSize * (1 + i * 0.5)
      const gradient = ctx.createRadialGradient(orb.x, orb.y, 0, orb.x, orb.y, layerSize)
      const alphaBase = 0.25 - i * 0.04
      gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${alphaBase})`)
      gradient.addColorStop(0.3, `rgba(${r}, ${g}, ${b}, ${alphaBase * 0.5})`)
      gradient.addColorStop(0.6, `rgba(${r}, ${g}, ${b}, ${alphaBase * 0.2})`)
      gradient.addColorStop(1, 'rgba(0, 0, 0, 0)')

      ctx.beginPath()
      ctx.arc(orb.x, orb.y, layerSize, 0, Math.PI * 2)
      ctx.fillStyle = gradient
      ctx.fill()
    }

    // Bright core
    const coreGradient = ctx.createRadialGradient(orb.x, orb.y, 0, orb.x, orb.y, pulseSize * 0.3)
    coreGradient.addColorStop(0, `rgba(255, 255, 255, 0.3)`)
    coreGradient.addColorStop(0.5, `rgba(${r}, ${g}, ${b}, 0.2)`)
    coreGradient.addColorStop(1, 'rgba(0, 0, 0, 0)')
    ctx.beginPath()
    ctx.arc(orb.x, orb.y, pulseSize * 0.3, 0, Math.PI * 2)
    ctx.fillStyle = coreGradient
    ctx.fill()
  })

  // Mouse trails
  if (mouseX > 0 && mouseY > 0) {
    const colors = getColors()
    for (let i = 0; i < 3; i++) {
      const color = colors[Math.floor(Math.random() * colors.length)]
      trails.push({
        x: mouseX + (Math.random() - 0.5) * 30,
        y: mouseY + (Math.random() - 0.5) * 30,
        alpha: 0.8,
        size: Math.random() * 10 + 5,
        color
      })
    }
  }

  // Draw and fade trails
  for (let i = trails.length - 1; i >= 0; i--) {
    const trail = trails[i]
    trail.alpha -= 0.03
    trail.size *= 0.97

    if (trail.alpha <= 0) {
      trails.splice(i, 1)
      continue
    }

    const { r, g, b } = trail.color
    const gradient = ctx.createRadialGradient(trail.x, trail.y, 0, trail.x, trail.y, trail.size * 4)
    gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${trail.alpha})`)
    gradient.addColorStop(0.3, `rgba(${r}, ${g}, ${b}, ${trail.alpha * 0.4})`)
    gradient.addColorStop(1, 'rgba(0, 0, 0, 0)')

    ctx.beginPath()
    ctx.arc(trail.x, trail.y, trail.size * 4, 0, Math.PI * 2)
    ctx.fillStyle = gradient
    ctx.fill()
  }

  // Shooting stars
  if (Math.random() < 0.015) {
    const colors = getColors()
    const color = colors[Math.floor(Math.random() * colors.length)]
    shootingStars.push({
      x: Math.random() * width,
      y: Math.random() * height * 0.4,
      angle: Math.PI / 4 + (Math.random() - 0.5) * 0.3,
      speed: 15 + Math.random() * 10,
      length: 80 + Math.random() * 120,
      alpha: 1,
      color
    })
  }

  // Draw shooting stars
  for (let i = shootingStars.length - 1; i >= 0; i--) {
    const star = shootingStars[i]
    star.x += Math.cos(star.angle) * star.speed
    star.y += Math.sin(star.angle) * star.speed
    star.alpha -= 0.02

    if (star.alpha <= 0 || star.x > width + 100 || star.y > height + 100) {
      shootingStars.splice(i, 1)
      continue
    }

    const { r, g, b } = star.color
    const endX = star.x - Math.cos(star.angle) * star.length
    const endY = star.y - Math.sin(star.angle) * star.length

    const gradient = ctx.createLinearGradient(endX, endY, star.x, star.y)
    gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, 0)`)
    gradient.addColorStop(0.7, `rgba(${r}, ${g}, ${b}, ${star.alpha * 0.5})`)
    gradient.addColorStop(1, `rgba(255, 255, 255, ${star.alpha})`)

    ctx.beginPath()
    ctx.moveTo(endX, endY)
    ctx.lineTo(star.x, star.y)
    ctx.strokeStyle = gradient
    ctx.lineWidth = 3
    ctx.lineCap = 'round'
    ctx.stroke()

    // Star head glow
    const headGlow = ctx.createRadialGradient(star.x, star.y, 0, star.x, star.y, 15)
    headGlow.addColorStop(0, `rgba(255, 255, 255, ${star.alpha})`)
    headGlow.addColorStop(0.5, `rgba(${r}, ${g}, ${b}, ${star.alpha * 0.5})`)
    headGlow.addColorStop(1, 'rgba(0, 0, 0, 0)')
    ctx.beginPath()
    ctx.arc(star.x, star.y, 15, 0, Math.PI * 2)
    ctx.fillStyle = headGlow
    ctx.fill()
  }

  // Update and draw particles
  particles.forEach(particle => {
    // Mouse repulsion
    const dx = particle.x - mouseX
    const dy = particle.y - mouseY
    const dist = Math.sqrt(dx * dx + dy * dy)

    if (dist < 180 && dist > 0) {
      const force = (180 - dist) / 180
      particle.vx += (dx / dist) * force * 0.8
      particle.vy += (dy / dist) * force * 0.8
    }

    particle.x += particle.vx
    particle.y += particle.vy
    particle.vx *= 0.98
    particle.vy *= 0.98
    particle.pulse += particle.pulseSpeed

    // Wrap
    if (particle.x < 0) particle.x = width
    if (particle.x > width) particle.x = 0
    if (particle.y < 0) particle.y = height
    if (particle.y > height) particle.y = 0

    const pulseAlpha = particle.alpha + Math.sin(particle.pulse) * 0.15
    const pulseSize = particle.size + Math.sin(particle.pulse * 2) * 0.8
    const { r, g, b } = particle.color

    // Glow
    const gradient = ctx.createRadialGradient(
      particle.x, particle.y, 0,
      particle.x, particle.y, pulseSize * 5
    )
    gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${pulseAlpha})`)
    gradient.addColorStop(0.2, `rgba(${r}, ${g}, ${b}, ${pulseAlpha * 0.4})`)
    gradient.addColorStop(1, 'rgba(0, 0, 0, 0)')

    ctx.beginPath()
    ctx.arc(particle.x, particle.y, pulseSize * 5, 0, Math.PI * 2)
    ctx.fillStyle = gradient
    ctx.fill()

    // Core
    ctx.beginPath()
    ctx.arc(particle.x, particle.y, pulseSize, 0, Math.PI * 2)
    ctx.fillStyle = `rgba(255, 255, 255, ${pulseAlpha + 0.2})`
    ctx.fill()
  })

  // Connections
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const p1 = particles[i]
      const p2 = particles[j]
      const dx = p1.x - p2.x
      const dy = p1.y - p2.y
      const dist = Math.sqrt(dx * dx + dy * dy)

      if (dist < 100) {
        const alpha = (1 - dist / 100) * 0.3
        const gradient = ctx.createLinearGradient(p1.x, p1.y, p2.x, p2.y)
        gradient.addColorStop(0, `rgba(${p1.color.r}, ${p1.color.g}, ${p1.color.b}, ${alpha})`)
        gradient.addColorStop(1, `rgba(${p2.color.r}, ${p2.color.g}, ${p2.color.b}, ${alpha})`)

        ctx.beginPath()
        ctx.moveTo(p1.x, p1.y)
        ctx.lineTo(p2.x, p2.y)
        ctx.strokeStyle = gradient
        ctx.lineWidth = 1
        ctx.stroke()
      }
    }
  }

  animationId = requestAnimationFrame(animate)
}

function handleResize() {
  init()
}

function handleMouseMove(e: MouseEvent) {
  mouseX = e.clientX
  mouseY = e.clientY
}

function handleMouseLeave() {
  mouseX = -1000
  mouseY = -1000
}

onMounted(() => {
  init()
  animate()
  window.addEventListener('resize', handleResize)
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('mouseleave', handleMouseLeave)
})

onUnmounted(() => {
  cancelAnimationFrame(animationId)
  window.removeEventListener('resize', handleResize)
  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseleave', handleMouseLeave)
})
</script>

<template>
  <div class="particle-container">
    <canvas ref="canvasRef" class="particle-canvas"></canvas>
    <div class="vignette"></div>
  </div>
</template>

<style scoped>
.particle-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -1;
  background: linear-gradient(135deg, #050510 0%, #0a0a1a 30%, #0d1025 60%, #05080f 100%);
  overflow: hidden;
  transition: background 0.5s ease;
}

/* Light theme background */
:global([data-theme="light"]) .particle-container {
  background: linear-gradient(135deg, #e8f4fc 0%, #dbe9f4 30%, #d4e5f7 60%, #c8dff5 100%);
}

.particle-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.vignette {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(ellipse at center, transparent 0%, rgba(0, 0, 0, 0.4) 100%);
  pointer-events: none;
  transition: background 0.5s ease;
}

:global([data-theme="light"]) .vignette {
  background: radial-gradient(ellipse at center, transparent 0%, rgba(100, 120, 150, 0.15) 100%);
}
</style>
