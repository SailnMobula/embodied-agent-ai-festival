import type { StateMachine } from './stateMachine'

export const greetingMachine: StateMachine = {
  initial: 'idle',
  states: [
    { id: 'idle', label: 'Idle', description: 'The robot stands still and waits for a start signal.' },
    { id: 'watching', label: 'Watching', description: 'The robot holds its place and scans the room.' },
    { id: 'personDetected', label: 'Person detected', description: 'The camera reported a person. Scanning stops.' },
    { id: 'waving', label: 'Waving', description: 'The arm plays back a recorded waving motion.' },
  ],
  transitions: [
    { from: 'idle', to: 'watching', event: 'start' },
    { from: 'watching', to: 'personDetected', event: 'person in view' },
    { from: 'watching', to: 'idle', event: 'stop' },
    { from: 'personDetected', to: 'waving', event: 'person is close enough' },
    { from: 'personDetected', to: 'watching', event: 'person left' },
    { from: 'waving', to: 'watching', event: 'wave finished' },
  ],
}
