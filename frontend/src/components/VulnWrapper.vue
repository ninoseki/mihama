<script setup lang="ts">
import { onMounted } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import { API } from '@/api'
import Error from '@/components/ErrorItem.vue'
import Loading from '@/components/LoadingItem.vue'
import Vuln from '@/components/VulnItem.vue'
import { type VulnerabilityType } from '@/schemas'

const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

const getVulnTask = useAsyncTask<VulnerabilityType, []>(async () => {
  return await API.getVuln(props.id)
})

onMounted(async () => {
  await getVulnTask.perform()
})
</script>

<template>
  <Loading v-if="getVulnTask.isRunning" />
  <Error :error="getVulnTask.last?.error" v-if="getVulnTask.isError" />
  <Vuln :vuln="getVulnTask.last.value" v-if="getVulnTask.last?.value" />
</template>
