<template>
  <div>
    <div>
      <h1>Battle</h1>
      <h5>game state {{game_state}}</h5>
      <h5>timer {{timer}}</h5>
      <h5>winner {{winner}}</h5>
      <h5>player id turn {{player_id_turn}}</h5>
    </div>
    <div align="center">
      <canvas id="battle_field" class="canvas" :width=field_x_cells*field_render_multiplier :height=field_y_cells*field_render_multiplier />
    </div>
  </div>
</template>







<script>
const fabric = require("fabric").fabric;
import 'fabric';


    export default {
        name: "BattlePage",
        props: {
            id: '',
        },
        data() {
            return {
                socket_status: 'disconnect',
                text_status: 'Ожидание игроков...',
                game_state: '',
                player_id_turn: -1,
                unit_selected: false,
                selected_id: -1,
                selected_cellX: -1,
                selected_cellY: -1,
                field_width: 1000,
                field_height: 500,
                field_y_cells: 5,
                field_x_cells: 10,
                field_render_multiplier: 100,
                timer: 0,
                self_user_id: 1,
                winner: '',
                board: [[]]
            }
        },
        mounted() {
            this.canvas = new fabric.Canvas("battle_field");
            this.render_field();
            this.canvas.on('mouse:down', this.PlayerMoveHandler);
        },
        created() {
            this.connect()
        },
        methods: {
            connect() {
                //this.self_user_id = Number(this.$store.getters.USER_ID)
                this.chatSocket = new WebSocket(
                    'ws:' + '127.0.0.1:8000/ws/battle/' + this.$route.params.id + '/?' + '7c0611170a9ab069554c674ad3a539a68f302e2e');
                this.chatSocket.onopen = () => {
                    this.socket_status = "connected";
                    this.chatSocket.onmessage = ({data}) => {
                        let parsed_data = JSON.parse(data)
                        this.game_state = parsed_data.state
                        if (parsed_data.state === 'started') {
                          this.board = parsed_data.board
                          this.player_id_turn = parsed_data.player_id_turn
                          this.timer = parsed_data.timer
                        }else if (parsed_data.state === 'over'){
                          this.winner = parsed_data.winner
                        }
                        this.render_field();
                    };
                };
            },
            render_field(){
              this.canvas.clear()
              for (let y = 0; y < this.field_y_cells; y++){
                for (let x = 0; x < this.field_x_cells; x++){
                   this.canvas.add(new fabric.Rect({
                      left: x * this.field_render_multiplier,
                      top: y * this.field_render_multiplier ,
                      height: this.field_render_multiplier,
                      width: this.field_render_multiplier,
                      fill: (x+y) % 2 === 0 ? '#70bf5d' : '#a4e49d',
                      evented: false,
                      selectable: false,
                      game_object_type: 'field'
                    }));
                }
              }
              if (this.game_state === 'started'){
                for (let y = 0; y < this.board.length; y++){
                  for (let x = 0; x < this.board.length; x++){
                    if (this.board[y][x] !== null) {
                      this.canvas.add(new fabric.Triangle({
                        left: this.board[y][x].unit.x * this.field_render_multiplier,
                        top: this.board[y][x].unit.y * this.field_render_multiplier,
                        height: this.field_render_multiplier,
                        width: this.field_render_multiplier,
                        fill: '#000000',
                        evented: false,
                        selectable: false,
                        game_object_type: 'unit',
                        attack_points: this.board[y][x].unit.attack_points,
                        battle_class: this.board[y][x].unit.battle_class,
                        health_points: this.board[y][x].unit.health_points,
                        max_attack_range: this.board[y][x].unit.max_attack_range,
                        max_move_range: this.board[y][x].unit.max_move_range,
                        name: this.board[y][x].unit.name,
                        player_id: this.board[y][x].unit.player_id,
                        shield_level: this.board[y][x].unit.shield_level,
                      }));
                    }else{
                    }
                  }
                }
                if (this.unit_selected && this.board[this.selected_cellY][this.selected_cellX] !== null){
                  console.log(this.board[this.selected_cellY][this.selected_cellX].unit.max_attack_range)
                        this.canvas.add(new fabric.Rect({
                          left: (2 - this.board[this.selected_cellY][this.selected_cellX].unit.max_attack_range) * this.field_render_multiplier,
                          top: (2 - this.board[this.selected_cellY][this.selected_cellX].unit.max_attack_range) * this.field_render_multiplier,
                          height: (1 + 2 + 2 * this.board[this.selected_cellY][this.selected_cellX].unit.max_attack_range) * this.field_render_multiplier,
                          width: (1 + 2 + 2 * this.board[this.selected_cellY][this.selected_cellX].unit.max_attack_range) * this.field_render_multiplier,
                          fill: 'rgba(255, 0, 0, 0.4)',
                          evented: false,
                          selectable: false,
                          game_object_type: 'attack_range'
                        }));
                      }else{
                        this.unit_selected = false;
                      }
              }
              this.canvas.renderAll();
            },
            disconnect() {
                this.chatSocket.close();
                this.socket_status = "disconnected";
            },
            sendMove(cellX, cellY) {
                this.chatSocket.send(JSON.stringify({
                    'data': {'type': 'move', 'selected': {'x': this.selected_cellX, 'y': this.selected_cellY}, 'move': {'x': cellX, 'y': cellY}}
                }));
            },
            CordsIsAvailableToMove(cx, cy){
              let objects = this.canvas.getObjects()
              for (let i = 0; i < objects.length; i++) {
                  if (objects[i].game_object_type === 'unit' &&
                      (objects[i].left / this.field_render_multiplier === cx && objects[i].top / this.field_render_multiplier === cy)) {
                    if (objects[i].player_id === this.self_user_id){
                      return {status: 'self unit', index: i}
                    }
                  }
                }
             // return 'no way'
              return {status: 'ok'}
            },
            PlayerMoveHandler(e){
              let pointer = this.canvas.getPointer(e);
              let cellX = Math.trunc(pointer.x / this.field_render_multiplier);
              let cellY = Math.trunc(pointer.y / this.field_render_multiplier);
              let objects = this.canvas.getObjects()
              if (this.unit_selected){
                let check_res = this.CordsIsAvailableToMove(cellX, cellY)
                if (check_res.status === 'self unit') {
                    this.unit_selected = true;
                    this.selected_id = check_res.index
                    this.selected_cellX = objects[check_res.index].left / this.field_render_multiplier
                    this.selected_cellY = objects[check_res.index].top / this.field_render_multiplier
                }else {
                  console.log('send...')
                  this.sendMove(cellX, cellY)
                  console.log('send complete...')
                  this.unit_selected = false
                }
              }else {
                for (let i = 0; i < objects.length; i++) {
                  if (objects[i].game_object_type === 'unit' &&
                      (objects[i].left / this.field_render_multiplier === cellX && objects[i].top / this.field_render_multiplier === cellY)
                    && objects[i].player_id === this.self_user_id) {
                    this.unit_selected = true;
                    this.selected_id = i
                    this.selected_cellX = objects[i].left / this.field_render_multiplier
                    this.selected_cellY = objects[i].top / this.field_render_multiplier
                  }
                }
              }
              this.canvas.renderAll();
            },
        }
    }
</script>

<style scoped>

</style>