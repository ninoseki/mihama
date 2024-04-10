<script setup lang="ts">
import { fromThrowable } from 'neverthrow'
import major from 'semver/functions/major'
import { type PropType, computed, ref } from 'vue'

const props = defineProps({
  versions: {
    type: Array as PropType<string[]>,
    required: true
  }
})

const selectedMajorVersion = ref<string>()

const selectMajorVersion = (v: string) => {
  if (selectedMajorVersion.value === v) {
    selectedMajorVersion.value = undefined
  } else {
    selectedMajorVersion.value = v
  }
}

const safeMajor = fromThrowable(major)

const getMajorVersion = (v: string): string => {
  return safeMajor(v)
    .map((v) => v.toString())
    .unwrapOr(v.split('.')[0])
}

const groups = computed(() => {
  const map = new Map<string, string[]>()

  props.versions.forEach((v) => {
    const majorVersion = getMajorVersion(v)

    const versions = map.get(majorVersion) || []
    map.set(majorVersion, versions.concat([v]))
  })

  return map
})
</script>

<template>
  <div class="block" v-for="[majorVersion, versions] of Array.from(groups)" :key="majorVersion">
    <p @click="selectMajorVersion(majorVersion)">
      <span class="icon">
        <font-awesome-icon icon="caret-down" />
      </span>
      <span>{{ majorVersion }}.*</span>
    </p>
    <div class="tags mt-2" v-if="majorVersion == selectedMajorVersion">
      <span class="tag" v-for="version in versions" :key="version">{{ version }}</span>
    </div>
  </div>
</template>
