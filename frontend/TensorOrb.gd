extends Area2D

var dragging = false

func _input_event(_viewport, event, _shape_idx):
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_LEFT:
            dragging = event.pressed
            if not dragging:
                snap_and_simulate()

func _process(_delta):
    if dragging:
        global_position = get_global_mouse_position()

func snap_and_simulate():
    # Snap to grid logic here
    print("Snapped! Call backend sim")
    # Future: engine.append_to_build('add', ...); engine.build_and_simulate()