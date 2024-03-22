import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios from 'axios'
import Vue3Toasity from 'vue3-toastify'
import 'vue3-toastify/dist/index.css';

axios.defaults.baseURL = 'http://127.0.0.1:8000'

const app = createApp(App)

app.use(createPinia())
app.use(router, axios)
app.use(Vue3Toasity)

app.mount('#app')
