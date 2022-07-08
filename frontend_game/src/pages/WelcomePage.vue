<template>
  <div class="cover-container d-flex w-100 h-100 p-3 mx-auto flex-column">

    <main class="px-3 m-auto" id="cover">
      <h1>Добро пожаловать, странник.</h1>
      
      <p class="lead">Пожалуйста, войди если уже имел удовольствие общения с сей шедевром. Если нет, то скорее
        регистрируйся - не пожалеешь. П.С. Это не точно</p>
      <div class="row">
          <p class="lead">
            <router-link to="signup" class="btn btn-lg btn-secondary fw-bold border-white bg-black">Регистрация</router-link>
          </p>
          <p class="lead">
            <router-link to="login" class="btn btn-lg btn-secondary fw-bold border-white bg-black">Вход</router-link>
          </p>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: "WelcomePage"
}
</script>

<style scoped>
#cover{
  text-align: center;
}
</style>