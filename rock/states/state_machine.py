import pygame
from rock.states.basic_state import BasicState
from rock.states.Inactive import Inactive
from rock.states.wave import Wave
from rock.states.brake import Brake
from rock.states.final_wave import FinalWave
from rock.states.compleated import Compleated
from rock.states.boss_fight import BossFight


class StateMachine:
    def __init__(self, context, game, stage) -> None:
        if stage == 0: self.state = 'inactive'
        elif stage == 6: self.state = 'boss_fight'
        else: self.state = 'brake'
        
        self.states = {
            'inactive': Inactive(context),
            'wave': Wave(context, game),
            'brake': Brake(context),
            'final_wave': FinalWave(context, game),
            'compleated': Compleated(context),
            'boss_fight': BossFight(context, game)
        }
        self.current_state: BasicState = self.states[self.state]
        self.current_state._enter()
    
    def interact(self, player): self.current_state.interact(player)
    
    def change_state(self, state: str):
        if not state: return
        if not self.states[state].cooldown(): return
        self.current_state._exsit()
        self.current_state = self.states[state]
        self.current_state._enter()
        self.state = state
    
    def update(self, dt, *args):
        self.current_state.update(dt, *args)
        for state in self.states.values(): state.cooldown.timer()
        if state := self.current_state.next_state(): self.change_state(state)
