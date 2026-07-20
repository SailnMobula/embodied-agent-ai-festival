import { getCollection, type CollectionEntry } from 'astro:content'

export type Station = CollectionEntry<'stations'>

export type StationNeighbours = {
  previous: Station | undefined
  next: Station | undefined
}

export async function loadStationsInOrder(): Promise<Station[]> {
  return sortByOrder(await getCollection('stations'))
}

export function findNeighbours(stations: Station[], id: string): StationNeighbours {
  const position = stations.findIndex((station) => station.id === id)
  return {
    previous: stations[position - 1],
    next: stations[position + 1],
  }
}

export function startMinuteOf(stations: Station[], index: number): number {
  return stations.slice(0, index).reduce(sumDuration, 0)
}

export function totalMinutes(stations: Station[]): number {
  return stations.reduce(sumDuration, 0)
}

function sortByOrder(stations: Station[]): Station[] {
  return [...stations].sort((a, b) => a.data.order - b.data.order)
}

function sumDuration(total: number, station: Station): number {
  return total + station.data.durationMinutes
}
