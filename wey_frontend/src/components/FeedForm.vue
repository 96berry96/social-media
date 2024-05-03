<script>
import axios from 'axios'
export default {
  props:{
    user: Object,
    posts: Array
  },

  data() {
    return {
      body: '',
      is_private: false,
      url: null,
    }
  },

  methods: {
    onFileChange(e){
      const file = e.target.files[0]
      this.url = URL.createObjectURL(file);
    },

    sendDirectMessage(){
      console.log('Send Messages');

      axios
        .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
        .then(response => {
          console.log(response.data);
          this.$router.push('/chat')
        })
        .catch(error => {
          console.log('error', error);
        })
    },
    sendFriendshipRequest(){
      axios
        .post(`/api/friends/${this.$route.params.id}/request/`)
        .then(response => {
          if(response.data.message === 'request already sent'){
            toast.info('The request has already been sent')
            this.can_send_friendship_request = false
          } else {
            toast.info('The request was sent')
          }
        })
        .catch(error => {
          console.log('error', error)
        })
    },
    getFeed() {
      axios
        .get(`/api/posts/profile/${this.$route.params.id}`)
        .then(response => {

          this.posts = response.data.posts
          this.user = response.data.user
          this.can_send_friendship_request = response.data.can_send_friendship_request
        })
        .catch(error => {
          console.log('error', error)
        })
    },

    submitForm(){
      let formData = new FormData()
      formData.append('image', this.$refs.file.files[0])
      formData.append('body', this.body)
      formData.append('is_private', this.is_private)
      axios
        .post('/api/posts/create/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        .then(response => {
          this.posts.unshift(response.data)

          this.body = ''
          this.is_private = false
          this.$refs.file.value = ''
          this.url = null

          if(this.user){
            this.user.posts_count += 1
          }
        })
        .catch(error => {
          console.log('error', error)
        })
    },

    logout() {
      this.userStore.removeToken()

      this.$router.push('/login')
    }

  }
}
</script>

<template>
<form @submit.prevent="submitForm" method="POST">
          <div class="p-4">

            <textarea class="p-4 w-full bg-gray-100 rounded-lg" v-model="body" placeholder="What are you thinking about"></textarea>

            <label>
              <input type="checkbox" v-model="is_private"> Private
            </label>

            <div id="previw" v-if="url">
              <img :src="url" class="w-[100px] mt-3 rounded-xl">
            </div>
          </div>

          <div class="p-4 border-t border-gray-100 flex justify-between">
            
            <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
              <input type="file" ref="file" @change="onFileChange">
              Attach Image
            </label>
            <button href="" class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
          </div>
      </form>
</template>