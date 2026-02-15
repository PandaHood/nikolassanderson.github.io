---
layout: page
permalink: /repositories/
title: open source
description:
nav: false
nav_order: 3
---

Here are a few open source projects I've developed and shared for others to use,
extend, and compare against. As of now, most of my software centers around my
research in SLAM, but occasionally other side projects sneak in.

{% if site.data.repositories.github_repos %}
<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.html repository=repo %}
  {% endfor %}
</div>
{% endif %}
