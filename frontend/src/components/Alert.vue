<template>
  <div class="alerts">
    <b-alert :show="dismissCountDown"
             dismissible
             fade
             variant="info"
             @dismissed="clearAlerts()"
             @dismiss-count-down="countDownChanged">
      <ul>Dismissed in: {{dismissCountDown}}
        <li v-for="(alert, i) in alerts" :key="i">{{alert}}</li>
      </ul>
    </b-alert>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'Alert',
  computed: {
    ...mapGetters('alert', {
      alerts: 'alerts',
      dismissCountDown: 'dismissCountDown'
    }),
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.$store.commit('alert/setDismissCountDown', dismissCountDown)
    },
    clearAlerts() {
      this.$store.commit('alert/setDismissCountDown', 0)
      this.$store.commit('alert/clear')
    }
  },
}
</script>

<style scoped>
.console-wrapper {
  order: 1;
}
.console {
  max-height: 25vh;
  height: 25vh;
  overflow-y: scroll;
  background: #1e394e;
  color: white;
  border-radius: 2%;
}
@media (min-width: 760px) {
  .console-wrapper {
    grid-column: 4 / 5;
    order: unset;
  }
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
