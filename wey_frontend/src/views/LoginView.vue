<script>
import { RouterLink } from 'vue-router'
import axios from 'axios';

import { useUserStore } from '@/stores/user';

export default {
  setup() {
    const userStore = useUserStore()

    return {
      store: userStore
    }
  },
  data() {
    return{
      form: {
        email: '',
        password: '',
      },
      errors: []
    }
  },

  methods: {
    async submitForm(){
      this.erros = []

      if(this.form.email === '') {
        this.errors.push('Your email is missing')
      }

      if(this.form.password === '') {
        this.errors.push('Your password is missing')
      }

      if(this.errors.length === 0){
        await axios
          .post('/api/login/', this.form)
          .then(response => {
            this.store.setToken(response.data)
            axios.defaults.headers.common['Authorization'] = "Bearer " + response.data.access
          })
          .catch(error => {
            console.log('error', error)

            this.errors.push('The email or password are wrong')
          })
      }

      if(this.errors.length === 0){
        await axios
          .get('/api/me/')
          .then(response => {
            this.store.setUserInfo(response.data)

            this.$router.push('/feed')
          })
          .catch(error => {
            console.log('error', error);
          })
      }
    }
  }
}

</script>
<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Login</h1>

        <p class="mb-6 text-gray-500">
          Bem vindo a nossa pagina
        </p>

        <p class="font-bold">
          Don't have an account? <RouterLink to="/signup" class="underline">Click here</RouterLink>
        </p>
      </div>
    </div>

    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" v-on:submit.prevent="submitForm">
          <div>
            <label>E-mail</label>
            <input type="email" v-model="form.email" placeholder="Your email address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>
          <div>
            <label>Password</label>
            <input type="password" v-model="form.password" placeholder="Your Password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
          </template>


          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Login</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>