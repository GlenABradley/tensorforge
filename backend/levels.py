# backend/levels.py
from engine import TensorForgeEngine

class LevelsManager:
    def __init__(self, engine):
        self.engine = engine
        self.levels = {}

    def define_level(self, level_id, inputs, target, components):
        self.levels[level_id] = {
            'inputs': inputs,
            'target': target,
            'components': components
        }
        for comp, func in components.items():
            self.engine.add_component(comp, func)

    def load_level(self, level_id):
        level = self.levels.get(level_id)
        if level:
            self.engine.level_data = level
            return True
        return False

# Example: Define Level 1
if __name__ == "__main__":
    engine = TensorForgeEngine()
    manager = LevelsManager(engine)
    manager.define_level(
        1,
        torch.tensor([1.0]),
        torch.tensor([2.0]),
        {'add_one': lambda x: torch.add(x, torch.tensor(1.0))}
    )
    manager.load_level(1)
    # Test build
    engine.append_to_build('add_one')
    result = engine.build_and_simulate(engine.level_data['inputs'])
    print("Level 1 Win:" if engine.check_win(result, engine.level_data['target']) else "Fail")