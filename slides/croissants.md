---
marp: true
theme: slides
size: 16:9
paginate: true
math: true
---

<!-- _paginate: false -->

<!-- ![bg blur:3px opacity:20%](https://raw.githubusercontent.com/bdpedigo/talks/main/docs/images/background.svg) -->

![bg right](./images/person.jpg)

<style scoped>
p {
    font-size: 24px;
}
</style>

# Le Tournoi des Croissants 2024

##### Ben Pedigo

(he/him)
Croissant Analyst II
Allen Institute for Pastry Science

![icon](https://raw.githubusercontent.com/bdpedigo/talks/main/docs/images/icons/email.png) [ben.pedigo@alleninstitute.org](mailto:ben.pedigo@alleninstitute.org)
![icon](https://raw.githubusercontent.com/bdpedigo/talks/main/docs/images/icons/github.png) [@bdpedigo (Github)](https://github.com/bdpedigo)
![icon](https://raw.githubusercontent.com/bdpedigo/talks/main/docs/images/icons/twitter.png) [@bpedigod (Twitter)](https://twitter.com/bpedigod)
![icon](https://raw.githubusercontent.com/bdpedigo/talks/main/docs/images/icons/web.png) [bdpedigo.github.io](https://bdpedigo.github.io/)

---

# By the numbers

![bg right](./images/map.png)

- 18 bakeries
- 16 weeks
- 180 croissants ranked

---

![center h:600](./images/votemap.svg)

---

# Voter-voter agreement

$*$ only computed for >= 5 votes

![bg right h:600](./images/agreements_no_labels.svg)

---

# Null voting model

- Preserve overall preference for each bakery at each week
- Randomize votes among voters that were present at that week

<div class="columns">
<div>

![](./images/null_0.svg)

</div>
<div>

![](./images/null_1.svg)

</div>
<div>

![](./images/null_2.svg)

</div>
<div>

![](./images/null_3.svg)

</div>
<div>

![](./images/null_4.svg)

</div>
</div>

<div class="columns">
<div>

![](./images/null_5.svg)

</div>
<div>

![](./images/null_6.svg)

</div>
<div>

![](./images/null_7.svg)

</div>
<div>

![](./images/null_8.svg)

</div>
<div>

![](./images/null_9.svg)

</div>
</div>

---

# Null suggests no significant agreement

![center h:500](./images/agreement_histogram.svg)

---

# Do you know your bestie?

![bg right h:600](./images/agreements.svg)

$*$ only computed for >= 5 votes

<style scoped>
p {
    font-size: 20px;
}
</style>

Ben's bestie is Derrick (agreement 0.83)
Bethanny's bestie is Xiaoyu (agreement 0.75)
Forrest's bestie is Rachael (agreement 0.83)
Jenna's bestie is Rachael (agreement 0.83)
Kim's bestie is Jenna (agreement 0.79)
Marc's bestie is Xiaoyu (agreement 0.88)
Nuno's bestie is Rachael (agreement 0.80)
Chi's bestie is Nuno (agreement 0.78)
Keith's bestie is Kim (agreement 0.70)
Cameron's bestie is Rachael (agreement 0.80)
Xiaoyu's bestie is Marc (agreement 0.88)
Rachael's bestie is Marc (agreement 0.86)
Derrick's bestie is Ben (agreement 0.83)

---

# Croissant preference space

![center h:550](./images/mds.svg)

---

# Are you a tastemaker?

Proportion of "correct" votes

<style scoped>
p {
    font-size: 20px;
}
</style>

Jenna       0.866667
Rachael     0.857143
Nuno        0.750000
Forrest     0.733333
Kim         0.733333
Cameron     0.700000
Ben         0.687500
Derrick     0.666667
Marc        0.642857
Xiaoyu      0.555556
Chi         0.545455
Keith       0.545455
Bethanny    0.533333

