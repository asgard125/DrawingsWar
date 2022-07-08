<template>
  <info-header :info_header="info_header"></info-header>
  <div class="charlist" v-for="char in all_chars" :key="char.id">
    <div class="charitem">
      <div class="row col-8 mx-auto">
        <div class="col"><img :src="require(`../assets/${char.name.toLowerCase()}.jpg`)"
                              alt="Картиночка пропала("></div>
        <div class="col"> Класс: {{ char.name }}</div>
        <div class="col"> Цена: {{ char.shop_price }}</div>
        <div class="col"> Радиус атк: {{ char.max_attack_range }}</div>
        <div class="col"> Радиус пер: {{ char.max_move_range }}</div>
        <div class="col"> Макс атк: {{ char.max_attack_points }}</div>
        <div class="col"> Макс зщт: {{ char.max_shield_level }}</div>
        <div class="col"> Макс здр: {{ char.max_health_points }}</div>
        <div class="col">
          <button @click="shop(char.id)" id="fight_btn" class="btn btn-primary bg-black" type="button">
            Купить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import InfoHeader from "@/components/InfoHeader";
import axios from "axios";

export default {
  name: "ShopPage",
  components: {InfoHeader},
  data() {
    return {
      info_header: {
        game_name: '',
        level_score: 0,
        level: 0,
        money: 0,
      },
      all_chars: [],
    }
  },
  mounted() {
    axios
        .get(axios.defaults.baseURL + "api/v1/user/current_user")
        .then((response) => {
          this.info_header.game_name = response.data.user.game_name;
          this.info_header.money = response.data.user.money;
          this.info_header.level_score = response.data.user.level_score;
          this.info_header.level = this.info_header.level_score / 100;
        })
    axios
        .get(axios.defaults.baseURL + "api/v1/battleunit")
        .then((response) => {
          this.all_chars = response.data;
        })
  },
  methods: {
    shop(id) {
      axios
          .post(axios.defaults.baseURL + "api/v1/playerbattleunit/", {
            id: id
          })

    }
  }
}
</script>

<style scoped>
.charitem {
  text-align: center;
  margin: 25px;
}
</style>