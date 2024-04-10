<script setup lang="ts">
import { type PropType, computed } from 'vue'
import VueJsonPretty from 'vue-json-pretty'
import 'vue-json-pretty/lib/styles.css'

import Versions from '@/components/VersionsItem.vue'
import { type AffectedType } from '@/schemas'

const props = defineProps({
  affected: {
    type: Object as PropType<AffectedType>,
    required: true
  }
})

const ranges = computed(() => {
  return props.affected.ranges || []
})

const versions = computed(() => {
  return props.affected.versions || []
})

const eventKeys = ['introduced', 'last_affected', 'limit', 'fixed']
const getEventKey = (event: any) => {
  return eventKeys.find((key) => {
    return key in event
  })
}
const getEventValue = (event: any) => {
  const key = getEventKey(event)
  if (key) {
    return event[key]
  }
  return undefined
}
</script>

<template>
  <table class="table is-fullwidth">
    <tr v-if="affected.package">
      <th>Package</th>
      <td>
        <div class="columns">
          <div class="column is-1"><strong>Name</strong></div>
          <div class="column">{{ affected.package.name }}</div>
        </div>
      </td>
    </tr>
    <tr v-if="ranges.length > 0">
      <th>Affected ranges</th>
      <td>
        <div v-for="(r, index) in ranges" :key="index">
          <div class="columns">
            <div class="column is-1"><strong>Type</strong></div>
            <div class="column">{{ r.type }}</div>
          </div>
          <div class="columns">
            <div class="column is-1"><strong>Events</strong></div>
            <div class="column">
              <ul>
                <li v-for="(e, index) in r.events" :key="index">
                  <strong>{{ getEventKey(e) }}</strong>
                  {{ getEventValue(e) }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </td>
    </tr>
    <tr v-if="versions.length > 0">
      <th>Affected versions</th>
      <td>
        <Versions :versions="versions" />
      </td>
    </tr>
    <tr v-if="affected.ecosystem_specific">
      <th>Ecosystem specific</th>
      <td>
        <VueJsonPretty :data="affected.ecosystem_specific" />
      </td>
    </tr>
  </table>
</template>

<style scoped>
table.table th {
  width: 240px;
}
</style>
