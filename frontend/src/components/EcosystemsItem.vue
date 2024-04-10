<script setup lang="ts">
import { type PropType, ref } from 'vue'

import { type EcosystemsType } from '@/schemas'

defineProps({
  ecosystems: {
    type: Object as PropType<EcosystemsType>,
    required: true
  }
})

const ecosystem = ref<string>()

const emit = defineEmits<{
  change: [newEcosystem: string | undefined]
}>()

const change = (newEcosystem?: string) => {
  ecosystem.value = newEcosystem
  emit('change', newEcosystem)
}
</script>

<template>
  <div class="field is-grouped is-grouped-multiline">
    <div class="control">
      <div class="tags has-addons" @click="change(undefined)">
        <span class="tag" :class="{ 'is-info is-light': ecosystem === undefined }"
          >All ecosystems</span
        >
        <span class="tag has-text-weight-bold">{{ ecosystems.total }}</span>
      </div>
    </div>
    <div class="control" v-for="e in ecosystems.ecosystems" :key="e.name">
      <div class="tags has-addons" @click="change(e.name)">
        <span class="tag" :class="{ 'is-info is-light': ecosystem === e.name }">{{ e.name }}</span>
        <span class="tag is-ghost has-text-weight-bold">{{ e.total }}</span>
      </div>
    </div>
  </div>
</template>
