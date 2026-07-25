import { useId, useState } from 'react'
import { greetingMachine } from '@/lib/greetingMachine'
import { stateById, transitionsFrom, type Transition } from '@/lib/stateMachine'
import {
  DIAGRAM_NODES,
  DIAGRAM_VIEWBOX,
  ENTRY_MARKER,
  edgeOf,
} from '@/lib/greetingMachineDiagram'

export default function StateMachineDemo() {
  const [currentId, setCurrentId] = useState(greetingMachine.initial)
  const [taken, setTaken] = useState<Transition | null>(null)
  const [preview, setPreview] = useState<Transition | null>(null)

  const current = stateById(greetingMachine, currentId)
  const options = transitionsFrom(greetingMachine, currentId)
  const highlighted = preview ?? taken

  const fire = (transition: Transition) => {
    setCurrentId(transition.to)
    setTaken(transition)
    setPreview(null)
  }

  const reset = () => {
    setCurrentId(greetingMachine.initial)
    setTaken(null)
    setPreview(null)
  }

  return (
    <figure className="my-10 overflow-hidden rounded-card border border-border bg-card">
      <MachineDiagram
        currentId={currentId}
        highlighted={highlighted}
        available={options}
        label={`State machine, currently in ${current.label}`}
      />

      <div className="grid gap-6 border-t border-border p-6 md:grid-cols-[1fr_1.2fr]">
        <div>
          <p className="text-sm font-bold text-muted-foreground">Current state</p>
          <p className="mt-1 text-lead font-bold text-card-foreground">{current.label}</p>
          <p className="mt-2 text-sm text-muted-foreground" aria-live="polite">
            {current.description}
          </p>
        </div>

        <div>
          <p className="text-sm font-bold text-muted-foreground">Possible events right now</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {options.map((transition) => (
              <button
                key={transition.event}
                type="button"
                onClick={() => fire(transition)}
                onMouseEnter={() => setPreview(transition)}
                onMouseLeave={() => setPreview(null)}
                onFocus={() => setPreview(transition)}
                onBlur={() => setPreview(null)}
                className="rounded-pill bg-foreground px-5 py-2.5 text-sm font-bold text-background hover:bg-accent hover:text-accent-foreground"
              >
                {transition.event}
              </button>
            ))}
            <button
              type="button"
              onClick={reset}
              className="rounded-pill border border-border-strong px-5 py-2.5 text-sm font-bold text-card-foreground hover:border-accent"
            >
              Reset
            </button>
          </div>
        </div>
      </div>

      <figcaption className="border-t border-border px-6 py-3 text-sm text-muted-foreground">
        Every arrow had to be drawn in advance. Nothing outside this diagram can happen.
      </figcaption>
    </figure>
  )
}

function MachineDiagram({
  currentId,
  highlighted,
  available,
  label,
}: {
  currentId: string
  highlighted: Transition | null
  available: Transition[]
  label: string
}) {
  const instance = useId()
  const arrow = `${instance}-arrow`
  const activeArrow = `${instance}-arrow-active`

  return (
    <svg
      viewBox={`${DIAGRAM_VIEWBOX.x} ${DIAGRAM_VIEWBOX.y} ${DIAGRAM_VIEWBOX.width} ${DIAGRAM_VIEWBOX.height}`}
      className="w-full bg-background"
      role="img"
      aria-label={label}
    >
      <defs>
        <ArrowHead id={arrow} fill="var(--color-ex-grey-400)" />
        <ArrowHead id={activeArrow} fill="var(--color-accent)" />
      </defs>

      <circle
        cx={ENTRY_MARKER.x}
        cy={ENTRY_MARKER.y}
        r={ENTRY_MARKER.radius}
        fill="var(--color-ex-grey-400)"
      />
      <line
        x1={ENTRY_MARKER.x + ENTRY_MARKER.radius}
        y1={ENTRY_MARKER.y}
        x2={ENTRY_MARKER.endX}
        y2={ENTRY_MARKER.y}
        stroke="var(--color-ex-grey-400)"
        strokeWidth={2}
        markerEnd={`url(#${arrow})`}
      />

      {greetingMachine.transitions.map((transition) => {
        const edge = edgeOf(transition.from, transition.to)
        const active =
          highlighted?.from === transition.from && highlighted?.to === transition.to
        const reachable = available.some((option) => option.event === transition.event)
        const faded = !active && !reachable

        return (
          <g key={transition.event} opacity={faded ? 0.4 : 1}>
            <path
              d={edge.path}
              fill="none"
              stroke={active ? 'var(--color-accent)' : 'var(--color-ex-grey-400)'}
              strokeWidth={active ? 4 : 2}
              markerEnd={`url(#${active ? activeArrow : arrow})`}
            />
            <text
              x={edge.labelX}
              y={edge.labelY}
              textAnchor={edge.labelAnchor}
              fontFamily="var(--font-mono)"
              fontSize={13}
              fontWeight={active ? 700 : 400}
              fill={active ? 'var(--color-foreground)' : 'var(--color-ex-grey-600)'}
            >
              {transition.event}
            </text>
          </g>
        )
      })}

      {DIAGRAM_NODES.map((node) => {
        const active = node.id === currentId

        return (
          <g key={node.id}>
            <rect
              x={node.x - node.width / 2}
              y={node.y - node.height / 2}
              width={node.width}
              height={node.height}
              rx={8}
              fill={active ? 'var(--color-accent)' : 'var(--color-card)'}
              fillOpacity={active ? 0.15 : 1}
              stroke={active ? 'var(--color-accent)' : 'var(--color-border-strong)'}
              strokeWidth={active ? 3 : 2}
            />
            <text
              x={node.x}
              y={node.y}
              textAnchor="middle"
              dominantBaseline="central"
              fontSize={16}
              fontWeight={700}
              fill={active ? 'var(--color-foreground)' : 'var(--color-muted-foreground)'}
            >
              {stateById(greetingMachine, node.id).label}
            </text>
          </g>
        )
      })}
    </svg>
  )
}

function ArrowHead({ id, fill }: { id: string; fill: string }) {
  return (
    <marker
      id={id}
      viewBox="0 0 10 10"
      refX={9}
      refY={5}
      markerWidth={6}
      markerHeight={6}
      orient="auto-start-reverse"
    >
      <path d="M 0 0 L 10 5 L 0 10 z" fill={fill} />
    </marker>
  )
}
