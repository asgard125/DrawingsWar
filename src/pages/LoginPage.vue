<template>
  <form class="login form">
    <div class="field">
      <label for="id_username">Username</label>
      <input
          v-model="username"
          type="text"
          placeholder="Username"
          autofocus="autofocus"
          maxlength="150"
          id="id_username"
      />
    </div>
    <div class="field">
      <label for="id_password">Password</label>
      <input
          v-model="password"
          type="password"
          placeholder="Password"
          id="id_password"
      />
    </div>
    <button @click.prevent="login" class="button primary" type="submit">
      Log In
    </button>
  </form>
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
            axios.defaults.headers.common["Authorization"] = "Token " + token;
            sessionStorage.setItem("token", token);
            this.$router.push("/");
          })
    }
  }
}
</script>

<style scoped>

</style>