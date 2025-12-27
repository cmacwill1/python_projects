import math
import random
import pyglet
from pyglet.window import key
from pyglet.math import Mat4, Vec3
from pyglet.graphics.shader import Shader, ShaderProgram

# ---------------- Window ----------------
window = pyglet.window.Window(800, 600, "Orb Collector", resizable=True)
window.set_exclusive_mouse(True)

# Track keys manually
keys_pressed = {
    'W': False,
    'S': False,
    'A': False,
    'D': False
}

# ---------------- Game State ----------------
position = Vec3(0, 1.8, 0)
yaw = 0.0
pitch = 0.0
speed = 8.0
score = 0
game_time = 60.0

# ---------------- Shaders ----------------
VERT_SRC = """
#version 330 core
layout (location = 0) in vec3 position;
uniform mat4 MVP;
void main()
{
    gl_Position = MVP * vec4(position, 1.0);
}
"""

FRAG_SRC = """
#version 330 core
out vec4 FragColor;
uniform vec3 color;
void main()
{
    FragColor = vec4(color, 1.0);
}
"""

program = ShaderProgram(
    Shader(VERT_SRC, "vertex"),
    Shader(FRAG_SRC, "fragment")
)

# ---------------- Geometry ----------------
def create_cube():
    return [
        -0.5,-0.5, 0.5,  0.5,-0.5, 0.5,  0.5, 0.5, 0.5,
        -0.5,-0.5, 0.5,  0.5, 0.5, 0.5, -0.5, 0.5, 0.5,
        -0.5,-0.5,-0.5, -0.5, 0.5,-0.5,  0.5, 0.5,-0.5,
        -0.5,-0.5,-0.5,  0.5, 0.5,-0.5,  0.5,-0.5,-0.5,
        -0.5,-0.5,-0.5, -0.5,-0.5, 0.5, -0.5, 0.5, 0.5,
        -0.5,-0.5,-0.5, -0.5, 0.5, 0.5, -0.5, 0.5,-0.5,
         0.5,-0.5,-0.5,  0.5, 0.5,-0.5,  0.5, 0.5, 0.5,
         0.5,-0.5,-0.5,  0.5, 0.5, 0.5,  0.5,-0.5, 0.5,
        -0.5, 0.5,-0.5, -0.5, 0.5, 0.5,  0.5, 0.5, 0.5,
        -0.5, 0.5,-0.5,  0.5, 0.5, 0.5,  0.5, 0.5,-0.5,
        -0.5,-0.5,-0.5,  0.5,-0.5,-0.5,  0.5,-0.5, 0.5,
        -0.5,-0.5,-0.5,  0.5,-0.5, 0.5, -0.5,-0.5, 0.5,
    ]

cube_verts = create_cube()
cube_vl = program.vertex_list(len(cube_verts) // 3, pyglet.gl.GL_TRIANGLES, position=("f", cube_verts))

# Ground plane
ground_size = 50
ground_verts = [
    -ground_size, 0, -ground_size,
     ground_size, 0, -ground_size,
     ground_size, 0,  ground_size,
    -ground_size, 0, -ground_size,
     ground_size, 0,  ground_size,
    -ground_size, 0,  ground_size,
]
ground_vl = program.vertex_list(len(ground_verts) // 3, pyglet.gl.GL_TRIANGLES, position=("f", ground_verts))

# ---------------- Orbs ----------------
class Orb:
    def __init__(self):
        self.pos = Vec3(
            random.uniform(-15, 15),
            random.uniform(1, 3),
            random.uniform(-15, 15)
        )
        self.color = Vec3(
            random.uniform(0.6, 1.0),
            random.uniform(0.6, 1.0),
            random.uniform(0.2, 0.6)
        )
        self.collected = False
        self.bob_offset = random.uniform(0, math.pi * 2)
    
    def check_collection(self, player_pos):
        if self.collected:
            return False
        dx = self.pos.x - player_pos.x
        dy = self.pos.y - player_pos.y
        dz = self.pos.z - player_pos.z
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < 2.0:
            self.collected = True
            return True
        return False

orbs = [Orb() for _ in range(20)]

# ---------------- Input ----------------
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.W:
        keys_pressed['W'] = True
    elif symbol == key.S:
        keys_pressed['S'] = True
    elif symbol == key.A:
        keys_pressed['A'] = True
    elif symbol == key.D:
        keys_pressed['D'] = True
    elif symbol == key.ESCAPE:
        window.set_exclusive_mouse(False)
    elif symbol == key.R:
        reset_game()

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.W:
        keys_pressed['W'] = False
    elif symbol == key.S:
        keys_pressed['S'] = False
    elif symbol == key.A:
        keys_pressed['A'] = False
    elif symbol == key.D:
        keys_pressed['D'] = False

@window.event
def on_mouse_motion(x, y, dx, dy):
    global yaw, pitch
    yaw -= dx * 0.15  # Reversed from += to -=
    pitch -= dy * 0.15
    pitch = max(-89, min(89, pitch))

@window.event
def on_mouse_press(x, y, button, modifiers):
    window.set_exclusive_mouse(True)

# ---------------- Update ----------------
total_time = 0

def update(dt):
    global position, score, game_time, total_time
    
    game_time -= dt
    total_time += dt
    
    if game_time <= 0:
        return
    
    # Movement vectors (horizontal only, ignore pitch)
    forward_x = math.sin(math.radians(yaw))
    forward_z = -math.cos(math.radians(yaw))
    
    right_x = math.cos(math.radians(yaw))
    right_z = math.sin(math.radians(yaw))
    
    dx = 0.0
    dz = 0.0
    
    # Check which keys are pressed
    w_pressed = keys_pressed['W']
    s_pressed = keys_pressed['S']
    a_pressed = keys_pressed['A']
    d_pressed = keys_pressed['D']
    
    if w_pressed:
        dx += forward_x
        dz += forward_z
    if s_pressed:
        dx -= forward_x
        dz -= forward_z
    if a_pressed:
        dx += right_x  # Changed from -= to +=
        dz += right_z  # Changed from -= to +=
    if d_pressed:
        dx -= right_x  # Changed from += to -=
        dz -= right_z  # Changed from += to -=
    
    # Normalize diagonal movement
    if dx != 0 or dz != 0:
        length = math.sqrt(dx*dx + dz*dz)
        dx /= length
        dz /= length
        
        position = Vec3(
            position.x + dx * speed * dt,
            position.y,
            position.z + dz * speed * dt
        )
    
    # Update debug info
    debug_label.text = f"Pos: ({position.x:.1f}, {position.y:.1f}, {position.z:.1f}) | Keys: W={w_pressed} S={s_pressed} A={a_pressed} D={d_pressed}"
    
    # Check orb collection
    for orb in orbs:
        if orb.check_collection(position):
            score += 10

def reset_game():
    global position, score, game_time, orbs, yaw, pitch, total_time, keys_pressed
    position = Vec3(0, 1.8, 0)
    yaw = 0.0
    pitch = 0.0
    score = 0
    game_time = 60.0
    total_time = 0
    orbs = [Orb() for _ in range(20)]
    keys_pressed = {'W': False, 'S': False, 'A': False, 'D': False}

# ---------------- Render ----------------
label = pyglet.text.Label('', font_size=18, x=10, y=window.height - 30,
                          color=(255, 255, 255, 255))
help_label = pyglet.text.Label('WASD to move | Mouse to look | R to restart',
                               font_size=14, x=10, y=window.height - 55,
                               color=(200, 200, 200, 255))
debug_label = pyglet.text.Label('', font_size=12, x=10, y=50,
                                color=(255, 255, 0, 255))

@window.event
def on_draw():
    pyglet.gl.glEnable(pyglet.gl.GL_DEPTH_TEST)
    pyglet.gl.glClearColor(0.4, 0.6, 0.9, 1.0)
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
    
    # Use standard perspective projection
    proj = Mat4.perspective_projection(
        window.width / window.height,
        z_near=0.1,
        z_far=100.0,
        fov=70
    )
    
    # Camera position behind and above the player at FIXED distance
    camera_distance = 6.0
    
    # Clamp pitch for reasonable camera angles
    clamped_pitch = max(-30, min(60, pitch))
    
    # Calculate camera position with both yaw and pitch
    # Horizontal distance decreases as we look down/up
    horizontal_distance = camera_distance * math.cos(math.radians(clamped_pitch))
    camera_height = camera_distance * math.sin(math.radians(clamped_pitch))
    
    camera_offset = Vec3(
        -math.sin(math.radians(yaw)) * horizontal_distance,
        camera_height + 1.8,  # Add player height offset
        math.cos(math.radians(yaw)) * horizontal_distance
    )
    camera_pos = position + camera_offset
    
    # Create a look-at view matrix that always points at the player
    # Direction from camera to player
    forward = (position - camera_pos).normalize()
    # Right vector
    right = Vec3(0, 1, 0).cross(forward).normalize()
    # Up vector
    up = forward.cross(right)
    
    # Build look-at matrix manually
    view = Mat4((
        right.x, up.x, -forward.x, 0,
        right.y, up.y, -forward.y, 0,
        right.z, up.z, -forward.z, 0,
        -right.dot(camera_pos), -up.dot(camera_pos), forward.dot(camera_pos), 1
    ))
    
    program.use()
    
    # Draw ground
    program["color"] = Vec3(0.2, 0.6, 0.3)
    program["MVP"] = proj @ view @ Mat4()
    ground_vl.draw(pyglet.gl.GL_TRIANGLES)
    
    # Draw orbs with bobbing animation
    for orb in orbs:
        if not orb.collected:
            bob = math.sin(total_time * 3 + orb.bob_offset) * 0.3
            model = Mat4.from_translation(Vec3(orb.pos.x, orb.pos.y + bob, orb.pos.z))
            model = model.scale(Vec3(0.7, 0.7, 0.7))
            # Make orbs glow/pulse
            glow = 0.8 + 0.2 * math.sin(total_time * 4 + orb.bob_offset)
            program["color"] = Vec3(orb.color.x * glow, orb.color.y * glow, orb.color.z * glow)
            program["MVP"] = proj @ view @ model
            cube_vl.draw(pyglet.gl.GL_TRIANGLES)
    
    # Draw THE PLAYER (red cube at player position, rotated to match camera yaw)
    player_model = Mat4.from_translation(position)
    player_model = player_model.rotate(math.radians(-yaw), Vec3(0, 1, 0))  # Negative yaw to match camera
    player_model = player_model.scale(Vec3(0.5, 0.5, 0.5))
    program["color"] = Vec3(1.0, 0.2, 0.2)
    program["MVP"] = proj @ view @ player_model
    cube_vl.draw(pyglet.gl.GL_TRIANGLES)
    
    # Draw UI
    pyglet.gl.glDisable(pyglet.gl.GL_DEPTH_TEST)
    
    if game_time > 0:
        remaining = sum(1 for o in orbs if not o.collected)
        label.text = f"Score: {score} | Time: {int(game_time)}s | Orbs Left: {remaining}"
        label.y = window.height - 30
        help_label.y = window.height - 55
    else:
        label.text = f"GAME OVER! Final Score: {score} | Press R to restart"
        label.y = window.height - 30
        help_label.text = ""
    
    label.draw()
    help_label.draw()
    debug_label.draw()

@window.event
def on_resize(width, height):
    label.y = height - 30
    help_label.y = height - 55

# ---------------- Main ----------------
pyglet.clock.schedule(update)
pyglet.app.run()
