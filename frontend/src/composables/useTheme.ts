import { ref, onMounted } from 'vue'

type Theme = 'light' | 'dark'

const STORAGE_KEY = 'theme-preference'

// Shared state across all component instances
const isDark = ref(false)

function getSystemPreference(): Theme {
  if (typeof window === 'undefined') return 'light'
  return window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light'
}

function getStoredPreference(): Theme | null {
  if (typeof window === 'undefined') return null
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored === 'dark' || stored === 'light') {
    return stored
  }
  return null
}

function applyTheme(theme: Theme) {
  document.documentElement.setAttribute('data-theme', theme)
  isDark.value = theme === 'dark'
}

function toggle() {
  const newTheme: Theme = isDark.value ? 'light' : 'dark'
  localStorage.setItem(STORAGE_KEY, newTheme)
  applyTheme(newTheme)
}

function initTheme() {
  // Priority: stored preference > system preference
  const theme = getStoredPreference() ?? getSystemPreference()
  applyTheme(theme)
}

// Listen for system preference changes
function setupSystemListener() {
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')

  mediaQuery.addEventListener('change', (e) => {
    // Only auto-switch if no stored preference
    if (!getStoredPreference()) {
      applyTheme(e.matches ? 'dark' : 'light')
    }
  })
}

export function useTheme() {
  onMounted(() => {
    initTheme()
    setupSystemListener()
  })

  return {
    isDark,
    toggle
  }
}

// Initialize immediately to prevent flash of wrong theme
// This runs when the module is imported
if (typeof window !== 'undefined') {
  initTheme()
}
