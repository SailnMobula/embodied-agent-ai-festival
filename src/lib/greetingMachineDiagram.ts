export type DiagramNode = {
  id: string
  x: number
  y: number
  width: number
  height: number
}

export type DiagramEdge = {
  from: string
  to: string
  path: string
  labelX: number
  labelY: number
  labelAnchor: 'start' | 'middle' | 'end'
}

export const DIAGRAM_VIEWBOX = { x: 0, y: 52, width: 780, height: 310 }

export const ENTRY_MARKER = { x: 16, y: 140, radius: 6, endX: 40 }

export const DIAGRAM_NODES: DiagramNode[] = [
  { id: 'idle', x: 100, y: 140, width: 120, height: 54 },
  { id: 'patrolling', x: 330, y: 140, width: 160, height: 54 },
  { id: 'personDetected', x: 590, y: 140, width: 200, height: 54 },
  { id: 'waving', x: 440, y: 320, width: 140, height: 54 },
]

export const DIAGRAM_EDGES: DiagramEdge[] = [
  {
    from: 'idle',
    to: 'patrolling',
    path: 'M 160 128 Q 205 92 250 128',
    labelX: 205,
    labelY: 80,
    labelAnchor: 'middle',
  },
  {
    from: 'patrolling',
    to: 'idle',
    path: 'M 250 152 Q 205 188 160 152',
    labelX: 205,
    labelY: 208,
    labelAnchor: 'middle',
  },
  {
    from: 'patrolling',
    to: 'personDetected',
    path: 'M 410 128 Q 450 92 490 128',
    labelX: 450,
    labelY: 80,
    labelAnchor: 'middle',
  },
  {
    from: 'personDetected',
    to: 'patrolling',
    path: 'M 490 152 Q 450 188 410 152',
    labelX: 450,
    labelY: 208,
    labelAnchor: 'middle',
  },
  {
    from: 'personDetected',
    to: 'waving',
    path: 'M 545 167 Q 520 240 495 293',
    labelX: 560,
    labelY: 246,
    labelAnchor: 'start',
  },
  {
    from: 'waving',
    to: 'patrolling',
    path: 'M 388 293 Q 340 240 330 167',
    labelX: 314,
    labelY: 246,
    labelAnchor: 'end',
  },
]

export function edgeOf(from: string, to: string): DiagramEdge {
  const edge = DIAGRAM_EDGES.find((candidate) => candidate.from === from && candidate.to === to)
  if (!edge) throw new Error(`No diagram edge for transition: ${from} to ${to}`)
  return edge
}
