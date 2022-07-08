<template>
  <div class="row align-items-center">
    <h1 id="title">Моя колода</h1>
    <div class="col" v-for="char in deck_chars" :key="char.id">
      <div class="deckitem">
        <img :src="require(`../assets/${char.base_unit.name.toLowerCase()}.jpg`)" alt="Картиночка пропала(">
        <div class=""> Имя персонажа: {{ char.base_unit.name }}</div>
        <button v-if="btn_visible" @click="delete_from_deck(char.id)" id="fight_btn" class="btn btn-primary bg-black" type="button">Удалить из колоды</button>
      </div>
    </div>
  </div>
  <div class="row d-flex col-6 mx-auto ">
    <button v-if="btn_visible" @click="this.$router.push('/')" id="fight_btn" class="btn btn-primary bg-black" type="button">Сохранить колоду и в бой</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "MyDeck",
  props:{
    deck_chars:{
      type: Array,
    },
    btn_visible: {
      type: Boolean,
      default: true,
    }
  },
  methods:{
    delete_from_deck(id){
      axios
          .put(axios.defaults.baseURL + "api/v1/playerbattleunit/" + id + "/", {
            action: "delete_from_deck",
          })
      //this.$emit('add', id)
    }
  }
}

</script>

<style scoped>
#title{
  text-align: center;
  margin-bottom: 25px;
  margin-top: 20px;
}
.deckitem{
  text-align: center;
  margin-bottom: 25px;
}
</style>