---
layout: post
title: Wildcarding For Camelcase
shortname: wildcarding-for-camelcase
description: Accurately search for sub-strings even if the source is camelCase
thumbnail: /assets/posts/wildcarding-for-camelcase/images/preview.png
categories: tips
tags: houdini code camelCase wildcard searching
---

> Hipfile: [jamesr_wildcardingforcamelcase.hip](/assets/posts/wildcarding-for-camelcase/jamesr_wildcardingforcamelcase.hip)
{:style="border-color: #d08770"}

{% capture images %}/assets/posts/{{ page.shortname }}/images{% endcapture %}

[![Cover Photo]({{ page.thumbnail }})]({{ page.thumbnail }})

As some people might know I *really* dislike camel case for a myriad reasons,
not the least of which is the lack of being able to accrurately extract
substrings and search for stuff with wildcards. Take the following model for
instance:

SOME MODEL


pants - button
shirt - collarButton, shirtButton
*utton

tire