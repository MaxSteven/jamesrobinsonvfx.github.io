---
layout: post
title: Transform RBD Pieces with Alembic Layering
description: Create two separate Alembic caches for geometry and transforms and combine them later
thumbnail: /assets/posts/xform-pieces-alembic-layering/images/preview.png
categories: tips
tags: houdini rbd alembic
---

> Hipfile: [jamesr_alembicrbdlayers.hip](/assets/posts/xform-pieces-alembic-layering/jamesr_alembicrbdlayers.hiplc)
>
> Or follow along on [hdbp.io](https://hdbp.io/xsx5HQz2)

![](/assets/posts/xform-pieces-alembic-layering/images/xform-pieces.mp4)
<video width="720" height="405" autoplay loop>
	<source src="/assets/posts/xform-pieces-alembic-layering/images/xform-pieces.mp4" type="video/mp4">
</video>

## Overview
There are plenty of ways to transfer RBD data from one application to another.
Some facilities might have proprietary tools to make this pretty straightforward
and quick. Others might use
[USD](https://graphics.pixar.com/usd/docs/index.html). But what if you don't
have either option?

One kind of interesting way of doing it is to use **Alembic Layering**.

## Concept

### Obstacles
One thing we *absolutely* want to avoid when writing RBD geo to Alembic is
writing all the pieces out as a single, unpacked, deforming point cache. This is
a huge waste of time and space because:

- All of the points and mesh data will be written on each frame.
- We are forced to use deformation blur.
- If we need more detailed motion blur, we must write *more motion samples* into
  the cache.

Multiply those factors by all of your iteration time and you get a really slow turnaround!

### Packed Geometry to the Rescue
Houdini is perfectly capable of writing its own packed geometry format as
packed Alembic primitives. Houdini treats each packed prim like its own
*object* and so each primitive gets its own *transform*. This is great beacause:

- We only need to wait for the mesh data to write into the Alembic cache once.
- Alembic caches are much smaller, since only one copy of the mesh data exists.
  The rest of the data is just time-varying attributes and transform matrices.
- We don't need to use motion samples or deformation blur.

### Take it a Step Further
This is all sounding pretty great! And for a small, lower-res sim this would
probably suffice. But what if we have a bigger sim, with pretty high-res pieces?
When writing the Alembic to disk, we would still need to wait for Houdini to
transform the packed high res pieces, and write their transforms.

Instead, what if we wrote the high-res static pieces to disk *once*, and anytime we
wanted to change the sim and export it, we write *only* the transforms from the
low-res sim to a cache, and leave the high-res static piece alone?

Alembic let's us do exactly that, using *Alembic Layering!*

### Layering
The concept behind layering transforms is simple:

1. Write one static Alembic cache of the high-res pieces.
2. Write one animated Alembic cache of *only* the transforms of each piece.
3. Load the static cache, and layer the transforms on top so that they override
   the static static transforms.

## Requirements

### `s@path` Attribute
Each piece needs to have a `s@path` attribute that corresponds to its place in a
a hierarchy. It's important that each piece has room for both a **Transform**
and **Shape**. Here's an example of a good looking `s@path`:

![Set Path from Name](/assets/posts/xform-pieces-alembic-layering/images/path-from-name.png)

```
s@path = sprintf("pieces_grp/%s_geo/%s_geoShape", s@name, s@name);
```

It's also crucial that the paths on the high-res geometry and the low-res
transform match up!

### Packed Geometry / Fragments
It's important that each piece is *packed*. This is how Houdini will get the
transform it needs. Make sure that the pieces are backed *before* transforming them. If
you're using this method with a **Copy to Points** SOP, or a **Transform
Pieces** SOP, make sure the geo is packed *before* moving them around. This way,
the `primintrinsic:packedfulltransform` will actually get updated! (ie. *don't*
copy/xform the unpacked pieces, then use an **Assemble** SOP to pack 'em up *after*.)

> There is a little trick to get the pivots to line up correctly, so please see
> the demo file for details on that if you're exporting RBD pieces and noticing
> some misalignment!


## ROP it Out
![Output](/assets/posts/xform-pieces-alembic-layering/images/network-output.png)

In order for the Alembic to work for our purposes, a few of the defaults need to
be changed on the **Alembic ROP**.

### Both ROPs
- Enable **Hierarchy > Build Hierarchy from Attribute**.
- Ensure **Path Attribute** is the same as the one you made earlier.
- **Geometry > Packed Transform** should be set to **Merge With Parent Transform**
- Disable **Use Instancing Where Possible** if this is an RBD sim with unique pieces.

![High Res Pieces Output Settings](/assets/posts/xform-pieces-alembic-layering/images/high-res-pieces.png)
High Res Pieces Output Settings

### Transforms Cache
- Make sure to disable **Create Shape Nodes**.

![Low Res Xform Output Settings](/assets/posts/xform-pieces-alembic-layering/images/low-res-xforms.png)
Low Res Xform Output Settings

> Since we are only concerned with storing the tranformation of each piece, don't
write the shape data in this cache. Otherwise, it will overwrite the high res
mesh completely when we layer it back in!

## Import in your DCC of Choice
The most common target application is probably going to be Maya. I'm not too
familiar with the procedurals for any other render engine aside from **Arnold**,
so I'll stick to what I know.

If you're rendering with Arnold in Houdini, it's as simple as setting the render
flag of an object to render an Alembic SOP. Arnold will render Packed Alembics
as procedurals by default.

![Layers](/assets/posts/xform-pieces-alembic-layering/images/layers.png)
<small>Alembic SOP in Houdini with layers</small>

### Recommendations

| Do                                                                    | Don't                                                                                                                                                                |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Load Alembic as a GPU Cache (Maya) or as an Arnold Standin Procedural | *Do Not* just do a  `File > Import`  and load the cache as Maya geometry. For a heavy sim with thousands of transforms and shape nodes, you're likely to crash Maya! |
