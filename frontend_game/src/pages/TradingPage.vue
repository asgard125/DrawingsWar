<template>
  <info-header :info_header="info_header"></info-header>
  <div class="charlist" v-for="char in market_chars" :key="char.id">
    <div class="charitem">
      <div class="row col-8 mx-auto">
        <div class="col"><img :src="require(`../assets/${char.base_unit.name.toLowerCase()}.jpg`)"
                              alt="Картиночка пропала("></div>
        <div class="col"> Имя персонажа: {{ char.base_unit.name }}</div>
        <div class="col"> Цена: {{ char.base_unit.market_price }}</div>
        <div class="col"> Уровень: {{ char.base_unit.level }}</div>

        <div class="col">
          <button @click="market(char.id)" id="fight_btn" class="btn btn-primary bg-black" type="button">
            Купить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import InfoHeader from "@/components/InfoHeader";


export default {
  name: "TradingPage",
  components: {InfoHeader},
  data() {
    return {
      info_header:{
        game_name: '',
        level_score: 0,
        level: 0,
        money: 0,
      },
      all_chars: [],
      market_chars: []
    }
  },
  mounted() {
    axios
        .get(axios.defaults.baseURL + "api/v1/user/current_user")
        .then((response) => {
          console.log(response.data)
          this.info_header.game_name = response.data.user.game_name;
          this.info_header.money = response.data.user.money;
          this.info_header.level_score = response.data.user.level_score;
          this.info_header.level = this.info_header.level_score / 100;
        })
    axios
        .get(axios.defaults.baseURL + "api/v1/playerbattleunit")
        .then((response) => {
          console.log(response.data)
          this.all_chars = response.data;
          this.market_chars = this.all_chars.filter(char => char.on_market === true)
          console.log(this.market_chars)
        })
  },
  methods: {
    market(id) {
      axios
          .put(axios.defaults.baseURL + "api/v1/playerbattleunit/market_purchase/", {
            id: id
          })
    }
  }
}
</script>

<style scoped>

</style>