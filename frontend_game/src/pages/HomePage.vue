<template>
  <header class="p-3 bg-dark text-white">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li><router-link to="/" class="nav-link px-2 text-secondary">Home</router-link></li>
          <li><router-link to="inventory" class="nav-link px-2 text-white">Inventory</router-link></li>
          <li><router-link to="shop" class="nav-link px-2 text-white">Shop</router-link></li>
        </ul>
        <div class="row my-0">
          <div class="col p-2 bg-gradient">Уровень: {{ this.level }}</div>
          <div class="col p-2 bg-gradient">Никнейм: {{ this.game_name }}</div>
          <div class="col p-2 bg-gradient">Денежки: {{ this.money }}</div>
        </div>
      </div>
    </div>
  </header>
  <div class="row d-flex col-6 mx-auto ">
    <button id="fight_btn" class="btn btn-primary bg-black" type="button">Button</button>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  name: "HomePage",
  data(){
    return {
      game_name:'',
      level_score: 0,
      level: 0,
      money: 0,

    }
  },
  mounted() {
    axios
        .get(axios.defaults.baseURL + "api/v1/user/current_user")
        .then((response)=>{
          this.game_name = response.data.user.game_name;
          this.money = response.data.user.money;
          this.level_score = response.data.user.level_score;
          this.level = this.level_score / 100;
        })

  }
}

</script>

<style scoped>
#fight_btn{
  font-size: 60px;
  margin: 0 0;
  height: 250px;
}
</style>