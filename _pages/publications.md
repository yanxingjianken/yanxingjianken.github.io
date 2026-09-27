---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
redirect_from:
  - /software/
  - /software.html
---

{% if site.author.googlescholar %}
  <div class="wordwrap">You can also find my articles on <a href="{{site.author.googlescholar}}">my Google Scholar profile</a>.</div>
{% endif %}

{% include base_path %}

<h2 class="archive__subtitle" id="papers">Papers</h2>

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}

<hr class="pubs-software-divider" style="border:0;border-top:1px solid #bbb;margin:2.5em 0 1.5em 0;">

<h2 class="archive__subtitle" id="software">Software</h2>

{% for post in site.software reversed %}
  {% include archive-single.html %}
{% endfor %}
