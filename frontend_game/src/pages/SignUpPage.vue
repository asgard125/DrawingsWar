<template>
  <div class="col-6 m-auto">
    <body class="text-center">

    <main class="form-signin w-100 m-auto">
      <form @submit.prevent>
        <h1 class="h3 mb-3 fw-normal">Регистрируемся, не стесняемся или <router-link to="login">входим</router-link></h1>
        <div class="form-floating">
          <input v-model="username" type="text" class="form-control" id="floatingUsername" placeholder="Никнейм">
          <label  for="floatingUsername">Никнейм</label>
        </div>
        <div class="form-floating">
          <input v-model="game_name" type="text" class="form-control" id="floatingGamename" placeholder="Игровое имя">
          <label for="floatingGamename">Игровое имя</label>
        </div>
        <div class="form-floating">
          <input v-model="password" type="password" class="form-control" id="floatingPassword" placeholder="Пароль">
          <label for="floatingPassword">Пароль</label>
        </div>

        <button @click="signup" class="w-100 btn btn-lg btn-primary" type="submit">Зарегаться</button>
        <p class="mt-5 mb-3 text-muted">© 2017–2022</p>
      </form>
    </main>
    </body>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SignUpPage",
  data() {
    return {
      username: "",
      password: "",
      game_name: ""
    }
  },
  methods: {
    signup() {
      axios
          .post(axios.defaults.baseURL + "auth/users/", {
            username: this.username,
            password: this.password,
            game_name: this.game_name
          })
          .then((response) => {
            this.$router.push("login");
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