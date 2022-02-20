---
layout: post
title: Expand/Collapse String Parameters
shortname: expand-and-collapse-string-parameters
description: Hacky setup to get expandable/collapsible text input fields
thumbnail: /assets/posts/expand-and-collapse-string-parameters/images/preview.png
categories: tips
tags: parameter interface string collapse expand python ui
---

> Hipfile: [jamesr_expandandcollapsestringparameters.hip](/assets/posts/expand-and-collapse-string-parameters/jamesr_expandandcollapsestringparameters.hip)
{:style="border-color: #d08770"}

{% capture images %}/assets/posts/{{ page.shortname }}/images{% endcapture %}

[![Cover Photo]({{ page.thumbnail }})]({{ page.thumbnail }})

# Overview
In a recent tool I was making, I wanted the option to switch between a single
line string parameter (the default), and a larger input field.

[Gif of switching between the two]

This could be done on a single parameter by messing around with the Parameter
Template, but a) that's always a bit of a faff and b) won't work for multiparms
when you might only one one string collapsed and the others expanded.

In this post, I'll walk through setting this up using *two* string parameters,
an invisible toggle, and some Action Buttons. We'll start by building it on a
single string parameter, and finish by seeing how we can add it to a multiparm
block. Let's get started!



The trick is

When you set a parameter in Houdini using *Python*, there are a couple ways of
going about it.

Remember that Python is an object-oriented language, and that everything you
deal with is an "object". In Houdini, we deal with parameters using hou.Parm.
When you instantiate a hou.Parm object using something like

```python
parm = hou.node("/obj/mynode").parm("someparm")
```
Houdini isn't going to give you the *value* of that parameter, but rather a
parameter *object*. This is quite powerful, because with the parameter object,
we can do a whoooole bunch of stuff with parameter like ask it about itself,
evaluate it, and so on.

When you *set* a parameter in Python in houdini, generally you'll use
hou.Parm.set() to set it to some literal value, like a float parm `4.0`
or a string parm `Hey there buddy`. If you're referencing this value from
another parm, you will have used hou.Parm.eval() to get the value first before
setting it on the target parameter.

But a really cool feature of setting parameters use Python is that if instead of
first *evaluating* the source parameter before setting the target parameter, you
pass the actual *parameter object* to hou.Parm.set(). This will create a ch() or
chs() channel reference to that source parameter automatically! This makes it
really easy to set up relative references just by passing parms to other parms.

hou.node("/obj/somenode").parm("someparm").set(hou.node("/obj/othernode").parm("otherparm"))

now you havea relative reference.

We are going to use this feature to make sure that our two string parameters are
always staying in sync. When we hit the expand/collapse button, instead of
evaluating the string, storing a copy of it, then replacing the parameter with
our stored value, let's just let Houdini take care of that itself. Whenever we
toggle the **Expand** checkbox, we want to create a relative reference from one
string to the other, and delete the previous relative reference if it existed.
See the following gif:

[gif of switching between]



So how will we switch between two string parameters without having to retype or
copy/paste the contents every time? Let's consider that our parameter is
currently "Collapsed". One approach would be:

1. Copy the contents of the collapsed string parameter when we hit **Expand**
2. Paste the copied text into the expanded string parameter
3. Show the expanded string parameter
4. Hide the collapsed string parameter

This would probably work, and wouldn't be too hard to implement. However, one
major drawback to this is that the two parameters are never in sync. Ideally,
they have the exact same contents, and all we're changing is the UI (as we know,
this isn't really possible in our scenario, so we're hacking it a bit). Consider
what would happen if you referenced the **Expanded** parameter, but made some
changes while it was collapsed. In order to have the latest changes in your
referenced parameter, you'd have to made sure to toggle the string
expanded/collapsed in order to update it.

Let's consider a slightly better approach. We can just use channel referencing
to make sure our string parameters are always in sync:
1. Set default value for **Expanded** to be `chs("note_collapsed")`
2. When we toggle the **Expand** checkbox, break the reference to
   `note_collapsed`. Doing this will automatically replace the reference with
   the actual literal value.
3. Set a channel reference on `note_collapsed` to `chs("node_expanded")`. Now
   the collapsed string will refernce whatever updates we make while expanded.

