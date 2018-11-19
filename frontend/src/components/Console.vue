<template>
  <div class="console-wrapper">
    <div class="header d-flex justify-content-between align-items-center">
      <div class="d-flex">
      <h5>Status log</h5>
      <b-link @click="showCollapse = !showCollapse"
           :class="showCollapse ? 'collapsed' : null"
           aria-controls="collapse4"
           :aria-expanded="showCollapse ? 'true' : 'false'">
      {{ showCollapse ? '(hide)' : '(show)' }}
    </b-link>
    </div>
      <div>
        <b-button-group variant="info" class="align-self-end">
        <b-dropdown variant="info" left split v-bind="{ text: `${keep}` }">
          <b-dropdown-item @click="keep = 0">0</b-dropdown-item>
          <b-dropdown-item @click="keep = 1">1</b-dropdown-item>
          <b-dropdown-item @click="keep = 2">2</b-dropdown-item>
          <b-dropdown-item @click="keep = 3">3</b-dropdown-item>
          <b-dropdown-item @click="keep = 4">4</b-dropdown-item>
          <b-dropdown-item @click="keep = 5">5</b-dropdown-item>
        </b-dropdown>
          <b-button size="sm" variant="info" @click="clearLog(keep)"><small>Clear {{ keep === 0 ? "" : `(keep ${keep} lines)`}}</small></b-button>
        </b-button-group>
      </div>
    </div>
    <b-collapse v-model="showCollapse" class="console" id="logConsole" ref="consoleDiv">
      <p v-if="log.length > 0" v-for="(line, i) in log" :key="i">>>> {{ line }}</p>
       <p v-else>>>> {{ line }}</p>
    </b-collapse>
    <p v-if="!showCollapse">Latest status: {{ status }}</p>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'Console',
  data () {
    return {
      keep: 0,
      showCollapse: true,
      keepOptions: [
        { value: 0, text: 0},
        { value: 1, text: 1},
        { value: 2, text: 2},
        { value: 3, text: 3},
        { value: 4, text: 4},
        { value: 5, text: 5},
      ]
    }
  },
  computed: {
    ...mapGetters('log', {
      status: 'status',
      log: 'log',
    }),
  },
  methods: {
    scrollToBottom: function() {
      const el = document.querySelector('#logConsole')
      const scrollHeight = el.scrollHeight
      el.scrollTop = scrollHeight
    },
    clearLog() {
      this.$store.commit('log/clear', this.keep)
    }
  },
  updated() {
    this.scrollToBottom()
  }
}
</script>

<style scoped>
.console-wrapper {
  order: 5;
}
.console {
  height: 100%;
  max-height: 30vh;
  overflow-y: scroll;
  background: #1e394e;
  color: white;
  border-radius: 2%;
}
p {
  text-align: left;
  font-family: monospace;
  margin: 0;
}
h6 {
  text-align: left;
  margin-left: 0.5em;
}
p:last-child {
  margin-bottom: 2em;
}
</style>
