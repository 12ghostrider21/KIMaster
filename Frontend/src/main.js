import './assets/main.css'

import { createApp } from 'vue';

import App from './App.vue';
import BaseDialog from './components/UI/BaseDialog.vue'
import BaseButton from './components/UI/BaseButtons.vue'
import DragableImage from './components/UI/DragableImage.vue'
import Footer from './components/layout/Footer.vue'
import NavBar from './components/layout/NavBar.vue'
import BaseCard from './components/UI/BaseCard.vue'
import LanguageSwitcher from './components/layout/LanguageSwitcher.vue'



import store from '@/store/index.js';
import router from "@/router/index.js";
import i18n from './i18n';

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"


const app =createApp(App);

app.component('base-dialog',BaseDialog);
app.component('base-button',BaseButton);
app.component('footer-bar',Footer);
app.component('nav-bar',NavBar);
app.component('base-card', BaseCard);
app.component('dragable-image', DragableImage);
app.component('language-switcher', LanguageSwitcher);

app.use(store);
app.use(router);
app.use(i18n);

app.mount('#app');

