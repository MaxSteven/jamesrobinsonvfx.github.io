---
layout: post
title: Transform RBD Pieces with Alembic Layering
description: Create two separate alembic caches for geometry and transforms and combine them later.
thumbnail: /assets/posts/xform-pieces-alembic-layering/images/preview.png
categories: tips
tags: houdini rbd alembic
---

> Hipfile: [jamesr_alembicrbdlayers.hip](/assets/posts/xform-pieces-alembic-layering/jamesr_alembicrbdlayers.hiplc)
>
> Or check it out on [hdbp.io](https://hdbp.io/xsx5HQz2)

![](/assets/posts/xform-pieces-alembic-layering/images/xform-pieces.mp4)
<video width="960" height="540" autoplay loop>
	<source src="/assets/posts/xform-pieces-alembic-layering/images/xform-pieces.mp4" type="video/mp4">
</video>

![Layers](/assets/posts/xform-pieces-alembic-layering/images/layers.png)

![Output](/assets/posts/xform-pieces-alembic-layering/images/network-output.png)
![Low Res Xform Output Settings](/assets/posts/xform-pieces-alembic-layering/images/low-res-xforms.png)
![High Res Pieces Output Settings](/assets/posts/xform-pieces-alembic-layering/images/high-res-pieces.png)
![Set Path from Name](/assets/posts/xform-pieces-alembic-layering/images/path-from-name.png)
```
s@path = sprintf("pieces_grp/%s_geo/%s_geoShape", s@name, s@name);
```