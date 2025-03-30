from rock.states.basic_state import BasicState

class Compleated(BasicState):
    def __init__(self, context, cooldown=0) -> None:
        super().__init__(context, cooldown)
        self.activated = False
    
    def interact(self, player):
        self.context.show_outline()
        self.context.board.show(f'kills: {self.context.resorce}')
        if player.using_e: self.activated = True
    
    def _enter(self):
        self.activated = False
        
    def next_state(self):
        if not self.activated: return

        if self.context.stage == 6:
            self.context.game.new_map('lobby')

        elif self.context.stage == 5:
            self.context.game.next_stage()
            self.context.game.new_map('map3')

        else:
            self.context.game.next_stage()
            self.context.game.new_map('map2')
        
        self.activated = False