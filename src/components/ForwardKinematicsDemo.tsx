import { useEffect, useId, useRef, useState } from 'react'
import { chainPositions, endEffectorOf, type Point, type Segment } from '@/lib/forwardKinematics'
import { anglesAt, appendFrame, durationOf, type Recording } from '@/lib/motionRecording'

const ORIGIN: Point = { x: 200, y: 320 }
const VIEWBOX = { width: 520, height: 380 }

const INITIAL_SEGMENTS: Segment[] = [
  { label: 'Shoulder', angleDegrees: 55, length: 120 },
  { label: 'Elbow', angleDegrees: -40, length: 100 },
  { label: 'Wrist', angleDegrees: -25, length: 60 },
]

type Mode = 'idle' | 'recording' | 'replaying'

export default function ForwardKinematicsDemo({ recorder = true }: { recorder?: boolean }) {
  const [segments, setSegments] = useState(INITIAL_SEGMENTS)
  const [recording, setRecording] = useState<Recording>([])
  const [mode, setMode] = useState<Mode>('idle')
  const startedAt = useRef(0)
  const instance = useId()

  const positions = chainPositions(ORIGIN, segments)
  const anglesOf = (of: Segment[]) => of.map((segment) => segment.angleDegrees)

  const updateAngle = (index: number, angleDegrees: number) => {
    const next = segments.map((segment, at) =>
      at === index ? { ...segment, angleDegrees } : segment,
    )
    setSegments(next)

    if (mode === 'recording') {
      setRecording((frames) =>
        appendFrame(frames, performance.now() - startedAt.current, anglesOf(next)),
      )
    }
  }

  const startRecording = () => {
    startedAt.current = performance.now()
    setRecording([{ atMs: 0, angles: anglesOf(segments) }])
    setMode('recording')
  }

  const stopRecording = () => {
    setRecording((frames) =>
      appendFrame(frames, performance.now() - startedAt.current, anglesOf(segments)),
    )
    setMode('idle')
  }

  useEffect(() => {
    if (mode !== 'replaying') return

    const playbackStartedAt = performance.now()
    let request = 0

    const tick = () => {
      const elapsed = performance.now() - playbackStartedAt
      const angles = anglesAt(recording, elapsed)
      setSegments((current) =>
        current.map((segment, joint) => ({ ...segment, angleDegrees: Math.round(angles[joint]) })),
      )

      if (elapsed >= durationOf(recording)) {
        setMode('idle')
        return
      }
      request = requestAnimationFrame(tick)
    }

    request = requestAnimationFrame(tick)
    return () => cancelAnimationFrame(request)
  }, [mode, recording])

  return (
    <figure className="my-10 overflow-hidden rounded-card border border-border bg-card">
      <div className="grid gap-6 p-6 md:grid-cols-[1.3fr_1fr] md:items-center">
        <ArmDrawing positions={positions} />
        <div className="flex flex-col gap-5">
          {segments.map((segment, index) => (
            <AngleSlider
              key={segment.label}
              sliderId={`${instance}-${segment.label.toLowerCase()}`}
              segment={segment}
              disabled={mode === 'replaying'}
              onChange={(angleDegrees) => updateAngle(index, angleDegrees)}
            />
          ))}
          <EndEffectorReadout position={endEffectorOf(positions)} />
          {recorder && (
            <RecorderControls
              mode={mode}
              recording={recording}
              onRecord={startRecording}
              onStop={stopRecording}
              onReplay={() => setMode('replaying')}
              onReset={() => {
                setSegments(INITIAL_SEGMENTS)
                setRecording([])
                setMode('idle')
              }}
            />
          )}
        </div>
      </div>
      <figcaption className="border-t border-border px-6 py-3 text-sm text-muted-foreground">
        {recorder
          ? 'Record the angles over time and the same motion plays back.'
          : 'Angles in, hand position out.'}
      </figcaption>
    </figure>
  )
}

function RecorderControls({
  mode,
  recording,
  onRecord,
  onStop,
  onReplay,
  onReset,
}: {
  mode: Mode
  recording: Recording
  onRecord: () => void
  onStop: () => void
  onReplay: () => void
  onReset: () => void
}) {
  const seconds = (durationOf(recording) / 1000).toFixed(1)

  return (
    <div className="flex flex-col gap-3">
      <div className="flex flex-wrap gap-2">
        {mode === 'recording' ? (
          <ControlButton onClick={onStop} active>
            Stop
          </ControlButton>
        ) : (
          <ControlButton onClick={onRecord} disabled={mode === 'replaying'}>
            Record
          </ControlButton>
        )}
        <ControlButton
          onClick={onReplay}
          disabled={mode !== 'idle' || recording.length < 2}
          active={mode === 'replaying'}
        >
          Replay
        </ControlButton>
        <ControlButton onClick={onReset} disabled={mode === 'recording'}>
          Reset
        </ControlButton>
      </div>
      <p className="font-mono text-xs text-muted-foreground" aria-live="polite">
        {mode === 'recording' && 'recording…'}
        {mode === 'replaying' && 'replaying…'}
        {mode === 'idle' &&
          (recording.length < 2
            ? 'wave.json, empty'
            : `wave.json, ${recording.length} frames · ${seconds} s`)}
      </p>
    </div>
  )
}

function ControlButton({
  onClick,
  disabled,
  active,
  children,
}: {
  onClick: () => void
  disabled?: boolean
  active?: boolean
  children: string
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`rounded-pill border px-5 py-2 text-sm font-bold disabled:opacity-40 ${
        active
          ? 'border-accent text-accent-foreground'
          : 'border-border-strong text-card-foreground enabled:hover:border-accent'
      }`}
    >
      {children}
    </button>
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
        stroke="var(--color-ex-grey-600)"
        strokeWidth={10}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {positions.slice(0, -1).map((point, index) => (
        <circle key={index} cx={point.x} cy={point.y} r={9} fill="var(--color-foreground)" />
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

function AngleSlider({
  sliderId,
  segment,
  disabled,
  onChange,
}: {
  sliderId: string
  segment: Segment
  disabled: boolean
  onChange: (value: number) => void
}) {
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
        disabled={disabled}
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
