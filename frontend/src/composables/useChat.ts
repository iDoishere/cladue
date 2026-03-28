import { ref } from 'vue'
import { chatWithAI } from '../services/ai.service'
import confetti from 'canvas-confetti'
import { toast } from 'vue3-toastify'
import 'vue3-toastify/dist/index.css'

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

const tabPrompts: Record<string, string> = {
  'Me': 'Tell me about Ido Cohen - who is he and what does he do?',
  'Projects': 'What projects has Ido worked on? Show me his best work.',
  'Skills': "What are Ido's technical skills and expertise levels?",
  'Fun': 'Tell me something fun or interesting about Ido!',
  'Contact': 'How can I contact Ido? What are his contact details?'
}

export function useChat() {
  const activeTab = ref('')
  const messages = ref<Message[]>([
    {
      role: 'assistant',
      content:
        "Hi! I'm Ido's AI assistant. Ask me about his experience, projects, or skills — or say **\"I want to reach out\"** and I'll help you send him a message directly.",
      timestamp: new Date()
    }
  ])
  const inputText = ref('')
  const showChat = ref(false)
  const isLoading = ref(false)

  async function handleTabClick(tab: string) {
    activeTab.value = tab
    inputText.value = ''
    showChat.value = true
    const message = tabPrompts[tab] || `Tell me about ${tab}`
    messages.value.push({ role: 'user', content: message, timestamp: new Date() })
    isLoading.value = true
    const aiResponse = await chatWithAI(message)
    isLoading.value = false
    messages.value.push({ role: 'assistant', content: aiResponse, timestamp: new Date() })
  }

  async function handleSendMessage() {
    if (!inputText.value.trim()) return
    showChat.value = true
    const userMessage = inputText.value
    inputText.value = ''
    messages.value.push({ role: 'user', content: userMessage, timestamp: new Date() })
    isLoading.value = true
    const aiResponse = await chatWithAI(userMessage)
    isLoading.value = false

    if (aiResponse.startsWith('EMAIL_SENT')) {
      confetti({
        particleCount: 120,
        spread: 70,
        origin: { y: 0.6 },
        colors: ['#7c3aed', '#a78bfa', '#4f46e5', '#fff']
      })
      toast.success('Message sent to Ido!', { autoClose: 4000, theme: 'dark' })
    }

    messages.value.push({
      role: 'assistant',
      content: aiResponse.replace(/^EMAIL_SENT\s*/, ''),
      timestamp: new Date()
    })
  }

  return {
    activeTab,
    messages,
    inputText,
    showChat,
    isLoading,
    handleTabClick,
    handleSendMessage
  }
}