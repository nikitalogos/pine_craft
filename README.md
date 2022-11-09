![Pine Craft intro](docs/images/pine_craft_intro.jpg)

# Pine Craft

## About

Pine Craft is a constructor created for solving everyday tasks. Its key features are versatility, minimalism and simplicity of use.

Its scope of application includes DIY projects, furniture making, home repairs, life hacks. In addition, it can be used to teach children construction design and robotics. Also, Pine Craft can be successfully used in startups and laboratories for making prototypes and fixtures.

Pine Craft is very simple in manufacturing and usage. It requires a minimum of tools for assembly. The constructor is quickly assembled, and if necessary, it can be easily disassembled into parts for reuse.

Pine Craft is suitable for use at home, as it is based on eco-friendly material - pine plywood.

This repository contains a set of utilities for self-manufacturing Pine Craft parts, as well as detailed instructions for using this constructor.

## Examples

You can find sample layout generations under `examples` folder. There are:
1. `simplest` - minimal viable example
2. `stool_kit` - a set of parts to assemble a stool
3. `universal_kit` - basic starter kit to manufacture if you want to play around with Pine Craft

Examples of items made of Pine Craft can be found [here](docs/examples.md).

## Set of parts

### Beams and plates

- The Pine Craft constructor consists of parts made of plywood on a laser cutter and screws to fasten them together.
- Parts have a rectangular shape and their dimensions are multiples of the base segment size - `unit_size`.
- Holes for connecting parts form a pattern that repeats with the `unit_size` step
    - One element of the pattern consists of 4 holes evenly distributed in the circle with the diameter of `unit_size/2`.
        - This arrangement of holes allows you to connect parts along and across
        - The `unit_size/2` diameter of the circle allows you to connect parts with a half step

In practice, it is convenient to classify Pine Craft parts by their shape:
1. 1x1-sized parts are called spacers
2. linear parts with an aspect ratio of 1xN are called beams
    1. recommended beam sizes are: 1x2, 1x3, 1x5, 1x7, 1x10, 1x14, 1x20
    2. short beams - up to 1x5 - are used mainly for connecting parts
    3. long beams - 1x10, 1x14, 1x20 - are used to create the frame of the structure
3. rectangular parts are called plates
    1. recommended plate sizes are: 2x2, 2x3, 10x10, 10x15, 10x20, 10x30
    2. small plates - 2x2, 2x3 - are needed to connect parts
    3. large plates - 10x10 and larger - serve as working surfaces of products (shelf, seat, etc.)

### Cubes

"Cubes" are used to connect parts in space. The cubes are assembled from two pairs of parts and are held together by the grooves and the tightening force of the screws.

![Pine Craft cube](docs/images/pine_craft_cube.jpg)

### Screws and nuts

To connect Pine Craft parts, it is recommended to use M4 screws of two main lengths:
1. 20 mm - allows you to fasten 2 parts together
2. 50 mm - allows you to fasten together 7 parts, or one cube and two parts on both sides of it

![Screw lengths](docs/images/screw_lengths.jpg)

I use hexagon head screws, as they wear out less when reused and have a lower chance of tearing them off when tightening.

For M4 screws, a hex key with a side of 3mm is suitable. It is better to take a hex key with a convenient handle, since you will have to tinker a lot of screws :) And even better to buy a compact screwdriver!

It is better to use nuts with a flange - in theory they should cling better to the plywood and prevent unscrewing. To support the nuts, you can use a 7 mm wrench, but in fact, you can do without it.

Here is the bill of materials for screws and nuts:
1. DIN912 4x20 screw
2. DIN912 4x50 screw
3. Nut with flange DIN6923 m4

## Scale

The standard dimensions of the constructor are adapted to the dimensions of structures 0.5-2 m and loads of 10-100 kg. These parameters are calculated for reasons of human use in everyday life.

Here are the default dimensions:
1. The `unit_size` is 30x30 mm
2. Plywood thickness is 6 mm
3. Screws are M4

However, all the dimensions of the constructor can be customized for your purpose.

## Manufacturing

Pine Craft is recommended to be made of pine plywood, as it is a durable and eco-friendly material. It is not recommended to use plastic, acrylic, as well as chipboard materials.

For manufacturing, it is recommended to use a laser cutter, not a milling cutter, since it is faster and utilizes the sheet completely because no technical clearances between parts are needed.

You can use a built-in utility `pine-craft place-parts` to create a cutting layout in the .dxf format. This utility only supports laser fabrication, as it neglects the gaps between the parts. This is done intentionally, as it allows you to optimize the cutting length by an average of 25% since the contours of neighboring parts are cut simultaneously. The manufacturing time is also reduced by a quarter. With a laser cut width of about 1mm, this optimization does not harm the geometry of the constructor.

Here is the example of the auto-generated cutting layout. It contains parts needed to make a [stool](docs/examples.md):

![Stool layout](docs/images/stool_layout.jpg)

It is important for beams to have holes along the entire length, but this is not necessary for plates. A large number of holes greatly increases the cutting time - not only due to the length of the cut, but also due to the loss of time on moving the machine head between the holes. Therefore, it is recommended to use a sparse pattern for plates.

In practice, only the holes on the edges of the plate are used. However, I also prefer to leave holes in the center for aesthetic purposes.

## Command line tool

Global installation:

```bash
sudo install.sh
# --> restart shell here to enable autocompletion
pine-craft --help
```
