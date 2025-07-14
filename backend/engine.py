import torch
import torch.nn as nn

class TensorForgeEngine:
    def __init__(self):
        self.components = {}
        self.player_build = []
        self.level_data = {}

    def add_component(self, op_name, op_func):
        self.components[op_name] = op_func

    def append_to_build(self, op_name, *args):
        def op_func(x):
            return self.components[op_name](x, *args)
        self.player_build.append(op_func)

    def build_and_simulate(self, inputs):
        result = inputs
        for op in self.player_build:
            result = op(result)
        return result

    def check_win(self, result, target):
        loss = nn.MSELoss()(result, target)
        return loss < 1e-3  # Simple threshold

    def load_level(self, level_id):
        if level_id == 1:
            self.level_data = {
                'inputs': torch.tensor([1.0]),
                'target': torch.tensor([2.0]),
                'available_components': ['add']
            }
            self.add_component('add', torch.add)

# Example usage (for testing)
if __name__ == "__main__":
    engine = TensorForgeEngine()
    engine.load_level(1)
    engine.append_to_build('add', torch.tensor([1.0]))
    result = engine.build_and_simulate(engine.level_data['inputs'])
    print("Win?" if engine.check_win(result, engine.level_data['target']) else "Fail")