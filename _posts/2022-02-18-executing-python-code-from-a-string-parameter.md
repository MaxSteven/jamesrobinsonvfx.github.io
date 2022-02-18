---
layout: post
title: Executing Python Code From A String Parameter
shortname: executing-python-code-from-a-string-parameter
description: Create a preset on a Null that lets you run Python code from it
thumbnail: /assets/posts/executing-python-code-from-a-string-parameter/images/preview.png
categories: tips
tags: houdini ui python
---

> Hipfile: [jamesr_executingpythoncodefromastringparameter.hip](/assets/posts/executing-python-code-from-a-string-parameter/jamesr_executingpythoncodefromastringparameter.hip)
{:style="border-color: #d08770"}

{% capture images %}/assets/posts/{{ page.shortname }}/images{% endcapture %}

[![Cover Photo]({{ page.thumbnail }})]({{ page.thumbnail }})

# Overview

Sometimes you just want to run some python code, but don't want to run
line-by-line in the Python Shell, can't be bothered to create a shelf tool, and
don't need to run over geometry (so the Python SOP is out). Luckily it's really
easy create a simple preset that lets us run some Python code from a string
parameter.

This is useful for creating small scripts to run in your scene, debug stuff,
prototype some code, and even for creating code for parameter callbacks on the
fly without needing to write your code to disk, or embed into an HDA.

> This method uses Python's `exec` function, and can be used to run arbitrary code. Use with caution...

# Setup

##