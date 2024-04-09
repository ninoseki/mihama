import { library } from '@fortawesome/fontawesome-svg-core'
import { faMoon, faSearch, faSpinner, faSun } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import 'bulma-helpers/css/bulma-helpers.min.css'
import 'bulma/css/bulma.css'
import 'font-awesome-animation/css/font-awesome-animation.min.css'
import { createApp } from 'vue'

import App from '@/App.vue'
import router from '@/router'

library.add(faSearch, faSpinner, faSun, faMoon)

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(router)
app.mount('#app')
