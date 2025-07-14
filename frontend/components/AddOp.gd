# frontend/components/AddOp.gd
extends "res://frontend/TensorOrb.gd"  # Assume base drag script

var op_name = "add"
var arg_value = 1.0  # For add_one example

func snap_and_simulate():
    .snap_and_simulate()  # Call base
    # Future backend call: engine.append_to_build(op_name, torch.tensor(arg_value))
    print("Added 'add' op with value:", arg_value)