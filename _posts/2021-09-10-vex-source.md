---
layout: post
title: Vex Source
description: Use one VOP network or VEX wrangle to drive many others without channel referencing
thumbnail: /assets/posts/vex-source/images/preview.png
categories: tips
tags: houdini vex vops
---

> Hipfile: [jamesr_vexsource.hiplc](/assets/posts/vex-source/jamesr_vexsource.hiplc)
{:style="border-color: #d08770"}

[[![Cover Photo](/assets/posts/vex-source/images/preview.png)]((/assets/posts/vex-source/images/preview.png))](((/assets/posts/vex-source/images/preview.png)))

Houdini offers several ways to duplicate and reuse nodes.

- Copy and paste nodes (**Ctrl + c**, **Ctrl + v**).
- Create an HDA.
- **RMB** > **Actions** > **Create Reference Copy**

...to name a few.

Sometimes, you might find yourself re-using the same VOP network or VEX wrangle
without changing the internal nodes or code. But what happens if you want to
change them all at once?

## Scenario

![](/assets/posts/vex-source/images/noisey-flippy.mp4)
<video width="720" height="405" autoplay loop>
	<source src="/assets/posts/vex-source/images/noisey-flippy.mp4" type="video/mp4">
</video>

Let's say we have a VOP network that applies some noisey displacement animation
to a character (see hipfile above). There are several other characters in the
scene who need the same displacement effect applied to them. We have a few
options:

### Option 1: Copy and Paste the VOP Network
[![Copy and Paste](/assets/posts/vex-source/images/copy-paste.gif)]((/assets/posts/vex-source/images/copy-paste.gif))

Simple as that. We can just duplicate it around and we're all set. 90% of the
time this will probably be what you do day-to-day. The downside though is that
anytime you update the internal nodes/code, you'll have to do the same thing to
all the copies...

### Option 2: Create an HDA

HDAs are perfect for when you want to bundle up some nodes and reuse them all
over the place. There are numerous advantages to using HDAs that I won't go into
in this post, but sometimes creating and tracking an HDA is just a bit overkill.
In our case, we have one VOP that makes some noise...we don't really need to go
through the effort of creating an asset for it!

### Option 3: Create a Reference Copy

[![Reference Copy](/assets/posts/vex-source/images/reference-copy.gif)]((/assets/posts/vex-source/images/reference-copy.gif))

> **RMB** > **Actions** > **Create Reference Copy**

We could create a **Reference Copy** which is really just like copying and
pasting the node like in the first option, except the new pasted node has
relative channel references back to all the parameters on the source node. This
works just fine, and we get a copy of all the internal nodes as well. But even
with the reference copy, if we were to change the internal nodes of the source
VOP network like adding new nodes or removing old ones, those changes would
*not* be reflected in the copies.

### Option 4: Change the Vex Source

The last option we'll go over is really the whole point of this post. On each VOP
network, there is a parameter called **Vex Source**. By default, this is is set
to **Myself**, which means it uses the operators inside itself to do all the work.

[![Vex Source Parameter](/assets/posts/vex-source/images/vex-source.png)]((/assets/posts/vex-source/images/vex-source.png))

If we change it instead to **Shop**, the **Shop Path** parameter is then
exposed, and we can actually set that parameter to *another VOP network in the
scene*.

We leave this VOP network empty - its internals are being overridden by the
contents of the VOP network specified in that **Shop Path** parameter!

#### Steps

[![VOP Network Shop Path Setup GIF](/assets/posts/vex-source/images/vopnet-shop-path-setup.gif)]((/assets/posts/vex-source/images/vopnet-shop-path-setup.gif))

To recap, the steps are as follows:
1. Create a VOP network that does something you want to reuse on other geo.
2. Create an empty VOP network and hook it up to wherever you want to reuse the original.
3. Select the original VOP network and hit **Ctrl + c**. This will copy the path
   to the node to the clipboard.
4. Select the empty VOP network, and set the **Vex Source** paramater to **Shop**.
5. Paste the copied path to the source VOP network in the **Shop Path**
   parameter (if you want this to be a relative path, that's fine too).

[![Make a change](/assets/posts/vex-source/images/change-source-vopnet.gif)]((/assets/posts/vex-source/images/change-source-vopnet.gif))

<small>Changes to the source networkl are propagated immediately!</small>

## What about Wrangles?
Hidden inside each wrangle is actually just a VOP network with a Snippet VOP
inside!

VEX wrangles don't have the **Vex Source** parameter exposed at the top level, so we
actually won't be able to use an empty wrangle on each of our other streams.

Instead, let's just write one wrangle with the code on it that we want to reuse, and the
rest of the geometry we want to copy it around to will have empty *VOP
Networks* instead, just like before.

[![Wrangle Source](/assets/posts/vex-source/images/reference-wrangle.gif)]((/assets/posts/vex-source/images/reference-wrangle.gif))

#### Steps:
1. Create the source wrangle with the desired code.
2. Create an empty VOP network and hook it up to the other geometry we want to process.
3. Dive inside the source wrangle node, and **Ctrl + c** on the VOP network inside. This copies the path to the node to the clipboard.
4. On each of the new empty VOP networks, set the **Vex Source** parameter to **Shop**.
5. Paste the path of the copied VOP network into the **Shop Path** parameter.

## Final Notes
The biggest downside to this method is that you can't really adjust the
parameters on the copies. However, you could get around this by instead using
attributes on the geometry to control certain parts of your setup!

[![Attributes for Parameters](/assets/posts/vex-source/images/attribs-for-parms.gif)]((/assets/posts/vex-source/images/attribs-for-parms.gif))
