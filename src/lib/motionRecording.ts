export type MotionFrame = {
  atMs: number
  angles: number[]
}

export type Recording = MotionFrame[]

export function appendFrame(recording: Recording, atMs: number, angles: number[]): Recording {
  return [...recording, { atMs, angles }]
}

export function durationOf(recording: Recording): number {
  return recording.at(-1)?.atMs ?? 0
}

export function anglesAt(recording: Recording, atMs: number): number[] {
  const first = recording.at(0)
  const last = recording.at(-1)
  if (!first || !last) return []
  if (atMs <= first.atMs) return first.angles
  if (atMs >= last.atMs) return last.angles

  const nextIndex = recording.findIndex((frame) => frame.atMs > atMs)
  const before = recording[nextIndex - 1]
  const after = recording[nextIndex]
  const progress = (atMs - before.atMs) / (after.atMs - before.atMs)

  return before.angles.map((angle, joint) => angle + (after.angles[joint] - angle) * progress)
}
