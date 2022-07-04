<template>
  <header class="p-3 bg-dark text-white">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li>
            <router-link to="/" class="nav-link px-2 text-secondary">Home</router-link>
          </li>
          <li>
            <router-link to="inventory" class="nav-link px-2 text-white">Inventory</router-link>
          </li>
          <li>
            <router-link to="shop" class="nav-link px-2 text-white">Shop</router-link>
          </li>
        </ul>
        <div class="row my-0">
          <div class="col p-2 bg-gradient">Уровень: {{ this.level }}</div>
          <div class="col p-2 bg-gradient">Никнейм: {{ this.game_name }}</div>
          <div class="col p-2 bg-gradient">Денежки: {{ this.money }}</div>
        </div>
      </div>
    </div>
  </header>
  <div class="row">
    <div class="col-6">
      <div class="charlist" v-for="char in all_chars">
        <div class="charitem">
          <div class="row">
            <div class="col"><img :src="require(`../assets/${char.base_unit.name.toLowerCase()}.jpg`)"
                                  alt="Картиночка пропала("></div>
            <div class="col"> Имя персонажа: {{ char.base_unit.name }}</div>
            <div class="col"> Цена: {{ char.base_unit.shop_price }}</div>
            <div class="col">
              <button @click="set_in_deck(char.id)" id="fight_btn" class="btn btn-primary bg-black" type="button">
                Button
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-6">
      <div class="row">
        <h1>Моя колода</h1>
        <div class="col" v-for="char in deck_chars">
          <div class="deckitem">
            <img :src="require(`../assets/${char.base_unit.name.toLowerCase()}.jpg`)" alt="Картиночка пропала(">
            <div class=""> Имя персонажа: {{ char.base_unit.name }}</div>
          </div>
        </div>
      </div>
      <div class="row d-flex col-6 mx-auto ">
        <button id="fight_btn" class="btn btn-primary bg-black" type="button">Button</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "InventoryPage",
  data() {
    return {
      game_name: '',
      level_score: 0,
      level: 0,
      money: 0,
      all_chars: [],
      deck_chars: []

    }
  },
  mounted() {
    axios
        .get(axios.defaults.baseURL + "api/v1/user/current_user")
        .then((response) => {
          console.log(response.data)
          this.game_name = response.data.user.game_name;
          this.money = response.data.user.money;
          this.level_score = response.data.user.level_score;
          this.level = this.level_score / 100;
        })
    axios
        .get(axios.defaults.baseURL + "api/v1/playerbattleunit")
        .then((response) => {
          console.log(response.data)
          this.all_chars = response.data;
          this.deck_chars = this.all_chars.filter(char => char.in_deck === true)
        })

  },
  methods: {
    set_in_deck(id) {
      axios
          .put(axios.defaults.baseURL + "api/v1/playerbattleunit/" +  id + "/" , {
            action: "set_in_deck",
          })
          .then((response) => {
            console.log(response.data);
          })
    }
  }
}

</script>

<style scoped>

</style>