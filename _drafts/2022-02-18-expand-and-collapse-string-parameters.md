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
