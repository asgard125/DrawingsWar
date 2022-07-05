<template>
  <info-header :info_header="info_header"></info-header>
  <div class="row d-flex col-6 mx-auto ">
    <button @click="getRoom" id="fight_btn" class="btn btn-primary bg-black" type="button">Button</button>
  </div>

</template>

<script>
import axios from 'axios';
import InfoHeader from "@/components/InfoHeader";

export default {
  name: "HomePage",
  components: {InfoHeader},
  data() {
    return {
      info_header:{
        game_name: '',
        level_score: 0,
        level: 0,
        money: 0,
      }
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

  },
  methods: {
    getRoom() {
      axios
          .get(axios.defaults.baseURL + "api/v1/battlesession/get_available_room")
          .then((response) => {
            console.log(response.data)
          })
    },
  }
}

</script>

<style scoped>
#fight_btn {
  font-size: 60px;
  margin: 0 0;
  height: 250px;
}
</style>