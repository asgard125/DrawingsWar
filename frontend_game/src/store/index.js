import {createStore} from "vuex";

export default createStore({
    state: {
        token: '',
        user_id: '',
        isAuthenticated: false
    },
    getters: {
        USER_ID : state => {
            return state.user_id
        },
        TOKEN : state => {
            return state.token
        }

    },
    mutations: {
        initializeStore(state) {
            if (localStorage.getItem('token')) {
                state.token = localStorage.getItem('token')
                state.isAuthenticated = true
            } else {
                state.token = ''
                state.isAuthenticated = false
            }
        },
        setToken(state, token) {
            state.token = token
            state.isAuthenticated = true
        },
        removeToken(state) {
            state.token = ''
            state.isAuthenticated = false
        },
        setUserId(state){
            state.user_id = localStorage.getItem("user_id");
        },
    }
}
)