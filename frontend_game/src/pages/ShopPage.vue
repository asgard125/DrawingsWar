<template>
  <info-header :info_header="info_header"></info-header>

</template>

<script>
import InfoHeader from "@/components/InfoHeader";
import axios from "axios";

export default {
  name: "ShopPage",
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
}
</script>

<style scoped>

</style>