import dearpygui.dearpygui as dpg
import math

# Create a callback function to update the speedometer needle
def update_speed(sender, app_data, user_data):
    # Update the needle angle based on the speed value (0-100)
    speed = app_data
    # Convert speed (0-100) to angle (-135° to 135°)
    angle = -225 + (speed * 2.7)
    radian_angle = math.radians(angle)
    
    # Calculate needle position based on angle
    x2 = 150 + 120 * math.cos(radian_angle)
    y2 = 150 + 120 * math.sin(radian_angle)
    # Update the needle's position
    dpg.configure_item("speedometer_needle", p2=(x2, y2))

# Create the speedometer interface
def create_speedometer():
    # Create a window
    with dpg.window(label="Speedometer Dashboard", width=400, height=500):
        # Draw the speedometer background (circle and ticks)
        with dpg.drawlist(width=300, height=300):
            # Draw the outer circle of the speedometer
            dpg.draw_circle(center=(150, 150), radius=140, color=(255, 255, 255, 255), thickness=2)
            
            # Draw speedometer ticks (every 10 units)
            for i in range(0, 11):
                angle = -225 + (i * 27)  # -135° to 135°
                radian_angle = math.radians(angle)
                x1 = 150 + 120 * math.cos(radian_angle)
                y1 = 150 + 120 * math.sin(radian_angle)
                x2 = 150 + 135 * math.cos(radian_angle)
                y2 = 150 + 135 * math.sin(radian_angle)
                dpg.draw_line(p1=(x1, y1), p2=(x2, y2), color=(255, 255, 255, 255), thickness=1)

            # Draw speedometer ticks (every 5 units)
            for i in range(0, 10):
                angle = -211.5 + (i * 27)  # -135° to 135°
                radian_angle = math.radians(angle)
                x1 = 150 + 130 * math.cos(radian_angle)
                y1 = 150 + 130 * math.sin(radian_angle)
                x2 = 150 + 135 * math.cos(radian_angle)
                y2 = 150 + 135 * math.sin(radian_angle)
                dpg.draw_line(p1=(x1, y1), p2=(x2, y2), color=(255, 255, 255, 255), thickness=1)
            
            # Draw the speedometer needle (initially at 0)
            dpg.draw_line(p1=(150, 150), p2=(65, 235), color=(255, 0, 0, 255), thickness=2, tag="speedometer_needle")

        # Add a slider to control speed value (0-100) inside the same window
        dpg.add_slider_int(label="Speed", min_value=0, max_value=100, default_value=0, callback=update_speed)

# Initialize Dear PyGui context
dpg.create_context()
create_speedometer()

# Create Dear PyGui view
dpg.create_viewport(title='Racecar Speedometer', width=400, height=500)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
