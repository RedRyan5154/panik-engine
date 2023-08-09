import pygame
import time
import math
import copy
import numpy as np


class Element:
    def __init__(self, texture, x, y, scale=100, flip=(0, 0)):
        """
        A base class for all game objects
        """
        self.original_texture = texture.image

        self.x, self.y = x, y
        self.w = scale * self.original_texture.get_width() / 100
        self.h = scale * self.original_texture.get_height() / 100
        self.scale = scale
        self.rotation = 0
        self.flip = flip

        self.type = "element"
        self.parent = None
        self.show = True
        self.is_hud = False

        # Create the scaled and flipped texture
        self.texture = pygame.transform.flip(
            pygame.transform.scale(
                self.original_texture,
                (self.w, self.h),
            ),
            self.flip[0],
            self.flip[1],
        )

    def scale_image(self, scale):
        """
        Scale the image to a given percentage
        """
        self.scale = scale
        self.w = scale * self.original_texture.get_width() / 100
        self.h = scale * self.original_texture.get_height() / 100

        self.texture = pygame.transform.scale(self.original_texture, (self.w, self.h))
        flip = self.flip
        self.flip = (0, 0)
        self.flip_image(flip)

    def flip_image(self, flip=(False, False)):
        """
        Flip the image horizontally or vertically
        """
        fx, fy = False, False
        if flip[0]:
            if not self.flip[0]:
                fx = True
        else:
            if self.flip[0]:
                fx = True
        if flip[1]:
            if not self.flip[1]:
                fy = True
        else:
            if self.flip[1]:
                fy = True

        self.flip = flip

        self.texture = pygame.transform.flip(self.texture, fx, fy)

    def set_image(self, image):
        """
        Set a new image for the element
        """
        self.original_texture = image.image
        self.scale_image(self.scale)


class CollisionRect:
    def __init__(self, x, y, width, height):
        self.type = "collisionrect"

        self._rotation = 0
        self._x, self._y = x, y
        self._width, self._height = width, height

        self.color = (255, 0, 0)
        self.parent = None
        self.is_hud = False

        self.show = False

        self.update_vertexes()

        self.x, self.y = x, y

    def __repr__(self) -> str:
        return f"Collision Rect ({self.def_vertex})({self.rotation})"

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation
        if self._rotation > 360:
            self._rotation -= 360
        elif self._rotation < 0:
            self._rotation += 360
        self.update_vertexes()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x
        self.update_vertexes()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y
        self.update_vertexes()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width
        self.update_vertexes()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height
        self.update_vertexes()

    def update_vertexes(self):
        self.vertexes = [
            pygame.math.Vector2(
                self._x,
                self._y,
            ),
            pygame.math.Vector2(
                self._x + self._width,
                self._y,
            ),
            pygame.math.Vector2(
                self._x + self._width,
                self._y + self._height,
            ),
            pygame.math.Vector2(
                self._x,
                self._y + self._height,
            ),
        ]

        self.centroid = sum(self.vertexes, pygame.math.Vector2()) / len(self.vertexes)

        pivot_subtracted = [v - self.centroid for v in self.vertexes]
        rotated = [sub.rotate(-self._rotation) for sub in pivot_subtracted]
        self.def_vertex = [rot + self.centroid for rot in rotated]

    def check_collision(self, collisions, get_pv=False):
        def centers_displacement(p1, p2):
            """
            Return the displacement between the geometric center of p1 and p2.
            """
            # geometric center
            c1 = np.mean(np.array(p1), axis=0)
            c2 = np.mean(np.array(p2), axis=0)
            return c2 - c1

        def edges_of(vertices):
            """
            Return the vectors for the edges of the polygon p.

            p is a polygon.
            """
            edges = []
            N = len(vertices)

            for i in range(N):
                edge = vertices[(i + 1) % N] - vertices[i]
                edges.append(edge)

            return edges

        def orthogonal(v):
            """
            Return a 90 degree clockwise rotation of the vector v.
            """
            return np.array([-v[1], v[0]])

        def is_separating_axis(o, p1, p2):
            """
            Return True and the push vector if o is a separating axis of p1 and p2.
            Otherwise, return False and None.
            """

            min1, max1 = float("+inf"), float("-inf")
            min2, max2 = float("+inf"), float("-inf")

            for v in p1:
                projection = np.dot(v, o)

                min1 = min(min1, projection)
                max1 = max(max1, projection)

            for v in p2:
                projection = np.dot(v, o)

                min2 = min(min2, projection)
                max2 = max(max2, projection)

            if max1 >= min2 and max2 >= min1:
                if get_pv:
                    d = min(max2 - min1, max1 - min2)
                    # push a bit more than needed so the shapes do not overlap in future
                    # tests due to float precision
                    d_over_o_squared = d / np.dot(o, o) + 1e-10
                    pv = d_over_o_squared * o
                    return False, pv
                else:
                    return False, None
            else:
                return True, None

        if not type(collisions) == list:
            if type(collisions) == dict:
                collisions = list(collisions.values())
            else:
                collisions = [collisions]

        result = False
        collisions_idx = []
        mpv_res = []

        p1 = [np.array(v, "float64") for v in self.def_vertex]
        p1edges = edges_of(p1)

        for i, collision in enumerate(collisions):
            # print(self.vertexes, collision.vertexes)
            p2 = [np.array(v, "float64") for v in collision.def_vertex]

            edges = p1edges + edges_of(p2)
            orthogonals = [orthogonal(e) for e in edges]

            push_vectors = []
            for o in orthogonals:
                separates, pv = is_separating_axis(o, p1, p2)

                if separates:
                    # they do not collide and there is no push vector
                    break
                else:
                    if get_pv:
                        push_vectors.append(pv)
            else:
                if get_pv:
                    # they do collide and the push_vector with the smallest length is the MPV
                    mpv = min(push_vectors, key=(lambda v: np.dot(v, v)))

                    # assert mpv pushes p1 away from p2
                    d = centers_displacement(p1, p2)  # direction from p1 to p2
                    if np.dot(d, mpv) > 0:  # if it's the same direction, then invert
                        mpv = -mpv
                    mpv_res.append(mpv)
                else:
                    mpv_res = None

                result = True
                collisions_idx.append(i)
        return (result, mpv_res, collisions_idx)

    def check_collision(self, collisions, get_pv=False):
        def centers_displacement(p1, p2):
            """
            Return the displacement between the geometric center of p1 and p2.
            """
            # geometric center
            c1 = np.mean(np.array(p1), axis=0)
            c2 = np.mean(np.array(p2), axis=0)
            return c2 - c1

        def edges_of(vertices):
            """
            Return the vectors for the edges of the polygon p.

            p is a polygon.
            """
            edges = []
            N = len(vertices)

            for i in range(N):
                edge = vertices[(i + 1) % N] - vertices[i]
                edges.append(edge)

            return edges

        def orthogonal(v):
            """
            Return a 90 degree clockwise rotation of the vector v.
            """
            return np.array([-v[1], v[0]])

        def is_separating_axis(o, p1, p2):
            """
            Return True and the push vector if o is a separating axis of p1 and p2.
            Otherwise, return False and None.
            """

            min1, max1 = float("+inf"), float("-inf")
            min2, max2 = float("+inf"), float("-inf")

            for v in p1:
                projection = np.dot(v, o)

                min1 = min(min1, projection)
                max1 = max(max1, projection)

            for v in p2:
                projection = np.dot(v, o)

                min2 = min(min2, projection)
                max2 = max(max2, projection)

            if max1 >= min2 and max2 >= min1:
                if get_pv:
                    d = min(max2 - min1, max1 - min2)
                    # push a bit more than needed so the shapes do not overlap in future
                    # tests due to float precision
                    d_over_o_squared = d / np.dot(o, o) + 1e-10
                    pv = d_over_o_squared * o
                    return False, pv
                else:
                    return False, None
            else:
                return True, None

        if not type(collisions) == list:
            if type(collisions) == dict:
                collisions = list(collisions.values())
            else:
                collisions = [collisions]

        result = False
        collisions_idx = []
        mpv_res = []

        p1 = [np.array(v, "float64") for v in self.def_vertex]
        p1edges = edges_of(p1)

        for i, collision in enumerate(collisions):
            # print(self.vertexes, collision.vertexes)
            p2 = [np.array(v, "float64") for v in collision.def_vertex]

            edges = p1edges + edges_of(p2)
            orthogonals = [orthogonal(e) for e in edges]

            push_vectors = []
            for o in orthogonals:
                separates, pv = is_separating_axis(o, p1, p2)

                if separates:
                    # they do not collide and there is no push vector
                    break
                else:
                    if get_pv:
                        push_vectors.append(pv)
            else:
                if get_pv:
                    # they do collide and the push_vector with the smallest length is the MPV
                    mpv = min(push_vectors, key=(lambda v: np.dot(v, v)))

                    # assert mpv pushes p1 away from p2
                    d = centers_displacement(p1, p2)  # direction from p1 to p2
                    if np.dot(d, mpv) > 0:  # if it's the same direction, then invert
                        mpv = -mpv
                    mpv_res.append(mpv)
                else:
                    mpv_res = None

                result = True
                collisions_idx.append(i)
        return (result, mpv_res, collisions_idx)


class Sprite(Element):
    def __init__(self, texture, x, y, scale=100, flip=(0, 0)):
        """
        A game object with animations and collisions
        """
        super().__init__(texture, x, y, scale, flip)

        self.type = "sprite"

        self.collision = None
        self.parent = None
        self.center = (0, 0)

        self.animationidx = 0
        self.starttime = time.time()
        self.prevanimation = None
        self.finished_anim = False

    def animate(self, animation, delay=0.1, loop=True):
        """
        Animate the sprite using a sequence of images

        Args:
            - animation: An Animation object that holds a sequence of images
            - delay: Delay between frame changes in seconds

        Returns true if finished
        """
        if self.prevanimation != animation:
            self.animationidx = 0
            self.prevanimation = animation
            self.starttime = time.time() - delay
            self.finished_anim = False
        if time.time() - self.starttime > delay:
            self.starttime = time.time()
            if self.animationidx >= len(animation.animations) - 1:
                if loop:
                    self.animationidx = 0
                else:
                    self.finished_anim = True
            else:
                self.animationidx += 1
            self.original_texture = list(animation.animations.values())[
                self.animationidx
            ]
            self.size_x, self.size_y = (
                self.scale * self.original_texture.get_width() / 100,
                self.scale * self.original_texture.get_height() / 100,
            )
            self.scale_image(self.scale)

    def move_x(self, x, collision=None):
        """
        Move or attempt to move the sprite horizontally (along the x-axis)

        Args:
            - x: The amount to move (positive for right, negative for left)
            - collision: The collision object to check against (optional)
            - multiplier: Multiplier to adjust the collision check distance

        Multiplier prevents the sprite from getting stuck to a collision. The higher the multiplier, the slower the sprite
        will move when colliding, but the wider the distance it can cover at higher speeds.
        """
        if collision:
            # Move while checking for collisions
            self.x += x
            self.collision.x += x
            if self.collision.check_collision(collision)[0]:
                self.x -= x
                self.collision.x -= x
        else:
            self.x += x
            self.collision.x += x

    def move_y(self, y, collision=None):
        """
        Move or attempt to move the sprite vertically (along the y-axis)

        Args:
            - y: The amount to move (positive for down, negative for up)
            - collision: The collision object to check against (optional)
            - multiplier: Multiplier to adjust the collision check distance

        Multiplier prevents the sprite from getting stuck to a collision. The higher the multiplier, the slower the sprite
        will move when colliding, but the wider the distance it can cover at higher speeds.
        """
        if collision:
            # Move while checking for collisions
            self.y += y
            self.collision.y += y
            if self.collision.check_collision(collision)[0]:
                self.y -= y
                self.collision.y -= y
        else:
            self.y += y
            self.collision.y += y

    def move_towards(self, x, y, pixels, collision=None):
        """
        Move the sprite towards a target point (x, y) by a specified number of pixels

        Args:
            - x, y: The target point coordinates
            - pixels: The number of pixels to move towards the target
            - collision: Thecollision object to check against (optional)
        - multiplier: Multiplier to adjust the collision check distance

        Returns:
            - mx, my: The actual movement in the x and y directions
            - direction: The direction in degrees from the sprite's current position to the target point
        """
        direction = -math.atan2(y - self.y, x - self.x)
        mx = math.cos(-direction) * pixels
        my = math.sin(-direction) * pixels
        self.move_x(mx, collision)
        self.move_y(my, collision)
        return mx, my, math.degrees(direction)

    def move_in_direction(self, direction, pixels, collisions=None):
        """
        Move the sprite in a specific direction by a specified number of pixels

        Args:
            - direction: The direction in degrees (0 is right, 90 is down, 180 is left, 270 is up)
            - pixels: The number of pixels to move in the specified direction
            - collisions: The collision object(s) to check against (optional)
            - multiplier: Multiplier to adjust the collision check distance

        Returns:
            - mx, my: The actual movement in the x and y directions
            - direction: The direction in degrees (same as the input direction)
        """
        direction = math.radians(direction)
        mx = math.cos(-direction) * pixels
        my = math.sin(-direction) * pixels
        self.move_x(mx, collisions)
        self.move_y(my, collisions)
        return mx, my, math.degrees(direction)

    def point_towards(self, x, y):
        """
        Rotate the sprite to point towards a target point (x, y)

        Args:
            - x, y: The target point coordinates

        Returns:
            - The new rotation angle in degrees
        """
        self.rotation = math.degrees(
            -math.atan2(
                y - self.y - (self.parent.y if self.parent else 0),
                x - self.x - (self.parent.x if self.parent else 0),
            )
        )
        if self.rotation < 0:
            self.rotation += 360

        return self.rotation

    def add_collision(self, collision):
        collision.parent = self
        self.collision = collision
        self.cx, self.cy = self.collision.x, self.collision.y
        self.cw, self.ch = self.collision.width, self.collision.height


class TileMap:
    def __init__(self, tile_list, tile_size, tileset, scale, x, y, parent=None) -> None:
        ## meta
        self.type = "tilemap"
        self.x = x
        self.y = y
        self.scale = scale
        self.assets = tileset.load()
        self.tile_size = tile_size * scale / 100
        if not str(self.tile_size).endswith(".0"):
            self.tile_size = round(self.tile_size) - 1

        ## store tile map
        f = open(tile_list, "r")
        data = f.read()
        f.close()
        data = data.split("\n")

        if data[len(data) - 1] == "":
            del data[len(data) - 1]

        self.show = True
        self.width = len(data[0]) * self.tile_size
        self.height = len(data) * self.tile_size

        ## look-up table
        self.tiles_lookup = {}

        ## tile table
        self.tiles = []

        # resize and prepare tiles
        for key, tile in self.assets.items():
            self.tiles_lookup[key] = pygame.transform.scale(
                tile,
                (
                    scale * tile.get_width() / 100,
                    scale * tile.get_height() / 100,
                ),
            )

        for y, row in enumerate(data):
            _tmprow = []
            for x, tile in enumerate(row.split(",")):
                if tile == "-1":
                    _tmprow.append(None)
                    continue
                _tmprow.append(tile)
            self.tiles.append(_tmprow)


class CollisionTileMap:
    """
    A tilemap used for collision detection.
    """

    def __init__(self, tile_list, tile_size, tileset, scale, x, y, parent=None) -> None:
        ## meta
        self.type = "tilemapcol"
        self.x = x
        self.y = y
        self.scale = scale
        self.assets = tileset.load_coll()
        self.tile_size = tile_size * scale / 100
        if not str(self.tile_size).endswith(".0"):
            self.tile_size = round(self.tile_size) - 1

        ## store tile map
        f = open(tile_list, "r")
        data = f.read()
        f.close()
        data = data.split("\n")

        if data[len(data) - 1] == "":
            del data[len(data) - 1]

        self.show = False
        self.width = len(data[0]) * self.tile_size
        self.height = len(data) * self.tile_size

        ## look-up table
        self.tiles_lookup = {}

        ## tile table
        self.tiles = []
        self.collisions = {}

        # resize and prepare tiles
        for key, tile in self.assets.items():
            if tile[0]:
                self.tiles_lookup[key] = (
                    pygame.transform.scale(
                        tile[0],
                        (
                            scale * tile[0].get_width() / 100,
                            scale * tile[0].get_height() / 100,
                        ),
                    ),
                    # left margin, right margin, top margin, bottom margin, left offset, top offset
                    (
                        tile[1][0],
                        tile[1][1],
                        tile[1][2],
                        tile[1][3],
                    ),
                )

        for y, row in enumerate(data):
            _tmprow = []
            for x, tile in enumerate(row.split(",")):
                if tile == "-1":
                    _tmprow.append(None)
                else:
                    tl = self.tiles_lookup[tile][1]
                    _tmprow.append(tile)
                    collision = CollisionRect(
                        x * self.tile_size + self.x + tl[0] * self.scale,
                        y * self.tile_size + self.y + tl[2] * self.scale,
                        (self.tile_size - tl[0] * self.scale / 100)
                        - tl[1] * self.scale / 100,
                        (self.tile_size - tl[2] * self.scale / 100)
                        - tl[3] * self.scale / 100,
                    )
                    collision.tx = x
                    collision.ty = y
                    collision.ox = tl[0] * self.scale / 100
                    collision.oy = tl[2] * self.scale / 100
                    self.collisions[f"({collision.tx}, {collision.ty})"] = collision
            self.tiles.append(_tmprow)

    def get_collisions_arround(self, element, dimensions=3):
        """
        Returns the collisions arround the playe
        """
        res = []
        tx = int(element.x // self.tile_size)
        ty = int(element.y // self.tile_size)
        start_x = tx - (dimensions // 2)
        start_y = ty - (dimensions // 2)
        end_x = start_x + dimensions - (dimensions // 2)
        end_y = start_y + dimensions - (dimensions // 2)
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                if self.tiles[y][x]:
                    res.append(self.collisions[f"({x}, {y})"])
        return res


class SpriteStack:
    def __init__(
        self, image_stack, x, y, scale=100, rotation=0, reverse=0, parent=None
    ):
        self.images = image_stack

        self.reverse = reverse

        self.x, self.y = x, y
        self.scale = scale
        self.rotation = rotation
        self.collision = None

        self.type = "spritestack"
        self.show = True
        self.is_hud = False
        self.cache = None
        self.outline_thickness = 5

        self.layer_separation = 10

    def prerender(
        self,
        angles,
        layer_separation,
        perspective_transformation,
        outline=0,
        outline_layers=[],
        offset_rotation=None,
    ):
        self.images.load(self.scale)
        self.w, self.h = self.images.w, self.images.h
        self.angles = angles
        self.cache = {}
        self.parent = None
        self.va = 360 // angles
        self.layer_separation = (
            (layer_separation * self.h / self.images.num_layers)
        ) / 2
        for deg in range(angles):
            size_surf = pygame.Surface(self.images.layers[0].get_size())
            size_surf = pygame.transform.rotate(
                size_surf, deg + (offset_rotation if offset_rotation else 0)
            )
            size_surf = pygame.transform.scale(
                size_surf,
                (
                    size_surf.get_width(),
                    size_surf.get_height() * perspective_transformation,
                ),
            )
            res = pygame.Surface(
                (
                    size_surf.get_width(),
                    size_surf.get_height()
                    + self.layer_separation * self.images.num_layers,
                ),
                pygame.SRCALPHA,
            )
            ores = copy.copy(res)
            for x, raw in enumerate(
                reversed(self.images.layers) if self.reverse else self.images.layers
            ):
                ## transform image

                ## rotate
                image = pygame.transform.rotate(
                    raw, deg * self.va + (offset_rotation if offset_rotation else 0)
                )
                image = pygame.transform.scale(
                    image,
                    (
                        image.get_width(),
                        image.get_height() * perspective_transformation,
                    ),
                )

                ## center image
                draw_x = res.get_width() / 2 - image.get_width() / 2
                image.get_height() - self.layer_separation * x
                draw_y = (
                    res.get_height() * 1.5 / 2
                    - image.get_height() / 2
                    - self.layer_separation * x
                )
                draw_y_2 = (
                    res.get_height() * 1.5 / 2
                    - image.get_height() / 2
                    - self.layer_separation * x
                    - self.layer_separation / 2
                )

                ## blit image
                if x + 1 in outline_layers:
                    outline = pygame.mask.from_surface(image).outline()
                    pygame.draw.polygon(image, "black", outline, self.outline_thickness)
                res.blit(image, (draw_x, draw_y))
                res.blit(image, (draw_x, draw_y_2))

            if outline:
                outline = pygame.mask.from_surface(res).outline()
                pygame.draw.polygon(ores, "black", outline, self.outline_thickness)

            res.blit(ores, (0, 0))

            self.cache[deg] = res

    def move_x(self, x, collision=None, multiplier=2):
        """
        Move or attempt to move the sprite horizontally (along the x-axis)

        Args:
            - x: The amount to move (positive for right, negative for left)
            - collision: The collision object to check against (optional)
            - multiplier: Multiplier to adjust the collision check distance

        Multiplier prevents the sprite from getting stuck to a collision. The higher the multiplier, the slower the sprite
        will move when colliding, but the wider the distance it can cover at higher speeds.
        """
        if collision:
            # Move while checking for collisions
            self.x += x
            self.collision.rect.rect.x += x * multiplier
            if self.collision.check_rect_collision(collision)[0]:
                self.x -= x
                self.collision.rect.rect.x -= x * multiplier

        else:
            self.x += x

    def move_y(self, y, collision=None, multiplier=2):
        """
        Move or attempt to move the sprite vertically (along the y-axis)

        Args:
            - y: The amount to move (positive for down, negative for up)
            - collision: The collision object to check against (optional)
            - multiplier: Multiplier to adjust the collision check distance

        Multiplier prevents the sprite from getting stuck to a collision. The higher the multiplier, the slower the sprite
        will move when colliding, but the wider the distance it can cover at higher speeds.
        """
        if collision:
            # Move while checking for collisions
            self.y += y
            self.collision.rect.rect.y += y * multiplier
            if self.collision.check_rect_collision(collision)[0]:
                self.y -= y
                self.collision.rect.rect.y -= y * multiplier
        else:
            self.y += y

    def move_towards(self, x, y, pixels, collision=None, multiplier=5):
        """
        Move the sprite towards a target point (x, y) by a specified number of pixels

        Args:
            - x, y: The target point coordinates
            - pixels: The number of pixels to move towards the target
            - collision: Thecollision object to check against (optional)
        - multiplier: Multiplier to adjust the collision check distance

        Returns:
            - mx, my: The actual movement in the x and y directions
            - direction: The direction in degrees from the sprite's current position to the target point
        """
        direction = -math.atan2(y - self.y, x - self.x)
        mx = math.cos(-direction) * pixels
        my = math.sin(-direction) * pixels
        self.move_x(mx, collision, multiplier)
        self.move_y(my, collision, multiplier)
        return mx, my, math.degrees(direction)

    def move_in_direction(self, direction, pixels, collisions=None, multiplier=5):
        """
        Move the sprite in a specific direction by a specified number of pixels

        Args:
            - direction: The direction in degrees (0 is right, 90 is down, 180 is left, 270 is up)
            - pixels: The number of pixels to move in the specified direction
            - collisions: The collision object(s) to check against (optional)
            - multiplier: Multiplier to adjust the collision check distance

        Returns:
            - mx, my: The actual movement in the x and y directions
            - direction: The direction in degrees (same as the input direction)
        """
        direction = math.radians(direction)
        mx = math.cos(-direction) * pixels
        my = math.sin(-direction) * pixels
        self.move_x(mx, collisions, multiplier)
        self.move_y(my, collisions, multiplier)
        return mx, my, math.degrees(direction)

    def point_towards(self, x, y, lag, dt):
        """
        Rotate the sprite to point towards a target point (x, y)

        Args:
            - x, y: The target point coordinates

        Returns:
            - The new rotation angle in degrees
        """
        target_rot = math.degrees(
            -math.atan2(
                y - self.y - (self.parent.y if self.parent else 0),
                x - self.x - (self.parent.x if self.parent else 0),
            )
        )
        max = 360
        da = (target_rot - self.rotation) % max
        self.rotation = self.rotation + ((2 * da % max - da) * lag) * dt
        if self.rotation < 0:
            self.rotation += 360

        return self.rotation


class Text:
    def __init__(self, text, x, y, font=None, size=20, color=(0, 0, 0)):
        if type(font) == str or font == None:
            self.font = pygame.font.Font(font, size)
        else:
            self.font = font.font
        self.orx = x
        self.ory = y
        self.color = color
        self.text = self.font.render(text, True, self.color)
        self.x = x - self.text.get_width() / 2
        self.y = y - self.text.get_height() / 2

        self.type = "text"
        self.show = True
        self.is_hud = True

    def render_text(self, text, update_pos=False):
        self.text = self.font.render(text, True, self.color)
        if update_pos:
            self.x = self.orx - self.text.get_width() / 2
            self.y = self.ory - self.text.get_height() / 2
