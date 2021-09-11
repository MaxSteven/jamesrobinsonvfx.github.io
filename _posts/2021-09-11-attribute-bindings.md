---
layout: post
title: Attribute Bindings
description: Write to attributes with one name while using another in your code
thumbnail: /assets/posts/attribute-bindings/images/preview.png
categories: tips
tags: houdini vex attributes tools
---

> Hipfile: [jamesr_attributebindings.hip](/assets/posts/attribute-bindings/jamesr_attributebindings.hip)
{:style="border-color: #d08770"}

[![Cover Photo]({{ page.thumbnail }})]({{ page.thumbnail }})

## Purpose

## Scenario
Let's say we want to build a tool/setup that changes something when
- A point is in a specific group


and we also want the user to be able specify what the name of the attribute is,
as well as the new group that the point belongs to.

The first issue we encounter is the flexibility part. If

For our purposes, hardcoding the attributes and group names is not an option. It
forces the user to actually tear apart your code (gasp!) and make sure all the
references to a specifically named attribute


## `setpointattrib()` and Friends
One common function you often see handling this sort of situation is
`setpointattrib()` (and its friends `setprimattrib()` etc...). Let's see how we
can use it






While this function certainly does what we are asking, *it is painfully slow*
when iterating over many many points, which isn't an uncommon task!

Let's do a quick comparison with the **Performance Monitor**. First we'll create
a point cloud consisting of `30,000,000` points. In this example, we want to
randomize some user-specified attribute relating to the scale of the points. In
the code, we'll refer to it simply as `f@scale`. The user can specify the name
they want it to actually be (probably `f@pscale`), and we'll write our result
into that attribute.

On the left stream, we have the following code



The difference is ~5x faster on my machine. Now the difference between `0.7s`
and `3.0s` per cook might not seem like a huge amount if you're already waiting
a minute or so per-frame to process a heavy point cloud (like a big FLIP sim).
But consider that in this example we are modifying just a *single* attribute, in
*one* wrangle. In a real-world setup, you might have several attributes and be
doing a few different things in different wrangles and steps which can really
add up!

## Volumes
This technique is *especially* useful when dealing with fields in Volume VOPs.
Have you ever dived inside a **Gas Turbulence DOP** or any similar nodes? If you
look in the Attribute Bindings section, you'll see that SideFX uses these all
the time! It's how you're able to specify the name of any **Control Field**, but
internally they only need to use one name!


## Attributes to Create

This parameter is often overlooked, and it's default is just `*` - which means
any attributes referred to in the wrangle using the `@` syntax will be created
if it they don't exist already.

The default is usually fine. But sometimes, you might be using an attribute
temporarily just to do some sort of calculation, and you don't actually want it
to be created and passed along through the output. In that case, you can just
use the `^` character plus the attribute name to skip it! This is also useful if you
have a tool that *allows* a user attribute to passed in but does not *require*
it.

Take this for example:

We have a tool that modifies the thickness of some curves. By default, the code
will apply some randomness. The user is also given the option to provide an
attribute by which to multiply the randomized thickness. For clarity, let's
provide a sensible default value like `thicknessscale` (sort of how vellum, and
other tools across houdini fill it in too). If we structure our code like so:


```
Code
```

with the following attribute bindings:

[![]()]()


we get exactly what we're after. In this example, the user provided an attribute
called `age_scale`, and it scaled the thickness of the curves over time.

But what happens if they don't want to do any extra scaling? If no attribute is
provided, and the binding is left blank or the attribute doesn't exist we wind up with a bit of an issue...


[![Scales are Zero]()]()

All the scales are now zero! Well that's not really what we want... if the user
doesn't specify an attribute (or if it doesn't exist), we should carry on and happily apply just the
randomized value to the thickness.


```
float @mod = 1.0;
f@scale = 1.0 * f@mod;
```

This works excellently! Now, even though the attribute is missing, everything
is just multiplied by `1.0`, so we're in the clear. But let's look at the
attributes now...

[![]()]()

Oh no! Since that default value we have sitting in there wasn't cleared out, and
since it doesn't already exist on the points, we wound up creating some attribute called `thicknessscale` with a value
of `1.0`! That's sort of annoying. If the user didn't ask for an attribute to
created, we should really just leave it alone.

Leaving it alone is simple. Just exclude it from that **Attributes to Create**
parameter.

[![Exclude f@mod Attribute]()]()

```
* ^mod
```


> The attributes specified in this list are the same as the *Vex Parameters* you're using in your code, even if they are *bound* to something different.


[![No Extra Attributes]()]()


If the attribute *does* exist on the points beforehand, don't worry - this
option won't cause it to be deleted. It will still passthrough just as expected,
with the added bonus that since it's being ignored in the **Attributes to
Create** parameter, we aren't able to actually write to it, which means we can't
muck it up inbetween!








- set a group name
- view the group (bonus!)



basic attribute binding

The idea is pretty straightforward. The **Attribute Name** is the name of the
attribute you *really* want to write to. **Vex Parameter** is simply what you'll
call that attribute inside your code. Think of this as an *alias* for the
attribute name that you actually care about. Let's see it in action:

