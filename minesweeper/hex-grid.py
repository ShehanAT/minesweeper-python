from abc import ABCMeta, abstractmethod
import pygame
import math
# from hexmap.Map import Grid
from argparse import ArgumentParser


class Map(object):

    """
....An top level object for managing all game data related to positioning.
...."""

    directions = [
        (0, 1),
        (1, 1),
        (1, 0),
        (0, -1),
        (-1, -1),
        (-1, 0),
        ]

    def __init__(
        self,
        rows, cols,
        *args,
        **keywords
        ):

        # Map size

        self.rows = rows
        self.cols = cols

    def __str__(self):
        return 'Map (%d, %d)' % (self.rows, self.cols)

    @property
    def size(self):
        """Returns the size of the grid as a tuple (row, col)"""

        return (self.rows, self.cols)

    @classmethod
    def distance(self, start, destination):
        """Takes two hex coordinates and determine the distance between them."""

        logger.debug('Start: %s, Dest: %s', start, destination)
        diffX = destination[0] - start[0]
        diffY = destination[1] - start[1]

        distance = min(abs(diffX), abs(diffY)) + abs(diffX - diffY)

        logger.debug('diffX: %d, diffY: %d, distance: %d', diffX,
                     diffY, distance)
        return distance

    @classmethod
    def direction(self, origin, destination):
        """
........Reports the dominating direction from an origin to a destination.  if even, chooses randomly
........Useful for calculating any type of forced movement
........"""

        offset = (destination[0] - origin[0], destination[1]
                  - origin[1])
        scale = float(max(abs(offset[0]), abs(offset[1])))
        if scale == 0:
            return (0, 0)
        direction = (offset[0] / scale, offset[1] / scale)

        # Handle special cases

        if direction == (1, -1):
            return random.choice([(1, 0), (0, -1)])
        elif direction == (-1, 1):
            return random.choice([(-1, 0), (0, 1)])

        def choose(i):
            if i == 0.5:
                return random.choice((0, 1))
            elif i == -0.5:
                return random.choice((0, -1))
            else:
                return int(round(i))

        return (choose(direction[0]), choose(direction[1]))

    def ascii(self, numbers=True):
        """ Debug method that draws the grid using ascii text """

        table = ''

        if numbers:
            text_length = len(str((self.rows - 1 if self.cols % 2
                              == 1 else self.rows)) + ','
                              + str(int(self.rows - 1
                              + math.floor(self.cols / 2))))
        else:
            text_length = 3

        # Header for first row

        for col in range(self.cols):
            if col % 2 == 0:
                table += ' ' + '_' * text_length
            else:
                table += ' ' + ' ' * text_length
        table += '\n'

        # Each row

        for row in range(self.rows):
            top = '/'
            bottom = '\\'

            for col in range(self.cols):

# ................unit = "U" if units and self.positions.get( ( row + col / 2, col ) ) else ""

                if col % 2 == 0:
                    text = ('%d,%d' % (row + col / 2,
                            col) if numbers else '')
                    top += text.center(text_length) + '\\'
                    bottom += ''.center(text_length, '_') + '/'
                else:
                    text = ('%d,%d' % (1 + row + col / 2,
                            col) if numbers else ' ')
                    top += ''.center(text_length, '_') + '/'
                    bottom += text.center(text_length) + '\\'

            # Clean up tail slashes on even numbers of columns

            if self.cols % 2 == 0:
                if row == 0:
                    top = top[:-1]
            table += top + '\n' + bottom + '\n'

        # Footer for last row

        footer = ' '
        for col in range(0, self.cols - 1, 2):
            footer += ' ' * text_length + '\\' + '_' * text_length + '/'
        table += footer + '\n'
        return table

    def valid_cell(self, cell):
        (row, col) = cell
        if col < 0 or col >= self.cols:
            return False
        if row < math.ceil(col / 2.0) or row >= math.ceil(col / 2.0) \
            + self.rows:
            return False
        return True

    def neighbors(self, center):
        """
........Return the valid cells neighboring the provided cell.
........"""

        return filter(self.valid_cell, [
            (center[0] - 1, center[1]),
            (center[0], center[1] + 1),
            (center[0] + 1, center[1] + 1),
            (center[0] + 1, center[1]),
            (center[0], center[1] - 1),
            (center[0] - 1, center[1] - 1),
            ])

    def spread(self, center, radius=1):
        """
........A slice of a map is a collection of valid cells, starting at an origin, 
........and encompassing all cells within a given radius. 
........"""

        result = set((center, ))  # Start out with this center cell
        neighbors = self.neighbors(center)  # Get the neighbors for use later
        if radius == 1:  # Recursion end case
            result = result | set(neighbors)  # Return the set of this cell and its neighbors
        else:

                                 # Otherwise, recurse over all the neghbors,

            for n in neighbors:  # decrementing the radius by one.
                result = result | set(self.spread(n, radius - 1))
        return filter(self.valid_cell, result)  # filter invalid cells before returning.

    def cone(
        self,
        origin,
        direction,
        length=1,
        ):
        """
........A slice of a map is a section of cells, originating a a single cell and 
........extending outward through two cells separated by one cell between them.
........In the example below, starting at (0,0), (0,1) and (1,0) define a slice,
........as do (-1,-1) and (0,1).
........       _____  
........ _____/-1,0 \_____
......../-1,-1\_____/ 0,1 \
........\_____/ 0,0 \_____/
......../0,-1 \_____/ 1,1 \
........\_____/ 1,0 \_____/
........      \_____/
........"""

        result = self.slice(origin, direction, length)
        result.extend(self.slice(origin, (direction + 1) % 6, length))
        return filter(self.valid_cell, set(result))

    def slice(
        self,
        origin,
        direction,
        length=2,
        ):
        """
........A slice of a map is a section of cells, originating a a single cell and 
........extending outward through two neighboring cells.  In the example below,
........starting at (0,0), (0,1) and (1,1) define a slice, as do (-1,0) and 
........(-1,-1).
........       _____
........ _____/-1,0 \_____
......../-1,-1\_____/ 0,1 \
........\_____/ 0,0 \_____/
......../0,-1 \_____/ 1,1 \
........\_____/ 1,0 \_____/
........      \_____/
........"""

        # The edge wheel described in the docnotes above, used for calculating edges and steps

        # edge is the step we take for each distance,
        # step is the increment for each cell that distance out

        (edge, step) = (self.directions[direction % 6],
                        self.directions[(direction + 2) % 6])

        logger.debug('Edge: %s, Step: %s', edge, step)

        result = [origin]

        # Work each row, i units out along an edge

        for i in range(1, length + 1):
            start = (origin[0] + edge[0] * i, origin[1] + edge[1] * i)
            for j in range(i + 1):

                # calculate

                pos = (start[0] + step[0] * j, start[1] + step[1] * j)
                result.append(pos)
        return filter(self.valid_cell, result)

    def line(
        self,
        origin,
        direction,
        length=3,
        ):
        """
........Returns all the cells along a given line, starting at an origin
........"""

        offset = self.directions[direction]
        results = [origin]

        # Work each row, i units out along an edge

        for i in range(1, length + 1):
            results.append((origin[0] + offset[0] * i, origin[1]
                           + offset[1] * i))
        return filter(self.valid_cell, results)

    def cells(self):
        cells = []
        for row in range(self.rows + self.cols / 2):
            cells.extend([(row, col) for col in range(1 + 2 * row)])
        return filter(self.valid_cell, cells)


class Grid(dict):

    """An extension of a basic dictionary with a fast, consistent lookup by value implementation."""

    def __init__(
        self,
        default=None,
        *args,
        **keywords
        ):
        super(Grid, self).__init__(*args, **keywords)
        self.default = default

    def __getitem__(self, key):
        return super(Grid, self).get(key, self.default)

    def find(self, item):
        """
........A fast lookup by value implementation
........"""

        for (pos, value) in self.items():
            if item == value:
                return pos
        return None


class MapUnit(object):

    """
....An abstract base class that will contain or require implementation of all 
....the methods necessary for a unit to be managed by a map object.
...."""

    __metaclass__ = ABCMeta

    def __init__(self, grid):
        self.grid = grid

    @property
    def position(self):
        """A property that looks up the position of this unit on it's associated map."""

        return self.grid.find(self)

    @abstractmethod
    def paint(self, surface):
        """An abstract base method to contain the painting code for a given unit."""

        pass


if __name__ == '__main__':

    # Setup arguments for testing this code

    parser = \
        ArgumentParser(description='Process some integers.')
                # argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument(
        '-r',
        '--rows',
        dest='rows',
        type=int,
        default=5,
        help='Number of rows in grid.  Defaults to 5.',
        )
    parser.add_argument(
        '-c',
        '--cols',
        dest='cols',
        type=int,
        default=5,
        help='Number of columns in grid.  Defaults to 5.',
        )
    parser.add_argument(
        '-n',
        '--numbers',
        action='store_true',
        dest='numbers',
        default=False,
        help='Display grid numbers on tiles.  Defaults to false.',
        )
    parser.add_argument(
        '-i',
        '--interactive',
        action='store_true',
        dest='interactive',
        default=False,
        help='Provide a ncurses interactive interface.',
        )

    args = parser.parse_args()
    print('Args: %s' % args)
    m = Map(args.rows, args.cols)
    m.units = Grid()
    numbers = args.numbers

    if args.interactive:
        try:
            import curses
            import re
            stdscr = curses.initscr()
            stdscr.keypad(1)

            while True:
                stdscr.addstr(1, 0, m.ascii(numbers=numbers))
                c = stdscr.getstr()
                stdscr.clear()
                if c == 'q':
                    break
                elif c == 'N':
                    numbers = not numbers
        finally:

            curses.nocbreak()
            stdscr.keypad(0)
            curses.echo()
            curses.endwin()
    else:
        print(m.ascii(numbers))


SQRT3 = math.sqrt( 3 )

class Render( pygame.Surface ):

	__metaclass__ = ABCMeta



	def __init__( self, map, radius=16, *args, **keywords ):
		self.map = map
		self.radius = radius

		# Colors for the map
		self.GRID_COLOR = pygame.Color( 50, 50, 50 )

		super( Render, self ).__init__( ( self.width, self.height ), *args, **keywords )

		self.cell = [( .5 * self.radius, 0 ),
					( 1.5 * self.radius, 0 ),
					( 2 * self.radius, SQRT3 / 2 * self.radius ),
					( 1.5 * self.radius, SQRT3 * self.radius ),
					( .5 * self.radius, SQRT3 * self.radius ),
					( 0, SQRT3 / 2 * self.radius )
		]



	@property
	def width( self ):
		return	math.ceil( self.map.cols / 2.0 ) * 2 * self.radius + \
				math.floor( self.map.cols / 2.0 ) * self.radius + 1
	@property
	def height( self ):
		return ( self.map.rows + .5 ) * self.radius * SQRT3 + 1

	def get_surface(self, row, col):
		"""
		Returns a subsurface corresponding to the surface, hopefully with trim_cell wrapped around the blit method.
		"""
		width = 2 * self.radius
		height = self.radius * SQRT3

		top = ( row - math.ceil( col / 2.0 ) ) * height + ( height / 2 if col % 2 == 1 else 0 )
		left = 1.5 * self.radius * col

		return self.subsurface( pygame.Rect( left, top, width, height ) )

	# Draw methods
	@abstractmethod
	def draw( self ):
		"""
		An abstract base method for various render objects to call to paint 
		themselves.  If called via super, it fills the screen with the colorkey,
		if the colorkey is not set, it sets the colorkey to magenta (#FF00FF)
		and fills this surface. 
		"""
		color = self.get_colorkey()
		if not color:
			magenta = pygame.Color( 255, 0, 255 )
			self.set_colorkey( magenta )
			color = magenta
		self.fill( color )

	# Identify cell
	def get_cell(self, x, y):
		"""
		Identify the cell clicked in terms of row and column
		"""
		# Identify the square grid the click is in.
		row = math.floor( y / ( SQRT3 * self.radius ) )
		col = math.floor( x / ( 1.5 * self.radius ) )

		# Determine if cell outside cell centered in this grid.
		x = x - col * 1.5 * self.radius
		y = y - row * SQRT3 * self.radius

		# Transform row to match our hex coordinates, approximately
		row = row + math.floor( ( col + 1 ) / 2.0 )

		# Correct row and col for boundaries of a hex grid 
		if col % 2 == 0:
			if 	y < SQRT3 * self.radius / 2 and x < .5 * self.radius and \
				y < SQRT3 * self.radius / 2 - x:
				row, col = row - 1, col - 1
			elif y > SQRT3 * self.radius / 2 and x < .5 * self.radius and \
				y > SQRT3 * self.radius / 2 + x:
				row, col = row, col - 1
		else:
			if 	x < .5 * self.radius and abs( y - SQRT3 * self.radius / 2 ) < SQRT3 * self.radius / 2 - x:
				row, col = row - 1 , col - 1
			elif y < SQRT3 * self.radius / 2:
				row, col = row - 1, col


		return ( row, col ) if self.map.valid_cell( ( row, col ) ) else None

def fit_window(self, window):
    top = max( window.get_height() - self.height, 0 )
    left = max( window.get_width() - map.width, 0 )
    return ( top, left )

class RenderUnits(Render):
	"""
	A premade render object that will automatically draw the Units from the map 
	
	"""

	def __init__( self, map, *args, **keywords ):
		super( RenderUnits, self ).__init__( map, *args, **keywords )
		if not hasattr( self.map, 'units' ):
			self.map.units = Grid()

	def draw( self ):
		"""
		Calls unit.paint for all units on self.map
		"""
		super( RenderUnits, self ).draw()
		units = self.map.units

		for position, unit in units.items():
			surface = self.get_surface( position )
			unit.paint( surface )

class RenderGrid( Render ):
	def draw( self ):
		"""
		Draws a hex grid, based on the map object, onto this Surface
		"""
		super( RenderGrid, self ).draw()
		# A point list describing a single cell, based on the radius of each hex

		for col in range( self.map.cols ):
			# Alternate the offset of the cells based on column
			offset = self.radius * SQRT3 / 2 if col % 2 else 0
			for row in range( self.map.rows ):
				# Calculate the offset of the cell
				top = offset + SQRT3 * row * self.radius
				left = 1.5 * col * self.radius
				# Create a point list containing the offset cell
				points = [( x + left, y + top ) for ( x, y ) in self.cell]
				# Draw the polygon onto the surface
				pygame.draw.polygon( self, self.GRID_COLOR, points, 1 )

class RenderFog( Render ):

	OBSCURED = pygame.Color( 00, 00, 00, 255 )
	SEEN	 = pygame.Color( 00, 00, 00, 100 )
	VISIBLE	 = pygame.Color( 00, 00, 00, 0 )

	def __init__( self, map, *args, **keywords ):

		super( RenderFog, self ).__init__( map, *args, flags=pygame.SRCALPHA, **keywords )
		if not hasattr( self.map, 'fog' ):
			self.map.fog = Grid( default=self.OBSCURED )

	def draw( self ):

		#Some constants for the math		
		height = self.radius * SQRT3
		width = 1.5 * self.radius
		offset = height / 2

		for cell in self.map.cells():
			row, col = cell
			surface = self.get_cell( cell )

			# Calculate the position of the cell
			top = row * height - offset * col
			left = width * col

			#Determine the points that corresponds with
			points = [( x + left, y + top ) for ( x, y ) in self.cell]
			# Draw the polygon onto the surface
			pygame.draw.polygon( self, self.map.fog[ cell ], points, 0 )




def trim_cell( surface ):
	pass


if __name__ == '__main__':
	# from Map import Map, MapUnit
    # import Map
    # import MapUnit
    import sys

    class Unit( MapUnit ):
	    color = pygame.Color( 200, 200, 200 )
def paint( self, surface ):
    radius = surface.get_width() / 2
    pygame.draw.circle( surface, self.color, ( radius, int( SQRT3 / 2 * radius ) ), int( radius - radius * .3 ) )

    m = Map( ( 5, 5 ) )

    grid = RenderGrid( m, radius=32 )
    units = RenderUnits( m, radius=32 )
    fog = RenderFog( m, radius=32 )

    m.units[( 0, 0 ) ] = Unit( m )
    m.units[( 3, 2 ) ] = Unit( m )
    m.units[( 5, 3 ) ] = Unit( m )
    m.units[( 5, 4 ) ] = Unit( m )

    for cell in m.spread( ( 3, 2 ), radius=2 ):
        m.fog[cell] = fog.SEEN

    for cell in m.spread( ( 3, 2 ) ):
        m.fog[cell] = fog.VISIBLE

    print( m.ascii() )


    try:
        pygame.init()
        fpsClock = pygame.time.Clock()

        window = pygame.display.set_mode( ( 640, 480 ), 1 )
        from pygame.locals import QUIT, MOUSEBUTTONDOWN

        #Leave it running until exit
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    print( units.get_cell( event.pos ) )

            window.fill( pygame.Color( 'white' ) )
            grid.draw()
            units.draw()
            fog.draw()
            window.blit( grid, ( 0, 0 ) )
            window.blit( units, ( 0, 0 ) )
            window.blit( fog, ( 0, 0 ) )
            pygame.display.update()
            fpsClock.tick( 10 )
    finally:
        pygame.quit()


