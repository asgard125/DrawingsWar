<template>
  <info-header :info_header="info_header"></info-header>
  <div class="row">
    <div class="col-6">
      <all-chars :all_chars="all_chars"></all-chars>
    </div>
    <div class="col-6">
      <my-deck :deck_chars="deck_chars" :btn_visible="true"></my-deck>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import InfoHeader from "@/components/InfoHeader";
import AllChars from "@/components/AllChars";
import MyDeck from "@/components/MyDeck";

export default {
  name: "InventoryPage",
  components: {MyDeck, AllChars, InfoHeader},
  data() {
    return {
      info_header:{
        game_name: '',
        level_score: 0,
        level: 0,
        money: 0,
      },
      all_chars: [],
      deck_chars: []

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
          this.deck_chars = this.all_chars.filter(char => char.in_deck === true)
        })
  },
  methods: {

  },
}

</script>

<style scoped>

</style>