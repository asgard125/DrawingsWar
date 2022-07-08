<template>
  <info-header :info_header="info_header"></info-header>

  <div class="row d-flex col-6 mx-auto ">
    <my-deck :deck_chars="deck_chars" :btn_visible="false"></my-deck>
    <button @click="enterRoom" id="fight_btn" class="btn btn-primary bg-black" type="button">Button</button>
  </div>

</template>

<script>
import axios from 'axios';
import InfoHeader from "@/components/InfoHeader";
import AllChars from "@/components/AllChars";
import MyDeck from "@/components/MyDeck";

export default {
  name: "HomePage",
  components: {MyDeck, AllChars, InfoHeader},
  data() {
    return {
      info_header:{
        game_name: '',
        level_score: 0,
        level: 0,
        money: 0,
      },
      deck_chars: [],
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
          const user_id = response.data.user.id
          localStorage.setItem('user_id', user_id);
          this.$store.commit("setUserId")
          console.log(this.$store.getters.TOKEN)
        })
    axios
        .get(axios.defaults.baseURL + "api/v1/playerbattleunit")
        .then((response) => {
          console.log(response.data)
          const all_chars = response.data
          this.deck_chars = all_chars.filter(char => char.in_deck === true)
        })

  },
  methods: {
    enterRoom: function () {
      axios
          .get(axios.defaults.baseURL + "api/v1/battlesession/get_available_room")
          .then((response) => {
            const room_id = response.data.room_code
            this.$router.push({
              name: 'battle',
              params: {id: room_id}
            })
            console.log(response.data.room_code)
          })
    },
  }
}

</script>

<style scoped>
#fight_btn {
  font-size: 60px;
  margin-top: 15px;
  height: 250px;
}
</style>