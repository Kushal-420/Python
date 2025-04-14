import pygame
import time

# Constants
AXIS_THRESHOLD = 0.5
DELAY = 0.1

# Initialize pygame and joystick
pygame.init()
pygame.joystick.init()

def init_controller():
    if pygame.joystick.get_count() == 0:
        print("No joystick connected.")
        return None
    controller = pygame.joystick.Joystick(0)
    controller.init()
    print(f"Controller initialized: {controller.get_name()}")
    return controller

def get_input_state(controller):
    pygame.event.pump()  # Updates internal input state

    state = {
        "left_x": controller.get_axis(0),
        "left_y": controller.get_axis(1),
        "right_x": controller.get_axis(3),
        "right_y": controller.get_axis(4),
        "buttons": {
            "A": controller.get_button(0),
            "B": controller.get_button(1),
            "X": controller.get_button(2),
            "Y": controller.get_button(3),
        }
    }
    return state

def interpret_input(state):
    x, y = state["left_x"], state["left_y"]

    if y < -AXIS_THRESHOLD:
        return "Forward"
    elif y > AXIS_THRESHOLD:
        return "Backward"
    elif x < -AXIS_THRESHOLD:
        return "Left"
    elif x > AXIS_THRESHOLD:
        return "Right"
    
    for btn, pressed in state["buttons"].items():
        if pressed:
            return f"{btn} Button Pressed"

    return "Neutral"

def main():
    controller = init_controller()
    if controller is None:
        return

    last_state = ""
    try:
        while True:
            state = get_input_state(controller)
            action = interpret_input(state)
            if action != last_state:
                print(action)
                last_state = action
            time.sleep(DELAY)
    except KeyboardInterrupt:
        print("\nController reading stopped.")
    finally:
        pygame.joystick.quit()
        pygame.quit()

if __name__ == "__main__":
    main()
