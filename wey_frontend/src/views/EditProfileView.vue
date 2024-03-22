<script>
import { RouterLink } from 'vue-router'
import axios from 'axios'
import { useToastStore } from '@/stores/toast'
import { useUserStore} from '@/stores/user'

export default {
  setup() {
      const toastStore = useToastStore()
      const userStore = useUserStore()
      return {
        toastStore,
        userStore,
      }
  },

  data() {
    return {
      errors: [],
      form: {
        email: this.userStore.user.email,
        name: this.userStore.user.name,
      }
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

      if(this.errors.length === 0) {
        axios
          .post('/api/editprofile/', this.form)
          .then(response => {
            if(response.data.message === 'profile updated') {
              
              this.toastStore.showToast(5000, 'The user was saved', 'bg-emerald-500')
            } else {
              console.log('Something went wrong');
              this.toastStore.showToast(5000, 'Something went wrong', 'bg-red-500')
            }
          })
          .catch(error => {
            console.log('error', error)
          })
      }
    }
  },
}
</script>


<template>
  <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
    <div class="main-left">
      <div class="p-12 bg-white border border-gray-200 rounded-lg">
        <h1 class="mb-6 text-2xl">Edit profile</h1>

        <p class="font-bold">
          Altere os detalhes da sua conta
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
          

          <template v-if="errors.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
            </div>
          </template>

          <div>
            <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Save changes</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>