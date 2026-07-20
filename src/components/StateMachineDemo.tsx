import { useState } from 'react'
import { greetingMachine } from '@/lib/greetingMachine'
import { stateById, transitionsFrom, type StateNode, type Transition } from '@/lib/stateMachine'

export default function StateMachineDemo() {
  const [currentId, setCurrentId] = useState(greetingMachine.initial)
  const current = stateById(greetingMachine, currentId)
  const options = transitionsFrom(greetingMachine, currentId)

  return (
    <figure className="not-prose my-10 overflow-hidden rounded-2xl border border-border-subtle bg-surface">
      <div className="grid gap-6 p-6 md:grid-cols-[1fr_1fr]">
        <ol className="flex flex-col gap-3">
          {greetingMachine.states.map((state) => (
            <StateRow key={state.id} state={state} isActive={state.id === currentId} />
          ))}
        </ol>
        <div className="flex flex-col gap-4">
          <p className="text-ink-muted">{current.description}</p>
          <p className="text-xs font-semibold tracking-[0.2em] text-ink-muted uppercase">
            Possible events right now
          </p>
          <div className="flex flex-col gap-2">
            {options.map((transition) => (
              <EventButton
                key={transition.event}
                transition={transition}
                onFire={() => setCurrentId(transition.to)}
              />
            ))}
          </div>
          <button
            type="button"
            onClick={() => setCurrentId(greetingMachine.initial)}
            className="self-start rounded-lg border border-border-subtle px-4 py-2 text-sm text-ink-muted hover:border-accent hover:text-accent"
          >
            Reset
          </button>
        </div>
      </div>
      <figcaption className="border-t border-border-subtle px-6 py-3 text-sm text-ink-muted">
        Every reaction has to be written down in advance. Nothing outside this diagram can happen.
      </figcaption>
    </figure>
  )
}

function StateRow({ state, isActive }: { state: StateNode; isActive: boolean }) {
  return (
    <li
      aria-current={isActive ? 'step' : undefined}
      className={
        isActive
          ? 'rounded-xl border-2 border-accent bg-canvas px-4 py-3 font-semibold text-accent'
          : 'rounded-xl border-2 border-border-subtle px-4 py-3 text-ink-muted'
      }
    >
      {state.label}
    </li>
  )
}

function EventButton({ transition, onFire }: { transition: Transition; onFire: () => void }) {
  return (
    <button
      type="button"
      onClick={onFire}
      className="rounded-lg bg-accent px-4 py-2.5 text-left font-medium text-accent-ink hover:brightness-110"
    >
      {transition.event} →
    </button>
  )
}
