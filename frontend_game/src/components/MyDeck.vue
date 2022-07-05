<template>
  <div class="row">
    <h1>Моя колода</h1>
    <div class="col" v-for="char in deck_chars" :key="char.id">
      <div class="deckitem">
        <img :src="require(`../assets/${char.base_unit.name.toLowerCase()}.jpg`)" alt="Картиночка пропала(">
        <div class=""> Имя персонажа: {{ char.base_unit.name }}</div>
      </div>
    </div>
  </div>
  <div class="row d-flex col-6 mx-auto ">
    <button id="fight_btn" class="btn btn-primary bg-black" type="button">Сохранить колоду и в бой</button>
    <button id="fight_btn" class="btn btn-primary bg-black" type="button">Очистить колоду</button>
  </div>

</template>

<script>
export default {
  name: "MyDeck",
  props:{
    deck_chars:{
      type: Array,
    }
  },
  methods:{
    //this.deck_chars = this.all_chars.filter(char => char.in_deck === true)
  }
}

</script>

<style scoped>

</style>