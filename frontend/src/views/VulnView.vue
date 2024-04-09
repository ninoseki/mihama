<script setup lang="ts">
import { useTitle } from '@vueuse/core'
import { onMounted } from 'vue'

import Vuln from '@/components/VulnWrapper.vue'

const props = defineProps({
  id: {
    type: String,
    required: true
  }
})

onMounted(() => {
  useTitle(`${props.id} - Mihama`)
})
</script>

<template>
  <Vuln :id="id" />
</template>
