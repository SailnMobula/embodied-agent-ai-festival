import { useState } from 'react'
import { greetingMachine } from '@/lib/greetingMachine'
import { stateById, transitionsFrom, type StateNode, type Transition } from '@/lib/stateMachine'

export default function StateMachineDemo() {
  const [currentId, setCurrentId] = useState(greetingMachine.initial)
  const current = stateById(greetingMachine, currentId)
  const options = transitionsFrom(greetingMachine, currentId)

  return (
    <figure className="my-10 overflow-hidden rounded-card border border-border bg-card">
      <div className="grid gap-6 p-6 md:grid-cols-2">
        <ol className="flex flex-col gap-3">
          {greetingMachine.states.map((state) => (
            <StateRow key={state.id} state={state} isActive={state.id === currentId} />
          ))}
        </ol>
        <div className="flex flex-col gap-4">
          <p className="text-muted-foreground">{current.description}</p>
          <p className="text-sm font-bold text-card-foreground">Possible events right now</p>
          <div className="flex flex-col items-start gap-2">
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
            className="self-start rounded-pill border border-border-strong px-5 py-2 text-sm font-bold text-card-foreground hover:border-accent"
          >
            Reset
          </button>
        </div>
      </div>
      <figcaption className="border-t border-border px-6 py-3 text-sm text-muted-foreground">
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
          ? 'rounded-container border-2 border-accent bg-accent/15 px-4 py-3 font-bold text-foreground'
          : 'rounded-container border-2 border-border px-4 py-3 text-muted-foreground'
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
      className="rounded-pill bg-foreground px-5 py-2.5 text-left font-bold text-background hover:bg-accent hover:text-accent-foreground"
    >
      {transition.event} →
    </button>
  )
}
