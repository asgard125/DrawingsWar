<template>
  <header class="p-3 bg-dark text-white">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li>
            <router-link to="home" class="nav-link px-2 text-secondary">Home</router-link>
          </li>
          <li>
            <router-link to="inventory" class="nav-link px-2 text-white">Inventory</router-link>
          </li>
          <li>
            <router-link to="shop" class="nav-link px-2 text-white">Shop</router-link>
          </li>
        </ul>
        <div class="row my-0">
          <div class="col p-2 bg-gradient">Уровень: {{ info_header.level }}</div>
          <div class="col p-2 bg-gradient">Никнейм: {{ info_header.game_name }}</div>
          <div class="col p-2 bg-gradient">Денежки: {{ info_header.money }}</div>
          <div class="col p-2 bg-gradient"><button @click="logout" id="fight_btn" class="btn btn-primary bg-white text-black" type="button">Выйти</button></div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: "InfoHeader",
  props: {
    info_header: {
      type: Object,
      required: true,
    }
  },
  methods: {
    logout(){
      this.$store.commit("removeToken")
      this.$store.commit("removeUserId")
      this.$router.push("login")
    }
  }
}
</script>

<style scoped>

</style>