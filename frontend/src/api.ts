import axios from 'axios'

import {
  EcosystemsSchema,
  type EcosystemsType,
  SearchResultsSchema,
  type SearchResultsType,
  VulnerabilitySchema,
  type VulnerabilityType
} from '@/schemas'

const client = axios.create()

export const API = {
  async getVuln(id: string): Promise<VulnerabilityType> {
    const res = await client.get(`/v1/vulns/${id}`)
    return VulnerabilitySchema.parse(res.data)
  },

  async search({
    ecosystem,
    q,
    searchAfter
  }: {
    ecosystem?: string
    q?: string
    searchAfter?: number[]
  }): Promise<SearchResultsType> {
    const res = await client.get(`/v1/vulns/`, {
      params: {
        ecosystem,
        q,
        searchAfter
      }
    })
    return SearchResultsSchema.parse(res.data)
  },

  async getEcosystems(): Promise<EcosystemsType> {
    const res = await client.get(`/v1/ecosystems/`)
    return EcosystemsSchema.parse(res.data)
  }
}
