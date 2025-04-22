<template>
    <q-layout view="lHh Lpr lFf">
  
      
      <q-header elevated class="bg-primary text-white">
        <q-toolbar>
          <q-toolbar-title>
            AI Chatbot
          </q-toolbar-title>
        </q-toolbar>
      </q-header>
  
      
      <q-page-container>
        <router-view />
      </q-page-container>
  
    </q-layout>
  </template>
  
  <script setup>
  // No extra imports needed
  </script>
  
  <style scoped>
  .q-layout {
    min-height: 100vh;
  }
  </style>
  