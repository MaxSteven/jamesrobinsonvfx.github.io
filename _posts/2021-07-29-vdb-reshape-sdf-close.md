---
layout: post
title: VDB Reshape SDF Close
description: Faster way to dilate and erode an SDF
thumbnail: /assets/posts/vdb-reshape-sdf-close/images/preview.jpg
categories: tips
tags: houdini vdb sdf
---

### Overview

{:.toc}
- [Old Way](#old-way)
- [New Way](#new-way)
- [Conclusion](#conclusion)

> Hipfile: [jamesr_vdbreshapesdfclose.hip](/assets/posts/vdb-reshape-sdf-close/jamesr_vdbreshapesdfclose.hiplc)

### Old Way
Most people are probably familiar with the following workflow for sealing up
gaps and holes in an SDF using 2 **VDB Reshape SDF** nodes:

1. Set the first one to **Dilate**
2. Set the second one to **Erode**
3. Channel reference the **Offset** parameter from the dilating node to the
   **Offset** parameter of the eroding node.
4. Adjust the offset until you're happy

> If you want to keep a filled interior, don't forget to set the **Trim**
> parameter to **None** (Houdini 18.5+)!

![Old way](/assets/posts/vdb-reshape-sdf-close/images/old-way.jpg)


### New Way
Not sure when this was added (or maybe it has been here the whole time!), but
there is another method that does the exact same thing in one go: **Close**.

![New way](/assets/posts/vdb-reshape-sdf-close/images/new-way.jpg)

### Conclusion
A side-by-side comparison of the two looks like you get the same result!

![Side by side](/assets/posts/vdb-reshape-sdf-close/images/side-by-side.gif)
