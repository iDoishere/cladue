# Vue 3 + Three.js Portfolio - Implementation Plan

## Overview
Building a visually stunning portfolio website for Ido Cohen using Vue 3, Vite 6, and Three.js with "crazy" 3D animations and interactive elements.

## Technology Stack

### Core
- **Vue 3.5+** with Composition API + TypeScript
- **Vite 6** for fast builds and HMR
- **TresJS v5** - Modern Vue wrapper for Three.js (recommended over TroisJS which is stagnant)
- **GSAP 3 + ScrollTrigger** for scroll-driven animations

### Supporting Libraries
- **@tresjs/cientos** - Helper components (camera controls, environment)
- **@tresjs/post-processing** - Shader effects (bloom, chromatic aberration)
- **three-custom-shader-material** - Custom shader integration
- **glsl-noise** - Procedural noise for shaders

## Project Structure

```
/home/idocohen/Projects/idoClaude/
├── public/
│   ├── models/              # 3D models (.glb)
│   └── textures/            # Texture maps
├── src/
│   ├── assets/
│   │   ├── shaders/         # GLSL shader files
│   │   │   ├── particles/
│   │   │   │   ├── vertex.glsl
│   │   │   │   └── fragment.glsl
│   │   │   └── dissolve/
│   │   └── images/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── AppHeader.vue
│   │   │   └── ScrollProgress.vue
│   │   ├── sections/
│   │   │   ├── HeroSection.vue
│   │   │   ├── AboutSection.vue
│   │   │   ├── ExperienceSection.vue
│   │   │   └── ProjectsSection.vue
│   │   └── three/           # 3D components
│   │       ├── scenes/
│   │       │   ├── HeroScene.vue
│   │       │   ├── ParticleField.vue
│   │       │   ├── FloatingObjects.vue
│   │       │   └── ProjectShowcase.vue
│   │       └── effects/
│   ├── composables/         # Reusable composition functions
│   │   ├── useScrollAnimation.ts    # GSAP + Three.js integration
│   │   ├── useThreeScene.ts
│   │   ├── useParticleSystem.ts
│   │   └── useResponsive3D.ts       # Dynamic quality scaling
│   ├── utils/
│   │   ├── three/
│   │   │   ├── materials.ts
│   │   │   ├── geometries.ts
│   │   │   └── loaders.ts
│   │   └── performance.ts
│   ├── data/
│   │   ├── experience.ts    # Work history
│   │   ├── projects.ts      # Project showcase data
│   │   └── skills.ts
│   ├── App.vue
│   ├── main.ts
│   └── style.css
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## Section Designs

### 1. Hero/Landing
**Concept:** Floating geometric shapes with GPU particle system

**3D Elements:**
- Large wireframe sphere with animated vertex displacement (Perlin noise)
- 8,000-10,000 GPU particles forming name, then exploding into constellation
- 5-7 floating geometric objects (icosahedrons, toruses) with mouse parallax
- Fresnel glow shader effects
- Bloom + chromatic aberration post-processing

**Animation:** Particles morph name → constellation on load, camera zooms through on scroll

### 2. About/Summary
**Concept:** Double helix of 3D skill tags

**3D Elements:**
- Skills arranged in DNA helix structure
- 3D text with emissive glow
- Interactive hover to show proficiency levels
- Gradient ramp shader on helix

**Animation:** Helix assembles on scroll-in, rotates during scroll, dissolves to particles on exit

### 3. Work Experience Timeline
**Concept:** 3D curved path with milestone nodes

**3D Elements:**
- Curved tube geometry (timeline road)
- Glowing sphere nodes at each job (Tigloo, Bezek, Clal Insurance)
- Animated flow gradient along tube
- Particle trail following path
- DOM overlay cards at each node

**Animation:** Camera follows path on scroll, active node pulses

### 4. Projects Showcase
**Concept:** 3D carousel of project cards

**3D Elements:**
- Circular arrangement of project cards with screenshot textures
- Hover displacement shader on cards
- Click to expand: 3D mockup (phone for Android app, laptop for web apps)
- Particle burst on selection

**Animation:** Carousel auto-rotates, drag to spin, zoom on project click

## Critical Implementation Files

### 1. `/home/idocohen/Projects/idoClaude/src/composables/useScrollAnimation.ts`
Core scroll animation logic connecting GSAP ScrollTrigger with Three.js cameras and shader uniforms.

```typescript
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { ScrollSmoother } from 'gsap/ScrollSmoother'

export function useScrollAnimation() {
  const initSmoother = () => {
    return ScrollSmoother.create({
      smooth: 2,
      effects: true,
      smoothTouch: 0.1,
    })
  }

  const createSceneAnimation = (trigger, camera, targetPosition) => {
    return gsap.timeline({
      scrollTrigger: {
        trigger,
        start: 'top top',
        end: 'bottom top',
        scrub: 1,
        pin: true,
      }
    }).to(camera.position, { ...targetPosition })
  }

  return { initSmoother, createSceneAnimation }
}
```

### 2. `/home/idocohen/Projects/idoClaude/src/components/three/scenes/HeroScene.vue`
First impression component with GPU particles and floating objects.

```vue
<template>
  <TresCanvas v-bind="canvasConfig">
    <TresPerspectiveCamera :position="[0, 0, 10]" />

    <!-- Wireframe sphere with displacement -->
    <TresMesh ref="heroSphere">
      <TresIcosahedronGeometry :args="[2, 4]" />
      <TresShaderMaterial
        :vertex-shader="vertexShader"
        :fragment-shader="fragmentShader"
        wireframe
      />
    </TresMesh>

    <!-- GPU Particles -->
    <ParticleField :count="8000" />

    <!-- Floating objects -->
    <FloatingObjects :mouse-position="mousePosition" />

    <!-- Post-processing -->
    <EffectComposer>
      <Bloom :intensity="1.2" />
    </EffectComposer>
  </TresCanvas>
</template>
```

### 3. `/home/idocohen/Projects/idoClaude/src/assets/shaders/particles/vertex.glsl` + `fragment.glsl`
GPU particle system shaders used across multiple sections.

### 4. `/home/idocohen/Projects/idoClaude/vite.config.ts`
Build configuration with code splitting and shader handling.

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import glsl from 'vite-plugin-glsl'

export default defineConfig({
  plugins: [vue(), glsl()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor-vue': ['vue'],
          'vendor-three': ['three', '@tresjs/core'],
          'vendor-gsap': ['gsap'],
        },
      },
    },
    target: 'esnext',
  },
})
```

### 5. `/home/idocohen/Projects/idoClaude/src/composables/useResponsive3D.ts`
Dynamic quality scaling for mobile vs desktop.

```typescript
export function useResponsive3D() {
  const { width } = useWindowSize()

  return computed(() => {
    const isMobile = width.value < 768

    return {
      particleCount: isMobile ? 2000 : 10000,
      antialias: !isMobile,
      postProcessing: !isMobile,
      floatingObjectCount: isMobile ? 3 : 7,
    }
  })
}
```

## Performance Optimization

### Code Splitting
- Separate chunks for Vue, Three.js, GSAP
- Lazy load 3D scenes using `defineAsyncComponent`
- Load scenes only when scrolled into view (Intersection Observer)

### GPU Optimization
- Use GPU particle system (GPGPU computation renderer)
- Instanced meshes for repeated objects
- BufferGeometry exclusively
- Texture atlases where possible

### Responsive Scaling
- Dynamic particle count (2k mobile, 10k desktop)
- Disable post-processing on mobile
- Max pixel ratio 1.5 on mobile
- Reduce floating object count

### Asset Optimization
- Draco compression for 3D models
- WebP textures (max 2048x2048)
- Merge static geometries
- Progressive texture loading

## Implementation Phases

### Phase 1: Foundation Setup
1. Initialize Vite + Vue 3 + TypeScript project
2. Install TresJS, Three.js, GSAP
3. Configure Vite with GLSL plugin
4. Create base section components
5. Test TresJS with simple rotating cube

**Deliverable:** Working dev environment with test 3D scene

### Phase 2: Hero Section
1. GPU particle system with morph states
2. Wireframe sphere with vertex displacement shader
3. Floating geometric objects with mouse parallax
4. GSAP ScrollTrigger integration
5. Bloom post-processing

**Deliverable:** Complete hero section with all animations

### Phase 3: About Section
1. Skill data structure
2. Double helix curve with skill boxes
3. Interactive hover with raycaster
4. Dissolve transition shader
5. Scroll-driven helix rotation

**Deliverable:** Interactive skill visualization

### Phase 4: Experience Timeline
1. Curved tube geometry timeline
2. Experience nodes with data
3. HTML overlay cards
4. Camera path-following animation
5. Particle trail

**Deliverable:** 3D timeline with smooth camera movement

### Phase 5: Projects Showcase
1. Circular carousel arrangement
2. Screenshot textures on cards
3. Hover displacement shader
4. Expand animation with 3D mockup
5. Rotation controls (drag, keyboard)

**Deliverable:** Interactive project gallery

### Phase 6: Transitions & Polish
1. Cross-section camera transitions
2. ScrollSmoother configuration
3. Loading states
4. Error handling (WebGL fallback)
5. Mobile touch handling

**Deliverable:** Seamless section flow

### Phase 7: Optimization
1. Performance profiling
2. Code splitting verification
3. Texture compression
4. Dynamic quality scaling
5. Cross-browser testing
6. Accessibility (reduced motion, keyboard nav)

**Deliverable:** Production-ready performance

### Phase 8: Content & Deployment
1. Real content integration
2. SEO meta tags
3. Analytics setup
4. Deploy to Vercel/Netlify
5. Final testing

**Deliverable:** Live portfolio website

## Key Technical Decisions

### Why TresJS over TroisJS?
- TresJS v5 is actively maintained (2025 release)
- WebGPU experimental support
- Better Vue 3 Composition API integration
- TroisJS last major update was 2021

### Why GSAP over Alternatives?
- Industry standard for scroll animations
- Excellent Three.js integration
- ScrollSmoother for GPU-accelerated smoothing
- Better performance than CSS scroll animations

### Shader Strategy
- Use vite-plugin-glsl for hot reload
- Modular shader files (.glsl)
- Uniforms for animation (time, mouse, scroll)
- Mobile optimization (mediump precision)

## Potential Challenges

| Challenge | Solution |
|-----------|----------|
| High GPU usage on mobile | Dynamic quality scaling, reduce particles |
| Slow initial load | Code splitting, lazy loading, progressive enhancement |
| ScrollTrigger sync issues | Use GSAP onUpdate, avoid RAF conflicts |
| Memory leaks | Proper cleanup in onBeforeUnmount |
| iOS Safari quirks | Test early, mobile-first approach |

## Content Data

### Work Experience
- **Front-End Developer** at Tigloo (2020-current, Ramat Gan)
- **Shift Supervisor** at Bezek International (2014-2016, Petah Tiqwa)
- **Sales Representative** at Clal Insurance (2012-2014)

### Projects
1. **Final Project** - Android app using Firebase
2. **Chat App** - Full stack with React + Node + Express + Socket.io

### Skills
JavaScript, HTML, React.js, Node.js, Rest APIs, SASS, Vue, GIT

### Contact
- Email: idoisher2@gmail.com
- Location: Rosh Ashlain, Israel
- Portfolio: https://portfoliolo.firebaseapp.com/
- LinkedIn, Github

## Resources

- [TresJS Docs](https://tresjs.org/)
- [Three.js Docs](https://threejs.org/docs/)
- [GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)
- [The Book of Shaders](https://thebookofshaders.com/)
- [Bruno Simon's Portfolio](https://bruno-simon.com/) - Inspiration

---

# 🚀 ULTRA MODE: THE DEVELOPER'S QUANTUM UNIVERSE

## Vision: "A Portfolio That Will Shock"

Transform the portfolio into a cinematic 3D journey through 6 distinct "quantum realms" representing different aspects of your developer story, with 100,000+ GPU-accelerated particles and cutting-edge shader effects.

---

## 🌌 THE SIX QUANTUM REALMS

### SCENE 1: GENESIS EXPLOSION (Opening)
**Duration:** 0-10% scroll (0-500px)

**Concept:** The universe begins - a massive particle explosion representing the birth of a developer.

**3D Elements:**
- 50,000 particles start at origin (0,0,0)
- Explosive burst in all directions (sphere pattern)
- Secondary shock waves ripple outward
- Glitch effect distorts reality during peak explosion
- Particles coalesce into "IDO COHEN" text
- Text dissolves into next scene

**Shaders:**
- Chromatic aberration (RGB channel separation during explosion)
- God rays emanating from center
- Motion blur on fast-moving particles
- Glitch shader (horizontal scanline displacement)

**Camera:**
- Starts inside explosion point
- Rapid zoom backwards with shake
- Stabilizes as text forms

**Controls:**
- Auto-plays on page load
- Scroll to trigger text → particle transition

---

### SCENE 2: CODE OCEAN (Hero/Identity)
**Duration:** 10-30% scroll (500-1500px)

**Concept:** Floating above an infinite ocean made of flowing code particles.

**3D Elements:**
- 100,000 particles arranged in wave patterns
- Particles display actual code snippets as textures (Vue, React, JS)
- Floating islands of geometric code blocks
- Holographic name badge with fresnel glow
- Mouse creates ripples that push particles
- Schools of particle "fish" swim in formations

**Shaders:**
- Fluid simulation shader for wave motion
- Holographic shader (rainbow fresnel + scan lines)
- Depth of field (distant particles blur)
- Underwater caustics (light ripples)

**Camera:**
- Gentle bobbing motion (boat on waves)
- Mouse parallax (slight tilt based on cursor)
- Scroll zooms into ocean surface

**Interaction:**
- Click to spawn particle ripples
- Hover over code blocks to highlight

---

### SCENE 3: SKILLS VORTEX (About/Skills)
**Duration:** 30-50% scroll (1500-2500px)

**Concept:** DNA helix vortex with skill orbs orbiting, underwater atmosphere.

**3D Elements:**
- Double helix structure (two intertwined curves)
- Skill orbs (JavaScript, Vue, React, Node, etc.) orbit along helix
- 20,000 ambient particles create underwater effect
- Skill orbs have emissive glow and text labels
- Bubbles rise from below
- Light rays pierce from above

**Shaders:**
- Fresnel glow on orbs
- Distortion shader (underwater lens effect)
- Bloom on emissive orbs
- Volumetric god rays

**Camera:**
- Spiral rotation around helix
- Zoom into specific skill on click
- Slow drift upward with scroll

**Interaction:**
- Click skill orb → expands + shows proficiency level
- Raycaster hover detection
- Drag to rotate helix

---

### SCENE 4: PROJECT PORTALS (Projects Showcase)
**Duration:** 50-70% scroll (2500-3500px)

**Concept:** Spiral galaxy of spinning project portals, each a wormhole to a project.

**3D Elements:**
- Spiral galaxy arms made of 30,000 star particles
- 6-8 large portal rings (one per project) in galaxy
- Each portal shows project screenshot as texture
- Portal edges have particle trails
- Active portal pulls in surrounding particles
- Nebula clouds (soft gradient meshes)

**Shaders:**
- Portal distortion shader (swirl effect)
- Star glow (point sprites with custom shapes)
- Nebula shader (Perlin noise + gradient)
- Warp speed shader (elongated star trails on click)

**Camera:**
- Orbits galaxy from above
- Click portal → warp speed zoom through it
- Inside portal shows 3D project mockup

**Interaction:**
- Click portal → enter project view (3D phone/laptop model)
- Scroll rotates galaxy
- Mouse tilts camera angle

---

### SCENE 5: TIMELINE WORMHOLE (Work Experience)
**Duration:** 70-90% scroll (3500-4500px)

**Concept:** Journey through a time-bending wormhole with career milestones.

**3D Elements:**
- Tube geometry forming twisting tunnel
- Gradient rings pulse along tunnel
- 3 major nodes (Tigloo, Bezek, Clal) as glowing spheres
- Particle trails flow along tunnel walls
- Year labels float in space
- DOM overlay cards at each node

**Shaders:**
- Tunnel distortion shader (bend space-time)
- Flow map shader for particle trails
- Chromatic aberration at tunnel edges
- Pulsing gradient rings

**Camera:**
- Flies through tunnel following path
- Slows at each job node
- Barrel roll during transitions

**Interaction:**
- Scroll controls flight speed
- Click node → pause + expand card
- Auto-resume after 3 seconds

---

### SCENE 6: CONTACT NEXUS (Contact/Footer)
**Duration:** 90-100% scroll (4500-5000px)

**Concept:** All particles converge into a central nexus forming contact information.

**3D Elements:**
- 80,000 particles converge from all directions
- Form holographic contact card in center
- Particles orbit the card in rings
- Email, LinkedIn, GitHub icons as 3D models
- Gentle breathing animation (expand/contract)
- Thank you message appears

**Shaders:**
- Holographic shader with scan lines
- Particle convergence trails
- Fresnel glow on contact card
- Star field background

**Camera:**
- Slow zoom toward center
- Gentle rotation around card
- Final rest position: slight angle above

**Interaction:**
- Click icon → particles burst + redirect
- Hover → icon glows brighter
- Final scroll locks camera

---

## 🎨 SHADER LIBRARY (10 Advanced Effects)

### 1. Chromatic Aberration
**File:** `src/assets/shaders/effects/chromaticAberration.glsl`
```glsl
uniform float uIntensity;
uniform vec2 uDirection;

vec3 chromaticAberration(sampler2D tex, vec2 uv) {
  vec2 offset = uDirection * uIntensity;
  float r = texture2D(tex, uv + offset).r;
  float g = texture2D(tex, uv).g;
  float b = texture2D(tex, uv - offset).b;
  return vec3(r, g, b);
}
```

### 2. God Rays (Volumetric Light)
**File:** `src/assets/shaders/effects/godRays.glsl`
```glsl
uniform vec2 uLightPosition;
uniform float uExposure;
uniform float uDecay;
uniform float uWeight;

vec3 godRays(sampler2D tex, vec2 uv) {
  vec2 deltaUV = uv - uLightPosition;
  deltaUV *= 1.0 / 100.0 * uDecay;
  vec3 color = texture2D(tex, uv).rgb;
  float illumination = 1.0;

  for(int i = 0; i < 100; i++) {
    uv -= deltaUV;
    vec3 sample = texture2D(tex, uv).rgb;
    sample *= illumination * uWeight;
    color += sample;
    illumination *= uDecay;
  }

  return color * uExposure;
}
```

### 3. Holographic Shader
**File:** `src/assets/shaders/materials/holographic.glsl`
```glsl
varying vec3 vNormal;
varying vec3 vViewPosition;
uniform float uTime;

void main() {
  vec3 normal = normalize(vNormal);
  vec3 viewDir = normalize(vViewPosition);

  // Fresnel
  float fresnel = pow(1.0 - dot(normal, viewDir), 3.0);

  // Rainbow gradient
  float hue = fresnel + uTime * 0.1;
  vec3 rainbow = vec3(
    sin(hue * 6.28318) * 0.5 + 0.5,
    sin(hue * 6.28318 + 2.094) * 0.5 + 0.5,
    sin(hue * 6.28318 + 4.189) * 0.5 + 0.5
  );

  // Scan lines
  float scanline = sin(vViewPosition.y * 50.0 + uTime * 5.0) * 0.5 + 0.5;

  vec3 color = rainbow * fresnel * scanline;
  gl_FragColor = vec4(color, fresnel * 0.7);
}
```

### 4. Glitch Effect
**File:** `src/assets/shaders/effects/glitch.glsl`
```glsl
uniform float uGlitchIntensity;
uniform float uTime;

vec2 glitch(vec2 uv) {
  float glitch = step(0.9, sin(uTime * 10.0));
  uv.x += glitch * (fract(sin(uv.y * 10.0) * 43758.5453) - 0.5) * uGlitchIntensity;
  return uv;
}
```

### 5. Particle Morphing System
**File:** `src/assets/shaders/particles/morph.glsl`
```glsl
attribute vec3 positionStart;
attribute vec3 positionTarget;
uniform float uMorphProgress;

vec3 morphPosition() {
  return mix(positionStart, positionTarget, uMorphProgress);
}
```

### 6. Fluid Wave Shader
**File:** `src/assets/shaders/effects/fluidWave.glsl`
```glsl
uniform float uTime;
uniform float uWaveAmplitude;
uniform float uWaveFrequency;

float wave(vec2 pos) {
  return sin(pos.x * uWaveFrequency + uTime) *
         sin(pos.y * uWaveFrequency * 0.7 + uTime * 0.7) *
         uWaveAmplitude;
}
```

### 7. Warp Speed Shader
**File:** `src/assets/shaders/effects/warpSpeed.glsl`
```glsl
uniform float uWarpSpeed;
uniform vec3 uWarpDirection;

void main() {
  vec3 pos = position;
  float dist = length(pos);
  vec3 dir = normalize(pos);

  // Stretch particles along direction
  pos += dir * uWarpSpeed * dist * 0.5;

  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
  gl_PointSize = 10.0 * (1.0 + uWarpSpeed * 2.0);
}
```

### 8. Depth of Field
**File:** `src/assets/shaders/effects/dof.glsl`
```glsl
uniform float uFocusDistance;
uniform float uAperture;

vec3 depthOfField(sampler2D tex, sampler2D depth, vec2 uv) {
  float d = texture2D(depth, uv).r;
  float blur = abs(d - uFocusDistance) * uAperture;

  // Simplified bokeh blur
  vec3 color = vec3(0.0);
  float samples = 5.0;
  for(float i = 0.0; i < samples; i++) {
    float angle = i * 6.28318 / samples;
    vec2 offset = vec2(cos(angle), sin(angle)) * blur * 0.01;
    color += texture2D(tex, uv + offset).rgb;
  }
  return color / samples;
}
```

### 9. Bloom Effect
**File:** `src/assets/shaders/effects/bloom.glsl`
```glsl
uniform float uBloomIntensity;
uniform float uBloomThreshold;

vec3 bloom(sampler2D tex, vec2 uv) {
  vec3 color = texture2D(tex, uv).rgb;
  float brightness = dot(color, vec3(0.2126, 0.7152, 0.0722));

  if(brightness > uBloomThreshold) {
    return color * uBloomIntensity;
  }
  return vec3(0.0);
}
```

### 10. Distortion Shader (Underwater/Portal)
**File:** `src/assets/shaders/effects/distortion.glsl`
```glsl
uniform float uDistortionStrength;
uniform float uTime;

vec2 distort(vec2 uv) {
  uv += sin(uv.y * 10.0 + uTime) * uDistortionStrength;
  uv += cos(uv.x * 10.0 + uTime * 0.7) * uDistortionStrength;
  return uv;
}
```

---

## 🏗️ UPDATED IMPLEMENTATION PHASES

### PHASE 1: ✅ Foundation Setup (COMPLETE)
- Vite + Vue 3 + TypeScript
- TresJS, Three.js, GSAP installed
- Basic scene running

### PHASE 2: GPU Particle System (100k particles)
**Files to create:**
1. `src/composables/useGPUParticles.ts` - Advanced particle manager
2. `src/assets/shaders/particles/gpuVertex.glsl` - 100k particle vertex
3. `src/assets/shaders/particles/gpuFragment.glsl` - Optimized fragment
4. Update `ParticleField.vue` for 100k support

**Key features:**
- GPU-based position calculations
- Instanced rendering
- LOD system (reduce count on low FPS)
- Particle pool recycling

### PHASE 3: Shader Library
**Files to create:**
1. All 10 shader files listed above
2. `src/utils/shaderManager.ts` - Shader loader/compiler
3. `src/composables/useShaders.ts` - Vue integration

### PHASE 4: Scene 1 - Genesis Explosion
**Files to create:**
1. `src/components/three/scenes/GenesisExplosion.vue`
2. `src/assets/shaders/genesis/explosion.glsl`
3. Update `App.vue` with scene router

**Deliverable:** Explosive opening sequence

### PHASE 5: Scene 2 - Code Ocean
**Files to create:**
1. `src/components/three/scenes/CodeOcean.vue`
2. `src/assets/shaders/ocean/waves.glsl`
3. `src/utils/codeTextureGenerator.ts` - Generate code textures

**Deliverable:** Flowing code particle ocean

### PHASE 6: Scene 3 - Skills Vortex
**Files to create:**
1. `src/components/three/scenes/SkillsVortex.vue`
2. `src/utils/helixCurve.ts` - DNA helix path generator
3. `src/components/three/SkillOrb.vue` - Individual skill sphere

**Deliverable:** Interactive skill helix

### PHASE 7: Scene 4 - Project Portals
**Files to create:**
1. `src/components/three/scenes/ProjectPortals.vue`
2. `src/components/three/Portal.vue` - Single portal component
3. `src/assets/shaders/portal/warp.glsl`

**Deliverable:** Galaxy of project portals

### PHASE 8: Scene 5 - Timeline Wormhole
**Files to create:**
1. `src/components/three/scenes/TimelineWormhole.vue`
2. `src/utils/tunnelPath.ts` - Curved path through time
3. `src/assets/shaders/wormhole/tunnel.glsl`

**Deliverable:** Career journey wormhole

### PHASE 9: Scene 6 - Contact Nexus
**Files to create:**
1. `src/components/three/scenes/ContactNexus.vue`
2. `src/assets/shaders/nexus/convergence.glsl`

**Deliverable:** Particle convergence finale

### PHASE 10: Scene Transitions & Polish
1. GSAP scroll choreography between scenes
2. Camera path animations
3. Loading screen with progress bar
4. Performance monitoring
5. Mobile optimization

### PHASE 11: Post-Processing Pipeline
**Files to create:**
1. `src/components/three/PostProcessing.vue`
2. Install `@tresjs/post-processing`
3. Configure EffectComposer with all effects

**Deliverable:** Film-quality rendering

### PHASE 12: Final Polish & Deploy
1. Content refinement
2. Cross-browser testing
3. Performance targets: 60 FPS desktop, 30 FPS mobile
4. Deploy to Vercel
5. Analytics integration

---

## 🎯 PERFORMANCE TARGETS

| Metric | Desktop | Mobile |
|--------|---------|--------|
| FPS | 60 | 30 |
| Particle Count | 100,000 | 10,000 |
| Load Time | < 3s | < 5s |
| Memory | < 500MB | < 200MB |

## 🚀 EXPECTED IMPACT

**"SHOCK FACTOR" Checklist:**
- ✅ Opening explosion immediately grabs attention
- ✅ 100k particles = visually dense and impressive
- ✅ 6 distinct 3D scenes = journey, not static page
- ✅ Advanced shaders = professional film-quality
- ✅ Interactive elements = engaging, not passive
- ✅ Smooth 60 FPS = polished, not janky
- ✅ Tells developer story = memorable narrative

**Result:** A portfolio that stands out from 99.99% of developer portfolios and demonstrates mastery of cutting-edge web technology.

---

## Next Steps

1. ✅ Update PLAN.md (THIS FILE)
2. 🔄 Build 100k GPU particle system (IN PROGRESS)
3. ⏳ Create shader library
4. ⏳ Implement 6 scenes sequentially
5. ⏳ Polish and deploy
