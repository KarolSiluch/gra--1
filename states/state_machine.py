import pygame
from states.basic_state import BasicState
from states.player_run import PlayerRunState
from states.player_idle import PlayerIdleState
from states.player_dodge import PlayerDodgeState
from states.contact_damage import ContactDamage

class StateMachine:
    def __init__(self, context) -> None:
        self.state = 'idle'
        self.states = {
            'idle': PlayerIdleState(context, {'run', 'contact_damage'}),
            'run': PlayerRunState(context, {'idle', 'dodge', 'contact_damage'}),
            'dodge': PlayerDodgeState(context, {'run', 'idle'}, cooldown=300),
            'contact_damage': ContactDamage(context, {'run', 'idle'}, cooldown=300)
        }
        self.current_state: BasicState = self.states[self.state]
    
    def change_state(self, state: str):
        if not state: return
        if not state in self.current_state.possible_next_states: return
        if not self.states[state].cooldown(): return
        self.current_state._exsit()
        self.current_state = self.states[state]
        self.current_state._enter()
        self.state = state
    
    def update(self, dt, events, *args):
        self.current_state.update(dt, *args)
        for state in self.states.values(): state.cooldown.timer()
        self.change_state(self.current_state.next_state(events))
        # if state := self.current_state.next_state(): self.change_state(state)


