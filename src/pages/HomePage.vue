<template>

</template>

<script>
import axios from 'axios';

export default {
  name: "HomePage",
  data(){
    return {
      username:''
    }
  },
  mounted() {
    axios
        .get(axios.defaults.baseURL + "api/v1/user/current_user", {})
    console.log(sessionStorage.getItem("token"));
  }
}

</script>

<style scoped>

</style>