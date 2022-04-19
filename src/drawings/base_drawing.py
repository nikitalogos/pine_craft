class BaseDrawing:
    """Base class for vector drawing.
    Supports
    - creation of instance (container)
    - adding elements to container
    - saving to file"""

    DEFAULT_COLOR = 'black'

    def line(self, p0, p1, color=None):
        """Create a line by two points"""
        pass

    def circle(self, center, diameter, color=None):
        """Create a circle by center and diameter"""
        pass

    def polygon_filled(self, points, color=None):
        """Create polygon defined by its boundary.
        Polygon here means "closed shape with piecewise linear boundary without self-intersections or nested shapes"
        Polygon has only fill, not stroke."""
        pass

    def arc_csa(self, center, start, angle_deg, color=None):
        """Create arc defined by it's center, start point and sweep angle"""
        pass

    def write(self, file, is_no_ext=False):
        """Save drawing to file. Filename can be passed with or without extension."""
        pass
