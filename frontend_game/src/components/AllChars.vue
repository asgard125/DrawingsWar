<template>
  <div class="charlist" v-for="char in all_chars" :key="char.id">
    <div class="charitem">
      <div class="row">
        <div class="col"><img :src="require(`../assets/${char.base_unit.name.toLowerCase()}.jpg`)"
                              alt="Картиночка пропала("></div>
        <div class="col"> Имя персонажа: {{ char.base_unit.name }}</div>
        <div class="col"> Цена: {{ char.base_unit.shop_price }}</div>
        <div class="col">
          <button @click="set_in_deck(char.id)" id="fight_btn" class="btn btn-primary bg-black" type="button">
            Добавить в колоду
          </button>
          <button @click="set_on_market(char.id, char.base_unit.shop_price)" id="fight_btn" class="btn btn-primary bg-black" type="button">
            Добавить на торговую
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AllChars",
  props: {
    all_chars: {
      type: Array,
    }
  },
  methods: {
    set_in_deck(id) {
      axios
          .put(axios.defaults.baseURL + "api/v1/playerbattleunit/" + id + "/", {
            action: "set_in_deck",
          })
      //this.$emit('add', id)
    },
    set_on_market(id, price){
      axios
          .put(axios.defaults.baseURL + "api/v1/playerbattleunit/" + id + "/", {
            action: "set_on_market",
            market_price: price,
          })
    }


  }
}
</script>

<style scoped>
.charitem{
  margin: 15px;
  text-align: center;
}
</style>