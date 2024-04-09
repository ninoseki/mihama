<script setup lang="ts">
import { onMounted } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import { API } from '@/api'
import Ecosystems from '@/components/EcosystemsItem.vue'
import { type EcosystemsType } from '@/schemas'

const emit = defineEmits<{
  change: [ecosystem: string | undefined]
}>()

const getEcosystemsTask = useAsyncTask<EcosystemsType, []>(async () => {
  return await API.getEcosystems()
})

const change = (ecosystem?: string) => {
  emit('change', ecosystem)
}

onMounted(async () => {
  await getEcosystemsTask.perform()
})
</script>

<template>
  <Ecosystems
    @change="change"
    :ecosystems="getEcosystemsTask.last.value"
    v-if="getEcosystemsTask.last?.value"
  />
</template>
