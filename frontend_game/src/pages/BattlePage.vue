<template>
  <div>
    <div>
      <h1>Battle</h1>
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
                game_status: '',
                field_width: 1000,
                field_height: 500,
                field_y_cells: 5,
                field_x_cells: 10,
                field_render_multiplier: 100,
                field: [[]]
            }
        },
        mounted() {
            this.canvas = new fabric.Canvas("battle_field");
            for (let y = 0; y < this.field_y_cells; y++){
              for (let x = 0; x < this.field_x_cells; x++){
                   this.canvas.add(new fabric.Rect({
                      left: x * this.field_render_multiplier,
                      top: y * this.field_render_multiplier ,
                      height: this.field_render_multiplier,
                      width: this.field_render_multiplier,
                      fill: (x+y) % 2 === 0 ? '#70bf5d' : '#a4e49d',
                      evented: false,
                      selectable: false
                    }));
              }
            }
            this.canvas.renderAll();
            this.canvas.on('mouse:down', this.PlayerMoveHandler);
        },
        created() {
            // this.chatSocket = new WebSocket(
            //     'ws://' + '127.0.0.1:8000' +
            //     '/ws/chat/' + this.$route.params.id + '/');
            // this.chatSocket = new Socket('ws:' + '127.0.0.1:8000' +
            //     '/ws/chat/' + this.$route.params.id + '/');
            this.connect()
        },
        methods: {
            connect() {
                this.chatSocket = new WebSocket(
                    'ws:' + '127.0.0.1:8000/ws/battle/' + this.$route.params.id + '/');
                this.chatSocket.onopen = () => {
                    this.status = "connected";
                    this.dialogs.push({event: "Connected to", message: 'WomsChat'})
                    this.chatSocket.onmessage = ({data}) => {
                        this.dialogs.push(JSON.parse(data));
                        console.log(data);
                        console.log(this.dialogs)
                    };
                };
            },
            // Загрузка диалога
            // loadDialog() {
            //     console.log(this.chatSocket.onmessage);
            //     console.log(this.chatSocket)
            // },
            disconnect() {
                this.chatSocket.close();
                this.status = "disconnected";
                this.dialogs = [];
            },
            // Отправка сообщения
            sendMes(e) {
                this.chatSocket.send(JSON.stringify({
                    'message': this.form.textarea, 'username': sessionStorage.getItem("username")
                }));
                // this.dialogs.push({event: "Sent message", message: this.form.textarea});
                this.form.textarea = "";
            },
            setName(){
                sessionStorage.setItem("username", this.userName);
            },
            PlayerMoveHandler(e){
            let pointer = this.canvas.getPointer(e);
            let cellX = Math.trunc(pointer.x / this.field_render_multiplier);
            let cellY = Math.trunc(pointer.y / this.field_render_multiplier);
            console.log(cellX, cellY)
            },
        }
    }
</script>

<style scoped>
    .dialog {
        border: 1px solid #000;
    }
    .btn-send {
        margin: 60px 0 0 15px;
    }
</style>