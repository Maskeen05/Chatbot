<template>
    <q-page>
        <div class="q-mb-md">
        <q-input v-model="question" label="Ask a question" />
        <q-btn @click="askQuestion" label="Ask" color="primary" />
        </div>
        <div v-if="answer">
        <q-card>
            <q-card-section>
            <p>{{ answer }}</p>
            </q-card-section>
        </q-card>
        </div>
    </q-page>
    </template>
      
      <script setup>
      import { ref } from 'vue';
      import { getAnswer } from 'src/services/api';
      
      const question = ref('');
      const answer = ref('');
      
      const askQuestion = async () => {
      try {
        answer.value = await getAnswer(question.value);
        question.value = ''; // Clear the input field
      } catch (error) {
        console.error('Error fetching the answer:', error);
      }
    };
      </script>
      
      <style scoped>
      .q-page {
        max-width: 500px;
        margin: 0 auto;
        text-align: center;
      }
      </style>
      
    