<script>
import axios from 'axios';

import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import Trends from '@/components/Trends.vue';
import FeedItem from '@/components/FeedItem.vue';
import FeedForm from  '@/components/FeedForm.vue';

export default {
  name:'FeedView',
  components: {
    PeopleYouMayKnow,
    Trends,
    FeedItem, 
    FeedForm
},

  data(){
    return{
      posts: [],
      body: ''
    }
  },

  mounted() {
    this.getFeed()
  },

  methods: {
    getFeed() {
      axios
        .get('/api/posts')
        .then(response => {
          //console.log('data', response.data)

          this.posts = response.data
        })
        .catch(error => {
          console.log('error', error)
        })
    },

    submitForm(){
      console.log('submit form', this.body)

      axios
        .post('/api/posts/create/', {
          'body':this.body
        })
        .then(response => {
          console.log('data', response.data)

          this.posts.unshift(response.data)

          this.body = ''
        })
        .catch(error => {
          console.log('error', error)
        })
    },
    deletePost(id){
      console.log('delete post', id);
      this.posts = this.posts.filter(post => post.id !== id)
    }
  }


}

</script>

<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-center col-span-3 space-y-4">
      <div class=" bg-white border border-gray-200 rounded-lg">
        <FeedForm 
          v-bind:user="null"
          v-bind:posts="posts"
          v-on:deletePost="deletePost"
        />
      </div>

      <div 
        class="p-4 bg-white border border-gray-200 rounded-lg"
        v-for="post in posts"
        v-bind:key="post.id"
      > 
        <FeedItem v-bind:post="post" />
      </div>
    </div> 

    <div class="main-right col-span-1 space-y-4">
      <PeopleYouMayKnow />

      <Trends />
      
    </div>
  </div>
</template>