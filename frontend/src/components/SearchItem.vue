<script setup lang="ts">
import { useRouteQuery } from '@vueuse/router'
import { onMounted, ref, watch } from 'vue'
import { useAsyncTask } from 'vue-concurrency'

import { API } from '@/api'
import Ecosystems from '@/components/EcosystemsWrapper.vue'
import Error from '@/components/ErrorItem.vue'
import Loading from '@/components/LoadingItem.vue'
import VulnTable from '@/components/VulnTable.vue'
import { type SearchResultsType, type VulnerabilityType } from '@/schemas'

const ecosystem = useRouteQuery<string | undefined>('ecosystem', undefined)
const q = useRouteQuery<string | undefined>('q', undefined)
const searchAfter = ref<(string | number)[]>()
const vulns = ref<VulnerabilityType[]>([])
const total = ref(0)

const searchTask = useAsyncTask<SearchResultsType, []>(async () => {
  return await API.search({
    q: q.value,
    ecosystem: ecosystem.value,
    searchAfter: searchAfter.value
  })
})

const search = async () => {
  const results = await searchTask.perform()
  vulns.value = vulns.value.concat(results.vulns)
  searchAfter.value = vulns.value[vulns.value.length - 1].sort
  total.value = results.total
}

const newSearch = async () => {
  total.value = 0
  vulns.value = []
  searchAfter.value = undefined
  await search()
}

const changeEcosystem = (newEcosystem?: string) => {
  ecosystem.value = newEcosystem
}

onMounted(async () => {
  await search()
})

watch(ecosystem, async () => {
  await newSearch()
})
</script>

<template>
  <div class="block">
    <div class="field has-addons">
      <p class="control is-expanded">
        <input class="input" type="text" placeholder="Package or ID" v-model="q" />
      </p>
      <p class="control">
        <a class="button" @click="newSearch">
          <span class="icon is-small">
            <font-awesome-icon icon="search" />
          </span>
          <span>Search</span>
        </a>
      </p>
    </div>
  </div>
  <div class="block">
    <Ecosystems @change="changeEcosystem" />
  </div>
  <Loading v-if="searchTask.isRunning" />
  <Error :error="searchTask.last?.error" v-if="searchTask.isError" />
  <VulnTable :vulns="vulns" />
  <button class="button" @click="search" v-if="vulns.length < total">Load more...</button>
</template>
