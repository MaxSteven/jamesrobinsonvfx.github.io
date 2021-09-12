---
layout: post
title: Attribute Bindings
shortname: attribute-bindings
description: Write to attributes with one name while using another in your code
thumbnail: /assets/posts/attribute-bindings/images/preview.png
categories: tips
tags: houdini vex attributes tools
---

{% capture images %}/assets/posts/{{ page.shortname }}/images{% endcapture %}

> Hipfile: [jamesr_attributebindings.hiplc](/assets/posts/attribute-bindings/jamesr_attributebindings.hiplc)
{:style="border-color: #d08770"}

[![Cover Photo]({{ page.thumbnail }})]({{ page.thumbnail }})

## Basics

Let's build a super simple setup that applies randomness to an attribute on some
points. The user will specify which attribute they want to write to. We also
want the user to be able to scale the points by any attribute they specify
without changing any of the code.

So the first thing we will need is some logic to randomize a value, and write it
out. In this case, let's start with `pscale` so we can see what's happening.

[![Scale Points]({{ images }}/scale-points.png)]({{ images }}/scale-points.png)

```c
float r = rand(i@ptnum);

f@pscale *= r * chf("global_scale");
```
Easy enough!

## `point()`, `setpointattrib()` and Friends


### Reading

Next, we'll need to fetch the user-specified attribute that we want to scale the
randomness by. The most familiar way is by using the `point()` function.

[![User Attrib]({{ images }}/user-scale.png)](({{ images }}/user-scale.png))

```c
f@coolscale = pow(relbbox(0, v@P).z, 4.0);
```

In this case we have a user-specified attribute called `coolscale`. We'll use the
`point()` function and a string parameter `chs()` to get that value.

[![User Attrib]({{ images }}/user-scale-point-func.png)](({{ images }}/user-scale-point-func.png))

So far so good. We've queried the custom user attribute and scaled our
randomness by it.

### Writing

We've successfully written to `pscale` so far. But remember that our setup's
requirements call for the user to be able to specify the output attribute.
Currently, we have it hardcoded to `f@pscale`.

In order to write to a custom attribute, let's add another parameter to specify
what the attribute should be called and use the `setpointattrib()` function to
write the value to the points.

[![Output Attrib]({{ images }}/output-attrib.png)](({{ images }}/output-attrib.png))

```c
float r = rand(i@ptnum);

float user_scale = point(0, chs("user_scale_attrib"), i@ptnum);

float scale =  r * user_scale * chf("global_scale");

setpointattrib(0, chs("output_attrib"), i@ptnum, scale);
```

While this function certainly does what we are asking, *it is painfully slow*
when iterating over many many points, which isn't an uncommon task! So how can
we do it all a bit better? Let's take a look at the **Bindings** tab.

### Attribute Bindings Tab

[![Attribute Bindings Tab]({{ images }}/attrib-bindings.png)]({{ images }}/attrib-bindings.png)

The idea is pretty straightforward. The **Attribute Name** is the name of the
attribute you *really* want to write to. **Vex Parameter** is simply what you'll
call that attribute inside your code. Think of this as an *alias* for the
attribute name that you actually care about.

We can modify our setup to use this method instead:

[![Rewrite Code]({{ images }}/rewrite-code.gif)]({{ images }}/rewrite-code.gif)

```c
float r = rand(i@ptnum);

f@scaled =  r * f@user_scale * chf("global_scale");
```

Our code has just gotten much simpler. We only need to refer the attributes that we put
in the **Vex Parameter** parameters using the familiar `@` syntax.

[![New Bindings]({{ images }}/new-bindings.png)]({{ images }}/new-bindings.png)

We can take advantage of the `chs()` channels we already made, and just channel reference them in the
bindings section. That way the interface can stay user-friendly (especially for whenever you
want to promote these up to the interface of a digital asset or something).


### Speed Comparison

Let's do a comparison with the **Performance Monitor**.

[![Performance Test]({{ images }}/perf-test.png)]({{ images }}/perf-test.png)

With ~112k points we can see that the `setpointattrib()` method takes about
`0.081 seconds` to cook, whereas the **Attribute Bindings** method takes
`0.002 seconds`! That's a pretty big difference, though `0.08` seconds is
pretty negligible too.

What happens if we try with a a point cloud consisting of `30,000,000` points?

[![Performance Test 30m Points]({{ images }}/perf-test-30m.png)]({{ images }}/perf-test-30m.png)

**Attribute Bindings** wins by a factor of ~30x on my machine. Now the difference between `0.13s`
and `3.9s` per cook might not seem like a huge amount if you're already waiting
a minute or so per-frame to process a heavy point cloud (like a big FLIP sim).
But consider that in this example we are writing just a *single* attribute, in
*one* wrangle. In a real-world setup, you might have several attributes and be
doing a few different things in different wrangles and steps which can really
add up!


## Volumes

This technique is *especially* useful when dealing with fields in Volume VOPs.
Have you ever dived inside a **Gas Turbulence DOP** or any similar nodes? If you
look in the Attribute Bindings section, you'll see that SideFX uses these all
the time! It's how you're able to specify the name of any **Control Field**, but
internally they only need to use one name!

Let's try it out on our own. We'll create a Volume VOP that adds noise to both
`density` and `temperature`. There's actually a shortcut toggle we can use
without needing to set all the names ourselves.


[![Bind Each to Density]({{ images }}/bind-each-to-density.png)]({{ images }}/bind-each-to-density.png)

[![Volume Bindings]({{ images }}/volume-binding-demo.gif)]({{ images }}/volume-binding-demo.gif)

1. Create a Volume VOP.
2. Add some nodes inside. Don't add any extra **Bind Export** nodes, just pipe
   them out to `density`.
3. On the **Volume Bindings** tab uncheck **Autobind by Name**.
4. Enable **Bind Each to Density**.

Now we've applied the same operation to all of the fields! This is really useful
if you're creating any tools that modify volumes, and you want the user to be
able to easily run over fields called anything.

## Attributes to Create

[![Attributes to Create - Default]({{ images }}/attribs-to-create-default.png)]({{ images }}/attribs-to-create-default.png)

This parameter is often overlooked, and its default is just `*` - which means
any attributes referred to in the wrangle using the `@` syntax will be created
if it they don't exist already.

The default is usually fine. But sometimes, you might be using an attribute
temporarily just to do some sort of calculation, and you don't actually want it
to be created and passed along through the output. In that case, you can just
use the `^` character plus the attribute name to skip it! This is also useful if
you have a tool that *allows* a user attribute to passed in but does not *require*
it.

Take this for example:

![]({{ images }}/attribs-to-create-scenario.mp4)
<video width="720" height="405" autoplay loop>
	<source src="{{ images }}/attribs-to-create-scenario.mp4" type="video/mp4">
</video>

We have a setup that modifies the thickness of some curves. By default, the code
will apply some randomness. The user is also given the option to provide an
attribute by which to multiply the randomized thickness. For clarity, let's
provide them a sensible default like `thicknessscale` (sort of how vellum and
other tools across houdini fill it in too).

[![Parameter Defaults and Code]({{ images }}/parm-defaults-and-code.png)]({{ images }}/parm-defaults-and-code.png)

If we structure our code like so:

```c
float r = rand(@seed + 65536);

f@pscale = r * f@scale * chf("global_scale");
```

with the following attribute bindings:

[![Attribute Bindings]({{ images }}/attribs-to-create-attrib-bindings.png)]({{ images }}/attribs-to-create-attrib-bindings.png)

we would expect that the `f@pscale` attribute is scaled by some random number,
and the curves will change shape.


But what happens if the user doesn't want to do any extra scaling, and they
didn't specify any attribute? If no attribute is provided, and the binding is
left blank or the attribute doesn't exist we wind up with a bit of an issue...


[![Scales are Zero]({{ images }}/zero-scales.gif)]({{ images }}/zero-scales.gif)

All the scales are now zero! Well that's not really what we want... if the user
doesn't specify an attribute (or if it doesn't exist), we should carry on and
happily apply just the randomized value to the thickness. Let's modify the code a bit:


```c
float @scale = 1.0; // Initialize it in case the user doesn't

float r = rand(@seed + 65536);

f@pscale = r * @scale * chf("global_scale");
```

[![Scales Working]({{ images }}/scales-working.gif)]({{ images }}/scales-working.gif)

This works excellently! Now, even though the attribute is missing, everything
is just multiplied by `1.0`, so we're in the clear. But let's look at the
attributes now...

[![Extra Attribute]({{ images }}/extra-attrib.png)]({{ images }}/extra-attrib.png)

Oh no! Since that default value we have sitting in there wasn't cleared out, and
since it doesn't already exist on the points, we wound up creating some
attribute called `thicknessscale` with a value of `1.0`! That's sort of
annoying. If the user didn't ask for an attribute to be created, we should
really just leave it alone.

Leaving it alone is simple. Just exclude it from that **Attributes to Create**
parameter.

[![Exclude f@scale Attribute]({{ images }}/exclude-attribs.png)]()

```
* ^scale ^seed
```

> The attributes specified in this list are the same as the *Vex Parameters*
> you're using in your code, even if they are *bound* to something different.


[![No Extra Attributes]({{ images }}/no-extra-attrib.png)]({{ images }}/no-extra-attrib.png)


If the attribute *does* exist on the points beforehand, don't worry - this
option won't cause it to be deleted. It will still pass through just as expected,
with the added bonus that since it's being ignored in the **Attributes to
Create** parameter, we aren't able to actually write to it, which means we can't
muck it up with our code!

### Result

Let's see it in action with the user specifying their own scaling attribute on
top of our randomization:

[![Final Result]({{ images }}/custom-attrib.gif)]({{ images }}/custom-attrib.gif)


## Final Notes

### Groups

We can do most of the same stuff with groups. Just remember than Vex expects the
prefix `i@group_` before group names, which also applies to the **Vex Parameter** parameter
in the bindings section.

[![Group Bindings]({{ images }}/group-bindings.png)]({{ images }}/group-bindings.png)

[![Group Bindings Example]({{ images }}/group-bindings-example.png)]({{ images }}/group-bindings-example.png)

An important note - if you're using the **Output Selection Group** parameter to
visualize the group in the viewport (and pass the selection to downstream
nodes), note that this parameter is expecting ***Group Name*** not the **Vex
Parameter**!

[![Output Selection Group]({{ images }}/output-selection-group.gif)]({{ images }}/output-selection-group.gif)
