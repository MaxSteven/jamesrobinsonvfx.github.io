---
layout: post
title: ftrim() HScript function
description: Trim unwanted digits from parameter values
thumbnail: /assets/posts/ftrim-function/images/preview.png
categories: tips
tags: houdini hscript
---

> Hipfile: [jamesr_ftrim.hip](/assets/posts/ftrim-function/jamesr_ftrim.hiplc)

{:.toc}
- [Problem](#problem)
- [Fix](#fix)

### Problem
Sometimes you want to reference the value of a parameter and display it as a
string to put in a Font SOP, or the [Viewport
Comment](2012-02-07-example-content.md) of a Camera node when you're wedging
sims or making some sort of visualizer.

But quite often, if you're referencing a `float` parameter, you wind up getting
allllll the digits that come with it, imprecision and all, rather than just a
nice float

![Problem](/assets/posts/ftrim-function/images/problem.png)

ie.
```
0.04
```
becomes
```
0.040000000000000001
```
which is probably *not* what you want!

A possible solution to trim off some of the rounding error might look something like

```
floor(ch("/some/parm") * 1000)/1000
```
Unfortunately, this fails too :(

### Fix

The solution is actually quite simple! We can use the `ftrim()` function from
HScript. `ftrim()` will strip off all those unwanted digits and leave you with a
nice clean value, pretty much as you typed it!

![Solution](/assets/posts/ftrim-function/images/solution.png)

Of course, this also works in a **Font SOP** too.

![Font SOP](/assets/posts/ftrim-function/images/font-sop.png)