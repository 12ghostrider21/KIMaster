// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/components/KIM_Pages/StartPage.vue';
import Lobby from '@/components/KIM_Pages/LobbyPage.vue';
import Play from '@/components/KIM_Pages/PlayPage.vue';
import Impressum from '@/components/ImpressumView.vue';
import About from '@/components/KIM_Pages/AboutView.vue';
import Wait from '@/components/KIM_Pages/WaitPage.vue';
import Instructions from '@/components/KIM_Pages/InstructionsPage.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/',
      name: 'lobby',
      component: Lobby,
    },
    {
      path: '/',
      name: 'play',
      component: Play,
    },
    {
      path: '/',
      name: 'impressum',
      component: Impressum
    },
    {
      path: '/',
      name: 'about',
      component: About
    },
    {
      path: '/',
      name: 'wait',
      component: Wait
    },
    {
      path: '/',
      name: 'instruction',
      component: Instructions
    }
  ]
});


export default router;
