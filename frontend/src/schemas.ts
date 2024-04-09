import { z } from 'zod'

export const EcosystemSchema = z.object({
  name: z.string(),
  total: z.number()
})

export type EcosystemType = z.infer<typeof EcosystemSchema>

export const EcosystemsSchema = z.object({
  ecosystems: z.array(EcosystemSchema),
  total: z.number()
})

export type EcosystemsType = z.infer<typeof EcosystemsSchema>

export const PackageSchema = z.object({
  ecosystem: z.string(),
  name: z.string(),
  purl: z.string().optional()
})

export type PackageType = z.infer<typeof PackageSchema>

export const AffectedSchema = z.object({
  package: PackageSchema.optional(),
  severity: z.any().optional(),
  ranges: z
    .array(
      z.object({
        type: z.string(),
        repo: z.string().optional(),
        events: z.array(z.object({}).catchall(z.any())),
        database_specific: z.object({}).catchall(z.any()).optional()
      })
    )
    .optional(),
  versions: z.array(z.string()).optional(),
  ecosystem_specific: z.object({}).catchall(z.any()).optional(),
  database_specific: z.object({}).catchall(z.any()).optional()
})

export type AffectedType = z.infer<typeof AffectedSchema>

export const VulnerabilitySchema = z.object({
  sort: z.array(z.number()).optional(),
  schema_version: z.string().optional(),
  id: z.string(),
  modified: z.any(),
  published: z.any().optional(),
  withdrawn: z.any().optional(),
  aliases: z.union([z.array(z.string()), z.null()]).optional(),
  related: z.array(z.string()).optional(),
  summary: z.string().optional(),
  details: z.string().optional(),
  severity: z.any().optional(),
  affected: z.union([z.array(AffectedSchema), z.null()]).optional(),
  references: z
    .union([
      z.array(
        z.object({
          type: z.string(),
          url: z.string()
        })
      ),
      z.null()
    ])
    .optional(),
  credits: z
    .array(
      z.object({
        name: z.string(),
        contact: z.array(z.string()).optional(),
        type: z.string().optional()
      })
    )
    .optional(),
  database_specific: z.object({}).catchall(z.any()).optional()
})

export type VulnerabilityType = z.infer<typeof VulnerabilitySchema>

export const SearchResultsSchema = z.object({
  total: z.number(),
  vulns: z.array(VulnerabilitySchema)
})

export type SearchResultsType = z.infer<typeof SearchResultsSchema>

export const ValidationErrorSchema = z.object({
  loc: z.array(z.string()),
  msg: z.string(),
  type: z.string()
})

export const ErrorDataSchema = z.object({
  detail: z.union([z.string(), z.array(ValidationErrorSchema)])
})

export type ErrorDataType = z.infer<typeof ErrorDataSchema>
