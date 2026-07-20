import { useState } from 'react'
import { chainPositions, endEffectorOf, type Point, type Segment } from '@/lib/forwardKinematics'

const ORIGIN: Point = { x: 200, y: 320 }
const VIEWBOX = { width: 520, height: 380 }

const INITIAL_SEGMENTS: Segment[] = [
  { label: 'Shoulder', angleDegrees: 55, length: 120 },
  { label: 'Elbow', angleDegrees: -40, length: 100 },
  { label: 'Wrist', angleDegrees: -25, length: 60 },
]

export default function ForwardKinematicsDemo() {
  const [segments, setSegments] = useState(INITIAL_SEGMENTS)
  const positions = chainPositions(ORIGIN, segments)

  const updateAngle = (index: number, angleDegrees: number) =>
    setSegments(segments.map((segment, at) => (at === index ? { ...segment, angleDegrees } : segment)))

  return (
    <figure className="my-10 overflow-hidden rounded-card border border-border bg-card">
      <div className="grid gap-6 p-6 md:grid-cols-[1.3fr_1fr] md:items-center">
        <ArmDrawing positions={positions} />
        <div className="flex flex-col gap-5">
          {segments.map((segment, index) => (
            <AngleSlider
              key={segment.label}
              segment={segment}
              onChange={(angleDegrees) => updateAngle(index, angleDegrees)}
            />
          ))}
          <EndEffectorReadout position={endEffectorOf(positions)} />
          <button
            type="button"
            onClick={() => setSegments(INITIAL_SEGMENTS)}
            className="self-start rounded-pill border border-border-strong px-5 py-2 text-sm font-bold text-card-foreground hover:border-accent"
          >
            Reset
          </button>
        </div>
      </div>
      <figcaption className="border-t border-border px-6 py-3 text-sm text-muted-foreground">
        Forward kinematics: joint angles go in, the hand position comes out.
      </figcaption>
    </figure>
  )
}

function ArmDrawing({ positions }: { positions: Point[] }) {
  return (
    <svg
      viewBox={`0 0 ${VIEWBOX.width} ${VIEWBOX.height}`}
      className="w-full rounded-container bg-background"
      role="img"
      aria-label="Two-dimensional robot arm rendered from the current joint angles"
    >
      <GroundLine y={ORIGIN.y} />
      <polyline
        points={positions.map((point) => `${point.x},${point.y}`).join(' ')}
        fill="none"
        stroke="var(--color-ex-grey-400)"
        strokeWidth={10}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {positions.slice(0, -1).map((point, index) => (
        <circle key={index} cx={point.x} cy={point.y} r={9} fill="var(--color-ex-white)" />
      ))}
      <circle
        cx={endEffectorOf(positions).x}
        cy={endEffectorOf(positions).y}
        r={13}
        fill="var(--color-accent)"
      />
    </svg>
  )
}

function GroundLine({ y }: { y: number }) {
  return (
    <line
      x1={0}
      y1={y}
      x2={VIEWBOX.width}
      y2={y}
      stroke="var(--color-border-strong)"
      strokeWidth={2}
      strokeDasharray="6 8"
    />
  )
}

function AngleSlider({ segment, onChange }: { segment: Segment; onChange: (value: number) => void }) {
  const sliderId = `angle-${segment.label.toLowerCase()}`

  return (
    <div>
      <label htmlFor={sliderId} className="flex items-baseline justify-between text-sm font-bold">
        <span className="text-card-foreground">{segment.label}</span>
        <span className="font-mono text-muted-foreground tabular-nums">{segment.angleDegrees}°</span>
      </label>
      <input
        id={sliderId}
        type="range"
        min={-150}
        max={150}
        step={1}
        value={segment.angleDegrees}
        onChange={(event) => onChange(Number(event.target.value))}
        className="mt-2 w-full accent-[var(--color-accent)]"
      />
    </div>
  )
}

function EndEffectorReadout({ position }: { position: Point }) {
  return (
    <dl className="rounded-container bg-background px-4 py-3 font-mono text-sm">
      <dt className="text-xs text-muted-foreground">End effector</dt>
      <dd className="mt-1 text-foreground tabular-nums">
        x = {Math.round(position.x - ORIGIN.x)} &nbsp; y = {Math.round(ORIGIN.y - position.y)}
      </dd>
    </dl>
  )
}
