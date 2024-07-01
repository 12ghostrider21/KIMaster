// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/components/KIM_Pages/StartPage.vue';
import Lobby from '@/components/KIM_Pages/LobbyPage.vue';
import Play from '@/components/KIM_Pages/PlayPage.vue';
import Impressum from '@/components/ImpressumView.vue';
import About from '@/components/KIM_Pages/AboutView.vue';
import Wait from '@/components/KIM_Pages/WaitPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/lobby/:game',
      name: 'lobby',
      component: Lobby,
      props: true // pass route.params as props to Lobby component
    },
    {
      path: '/game/:game',
      name: 'play',
      component: Play,
      props: true,
    },
    {
      path: '/impressum',
      name: 'impressum',
      component: Impressum
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    {
      path: '/Lobby',
      name: 'wait',
      component: Wait
    },
  ]
});

export default router;
