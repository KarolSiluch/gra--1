from rock.states.basic_state import BasicState

class Inactive(BasicState):
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
        if self.activated:
            self.context.game.next_stage()
            self.context.game.new_map('map2')
            self.activated = False