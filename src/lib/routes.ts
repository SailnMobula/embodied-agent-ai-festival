const base = import.meta.env.BASE_URL

export function overviewRoute(): string {
  return withBase('/')
}

export function stationRoute(id: string): string {
  return withBase(`/stations/${id}/`)
}

function withBase(path: string): string {
  return `${base.replace(/\/$/, '')}${path}`
}
