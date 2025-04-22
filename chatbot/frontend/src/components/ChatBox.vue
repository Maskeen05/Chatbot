<template>
    <div class="q-pa-md">
      <q-card class="q-pa-md">
        <q-card-section>
          <div class="text-h6">Chat with AI</div>
        </q-card-section>
  
        <q-card-section>
          <div v-for="(msg, idx) in messages" :key="idx">
            <div><strong>{{ msg.sender }}:</strong> {{ msg.text }}</div>
          </div>
        </q-card-section>
  
        <q-card-section>
          <q-input
            v-model="userInput"
            @keyup.enter="sendMessage"
            filled
            label="Type your question"
          />
          <q-btn @click="sendMessage" label="Send" class="q-mt-sm" color="primary" />
        </q-card-section>
      </q-card>
    </div>
  </template>
  
<script setup>
import { ref } from 'vue'
import { getAnswer } from 'src/services/api' 

const userInput = ref('')
const messages = ref([
  { sender: 'System', text: 'Ask me anything about student data.' }
])

const sendMessage = async () => {
  if (!userInput.value) return

  const userMsg = userInput.value
  messages.value.push({ sender: 'You', text: userMsg })
  userInput.value = ''
  
  try {
    // Call the backend API to fetch answer
    const response = await getAnswer(userMsg)
    messages.value.push({ sender: 'Bot', text: response })
  } catch (err) {
    console.error(err)
    messages.value.push({ sender: 'Error', text: 'Something went wrong!' })
  }
}
  </script>
  
  <style scoped>
  .q-card {
    max-width: 600px;
    margin: 0 auto;
  }
  </style>
