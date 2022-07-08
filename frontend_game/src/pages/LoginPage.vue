<template>
  <div class="col-6">
    <body class="text-center">

    <main class="form-signin w-100 m-auto">
      <form @submit.prevent>
        <h1 class="h3 mb-3 fw-normal">Please sign in</h1>
        <div class="form-floating">
          <input v-model="username" type="text" class="form-control" id="floatingInput" placeholder="Username">
          <label  for="floatingInput">Username</label>
        </div>
        <div class="form-floating">
          <input v-model="password" type="password" class="form-control" id="floatingPassword" placeholder="Password">
          <label for="floatingPassword">Password</label>
        </div>


        <button @click="login" class="w-100 btn btn-lg btn-primary" type="submit">Sign in</button>
        <p class="mt-5 mb-3 text-muted">© 2017–2022</p>
      </form>
    </main>
    </body>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
    }
  },
  methods: {
    login() {
      axios
          .post(axios.defaults.baseURL + "auth/token/login", {
            username: this.username,
            password: this.password
          })
          .then((response) => {
            console.log(response.data);
            const token = response.data.auth_token;
            axios.defaults.headers.common['Authorization'] = 'Token ' + token;
            localStorage.setItem('token', token);
            this.$router.push("home");
          })

    }
  }
}
</script>

<style scoped>
body {
  display: flex;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}
.w-100{
  width: 50%;
}
</style>