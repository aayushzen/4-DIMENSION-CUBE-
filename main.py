import pygame
import math
import sys

pygame.init()

WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tesseract")
clock = pygame.time.Clock()

# some platforms just give you their own screen size no matter what
# you pass to set_mode, so grab the real value back
WIDTH, HEIGHT = screen.get_size()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (80, 160, 255)
PURPLE = (190, 100, 255)
CYAN = (100, 230, 255)

CX, CY = WIDTH // 2, HEIGHT // 2
SCALE = 130

# 16 corners of a tesseract - each coord is -1 or 1
corners = []
for x in (-1, 1):
    for y in (-1, 1):
        for z in (-1, 1):
            for w in (-1, 1):
                corners.append((x, y, z, w))

# edge = two corners differing in exactly one coordinate
edges = []
for i in range(len(corners)):
    for j in range(i + 1, len(corners)):
        diff = sum(a != b for a, b in zip(corners[i], corners[j]))
        if diff == 1:
            edges.append((i, j))

angle_xw = 0.0
angle_yw = 0.0
angle_zw = 0.0
angle_xz = 0.0
angle_yz = 0.3

speed = 1.0
paused = False

dragging = False
moved_while_dragging = False
prev_mouse = (0, 0)


def rotate_point(x, y, z, w):
    c, s = math.cos(angle_xw), math.sin(angle_xw)
    x, w = x * c - w * s, x * s + w * c

    c, s = math.cos(angle_yw), math.sin(angle_yw)
    y, w = y * c - w * s, y * s + w * c

    c, s = math.cos(angle_zw), math.sin(angle_zw)
    z, w = z * c - w * s, z * s + w * c

    c, s = math.cos(angle_xz), math.sin(angle_xz)
    x, z = x * c - z * s, x * s + z * c

    c, s = math.cos(angle_yz), math.sin(angle_yz)
    y, z = y * c - z * s, y * s + z * c

    return x, y, z, w


def project(x, y, z, w):
    w_dist = 3.0
    wf = w_dist / (w_dist - w)
    x, y, z = x * wf, y * wf, z * wf

    z_dist = 4.0
    zf = z_dist / (z_dist - z)

    sx = CX + x * SCALE * zf
    sy = CY + y * SCALE * zf
    return sx, sy, w, z


def get_projected_points():
    pts = []
    for (x, y, z, w) in corners:
        rx, ry, rz, rw = rotate_point(x, y, z, w)
        pts.append(project(rx, ry, rz, rw))
    return pts


def draw_cube(pts):
    for i, j in edges:
        x1, y1, w1, z1 = pts[i]
        x2, y2, w2, z2 = pts[j]

        w_avg = (w1 + w2) / 2
        z_avg = (z1 + z2) / 2

        base_color = BLUE if w_avg >= 0 else PURPLE
        depth_fade = max(0.45, min(1.0, 1.0 - z_avg * 0.15))
        color = tuple(int(c * depth_fade) for c in base_color)

        thickness = 3 if abs(w_avg) < 0.5 else 2
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), thickness)

    for x, y, w, z in pts:
        color = WHITE if w >= 0 else CYAN
        radius = 5 if w >= 0 else 4
        pygame.draw.circle(screen, color, (int(x), int(y)), radius)


while True:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_LEFT:
                angle_xw -= 0.15
            elif event.key == pygame.K_RIGHT:
                angle_xw += 0.15
            elif event.key == pygame.K_UP:
                angle_yw += 0.15
            elif event.key == pygame.K_DOWN:
                angle_yw -= 0.15

        elif event.type == pygame.MOUSEBUTTONDOWN:
            dragging = True
            moved_while_dragging = False
            prev_mouse = event.pos

        elif event.type == pygame.MOUSEMOTION and dragging:
            dx = event.pos[0] - prev_mouse[0]
            dy = event.pos[1] - prev_mouse[1]
            if abs(dx) > 2 or abs(dy) > 2:
                moved_while_dragging = True
            angle_xw += dx * 0.005
            angle_yw += dy * 0.005
            prev_mouse = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
            if not moved_while_dragging:
                paused = not paused

    if not paused:
        angle_xw += 0.35 * speed * dt
        angle_yw += 0.22 * speed * dt
        angle_zw += 0.28 * speed * dt
        angle_xz += 0.15 * speed * dt
        angle_yz += 0.10 * speed * dt

    screen.fill(BLACK)
    points = get_projected_points()
    draw_cube(points)
    pygame.display.flip()
