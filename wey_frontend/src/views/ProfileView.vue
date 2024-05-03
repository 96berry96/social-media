<script>
import axios from 'axios';
import { toast } from 'vue3-toastify';

import { useUserStore } from '@/stores/user';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import FeedItem from '@/components/FeedItem.vue';
import { RouterLink } from 'vue-router';
import FeedForm from '@/components/FeedForm.vue';

export default {
  // 8a0f7d5f-a920-459a-ac9a-95fb3170c8c0
  // 40a213f8-c283-42a4-a801-15085cc9acc4
  name:'ProfileView',

  setup() {
    const userStore = useUserStore()

    return {
      userStore
    }
  },

  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem,
    RouterLink,
    FeedForm
},

  data(){
    return{
      posts: [],
      user: {
        id: null
      },
      body: '',
      is_private: false,
      url: null,
      can_send_friendship_request: null,
    }
  },

  mounted() {
    this.getFeed()
  },

  watch: {
    '$route.params.id': {
      handler:function() {
        this.getFeed()
      },
      deep: true,
      imediate:true
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

          this.user.posts_count += 1
        })
        .catch(error => {
          console.log('error', error)
        })
    },

    logout() {
      this.userStore.removeToken()

      this.$router.push('/login')
    },

    deletePost(id){
      this.posts = this.posts.filter(post => post.id !== id)
    }

  }


}

</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="pb-4 bg-white border border-gray-200 text-center rounded-lg">
        <img :src="user.get_avatar" class="mb-6 mt-2 mx-auto rounded-full">

        <p><strong>{{ user.name }}</strong></p>

        <div class="mt-6 flex space-x-8 justify-around" v-if="user.id">
          <RouterLink :to="{name: 'friends', params: {id: user.id}}" class="text-xs text-gray-500">{{ user.friends_count }} friends</RouterLink>
          <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
        </div>

        <div class="mt-6" >
          <button v-if="userStore.user.id !== user.id && can_send_friendship_request" class="inline-block py-4 px-3 bg-purple-600 text-xs text-white rounded-lg" @click="sendFriendshipRequest">Send friendship request</button>

          <button v-if="userStore.user.id !== user.id" class="inline-block mt-4 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg" @click="sendDirectMessage">Send Message</button>

          <RouterLink v-if="userStore.user.id === user.id" class="inline-block mr-4 py-4 px-3 bg-purple-600 text-xs text-white rounded-lg" to="/profile/edit">Edit Profile</RouterLink>

          <button v-if="userStore.user.id === user.id" class="inline-block py-4 px-3 bg-red-600 text-xs text-white rounded-lg" @click="logout">Log out</button>

        </div>
      </div>
    </div>

    <div class="main-center col-span-2 space-y-4">
      <div 
        class=" bg-white border border-gray-200 rounded-lg"
        v-if="userStore.user.id === user.id"
      >

        <FeedForm 
          v-bind:user="user"
          v-bind:posts="posts"
        />

        
      </div>

      <div 
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts"
        v-bind:key="post.id"
      >
        <FeedItem v-bind:post="post" v-on:deletePost="deletePost"/>
      </div>
    </div> 

    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />

      <Trends />
      
    </div>
  </div>
</template>

<style>
input[type="file"] {
  display: none;
}

.custom-file-upload {
  border: 1px solid #ccc;
  display: inline-block;
  padding: 6px 12px;
  cursor: pointer;
}
</style>