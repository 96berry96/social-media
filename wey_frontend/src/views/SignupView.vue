<script>
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { useToastStore } from '@/stores/toast';
import { toast } from 'vue3-toastify';

export default {
  setup() {
    const toastStore = useToastStore()

    return {
      toastStore
    }
  },

  data() {
    return {
      form:{
        email: '',
        name: '',
        password1: '',
        password2: ''
      },
      errors:[],
    }
  },

  methods: {
    submitForm() {
      this.errors = []

      if(this.form.email === '') {
        this.errors.push('Your email is missing')
      }

      if(this.form.name === '') {
        this.errors.push('Your name is missing')
      }

      if(this.form.password1 === '') {
        this.errors.push('Your password is missing')
      }

      if(this.form.password1 !== this.form.password2){
        this.errors.push('The password does not match')
      }

      if(this.errors.length === 0) {
        axios
          .post('/api/signup/', this.form)
          .then(response => {
            console.log(response.data)
            if(response.data.message === 'success') {
              toast.success('The user is registered Please activate your account by clicking on the link sent to your email. Please log in')
              this.form.email = ''
              this.form.name = ''
              this.form.password1 = ''
              this.form.password2 = ''
            } else {
              const data = JSON.parse(response.data.message)

              for (const key in data) {
                this.errors.push(data[key][0].message)
              }
              toast.error('Something went wrong')
            }
          })
          .catch(error => {
            console.log('error', error)
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
        <h1 class="mb-6 text-2xl">Sign up</h1>

        <p class="mb-6 text-gray-500">
          Bem vindo a nossa pagina
        </p>

        <p class="font-bold">
          Already have an account? <RouterLink :to="{name: 'login'}" class="underline">Click here</RouterLink>
        </p>
      </div>
    </div>

    <div class="main-right">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <form class="space-y-6" v-on:submit.prevent="submitForm">
          <div>
            <label>Name</label>
            <input type="text" v-model="form.name" placeholder="Your full name" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>
          <div>
            <label>E-mail</label>
            <input type="email" v-model="form.email" placeholder="Your email address" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>
          <div>
            <label>Password</label>
            <input type="password" v-model="form.password1" placeholder="Your Password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>
          <div>
            <label>Repeat Password</label>
            <input type="password" v-model="form.password2" placeholder="Your Password" class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
          </div>

          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
          </template>

          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Sign up</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>