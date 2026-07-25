import type { StateMachine } from './stateMachine'

export const greetingMachine: StateMachine = {
  initial: 'idle',
  states: [
    { id: 'idle', label: 'Idle', description: 'The robot stands still and waits for a start signal.' },
    { id: 'patrolling', label: 'Patrolling', description: 'The robot walks a fixed route and keeps scanning.' },
    { id: 'personDetected', label: 'Person detected', description: 'The camera reported a person. Walking stops.' },
    { id: 'waving', label: 'Waving', description: 'The arm plays back a recorded waving motion.' },
  ],
  transitions: [
    { from: 'idle', to: 'patrolling', event: 'start' },
    { from: 'patrolling', to: 'personDetected', event: 'person in view' },
    { from: 'patrolling', to: 'idle', event: 'stop' },
    { from: 'personDetected', to: 'waving', event: 'person is close enough' },
    { from: 'personDetected', to: 'patrolling', event: 'person left' },
    { from: 'waving', to: 'patrolling', event: 'wave finished' },
  ],
}
