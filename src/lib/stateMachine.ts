export type StateNode = {
  id: string
  label: string
  description: string
}

export type Transition = {
  from: string
  to: string
  event: string
}

export type StateMachine = {
  initial: string
  states: StateNode[]
  transitions: Transition[]
}

export function transitionsFrom(machine: StateMachine, stateId: string): Transition[] {
  return machine.transitions.filter((transition) => transition.from === stateId)
}

export function stateById(machine: StateMachine, stateId: string): StateNode {
  const state = machine.states.find((candidate) => candidate.id === stateId)
  if (!state) throw new Error(`Unknown state: ${stateId}`)
  return state
}
