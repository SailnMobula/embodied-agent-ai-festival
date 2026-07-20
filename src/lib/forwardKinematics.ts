export type Point = { x: number; y: number }

export type Segment = {
  label: string
  angleDegrees: number
  length: number
}

export function chainPositions(origin: Point, segments: Segment[]): Point[] {
  const positions = [origin]
  let heading = 0

  for (const segment of segments) {
    heading += segment.angleDegrees
    positions.push(translate(positions.at(-1)!, heading, segment.length))
  }

  return positions
}

export function endEffectorOf(positions: Point[]): Point {
  return positions.at(-1)!
}

function translate(from: Point, angleDegrees: number, length: number): Point {
  const radians = (angleDegrees * Math.PI) / 180
  return {
    x: from.x + Math.cos(radians) * length,
    y: from.y - Math.sin(radians) * length,
  }
}
