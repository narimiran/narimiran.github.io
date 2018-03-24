---
layout: post
title: Double pendulum chaos
date: 2018-03-24
---


Pendula have fascinated people for centuries.
Probably the most famous pendulum is [Foucault's pendulum](https://en.wikipedia.org/wiki/Foucault_pendulum), which was used to demonstrate Earth's rotation.

In the first part of this post we will scratch the surface of the mechanics behind the pendulum movement and show the equations needed to solve these problems numerically.
The second part contains several video examples of pendula movement.

If you want to skip the mathematical part and go straight to the videos, [click here](#animations).




## Simple pendulum

![Simple gravity pendulum](/figures/pendulum/pendulum.svg){: .center-image}

A simple gravity pendulum is a well-known idealized mathematical model of a real pendulum.
It consists of a massless incompressible rod with one fixed end and a point mass on the other end.
It is a frictionless system oscillating at a constant frequency.


### Polar coordinates

![Polar coordinates](/figures/pendulum/polar.svg){: .center-image}

The equation of motion of a simple pendulum, obtained from free body diagram and mass-acceleration diagram, is

$$
\ddot \theta + \frac{g}{l} \sin \theta = 0
$$

where $$\theta$$ is the angle from the vertical, $$\ddot \theta$$ is the angular acceleration, $$g$$ is the acceleration of gravity, and $$l$$ is the length of the pendulum.



### Cartesian coordinates

![Cartesian coordinates](/figures/pendulum/cartesian.svg){: .center-image}

If the same problem is rewritten in Cartesian coordinates, an additional algebraic constraint is needed

$$
f (x, y) = x^2 + y^2 - l^2 = 0
$$

which describes the orbit of the free end of the pendulum, i.e. it means the length of a rod must remain a constant.

From the Lagrangian of the system ($$L = T - V$$, where $$T$$ and $$V$$ are kinetic and potential energy, respectively), using [Lagrange's equations of the first kind](https://en.wikipedia.org/wiki/Lagrangian_mechanics) we obtain [equations of motion](https://en.wikipedia.org/wiki/Equations_of_motion)

$$
\begin{align}
    m \ddot x &= - 2 x \lambda \\
    m \ddot y &= - m g - 2 y \lambda \\
    % 0 &= x^2 + y^2 - l^2
\end{align}
$$

where $$m$$ is the mass, $$\ddot{x}$$ and $$\ddot{y}$$ are the accelerations in $$x$$ and $$y$$ directions (measured from the fixed end of the pendulum) respectively, and $$\lambda$$ is the [Lagrange multiplier](https://en.wikipedia.org/wiki/Lagrange_multiplier).





## Double pendulum

A double pendulum is made by attaching another pendulum to the free end of a simple pendulum.
In our examples, the motion is still restricted to the vertical plane, and rods are massless with point masses on their ends.

![Double pendulum](/figures/pendulum/double_pendulum.svg){: .center-image}

In this situation two algebraic constraints are needed

$$
\begin{align}
    f_1 &= x_1^2 + y_1^2 - l_1^2 = 0 \\
    f_2 &= (x_2 - x_1)^2 + (y_2 - y_1)^2 - l_2^2 = 0
\end{align}
$$

describing the orbits of both masses, while the lengths of the rods remain constant.

Now the equations of motion are

$$
\begin{align}
    m_1 \ddot{x_1} &= 2 (\lambda_1 + \lambda_2) x_1 - 2 \lambda_2 x_2 \\
    m_1 \ddot{y_1} &= 2 (\lambda_1 + \lambda_2) y_1 - 2 \lambda_2 y_2 - m_1 g \\
    m_2 \ddot{x_2} &= - 2 \lambda_2 x_1 + 2 \lambda_2 x_2 \\
    m_2 \ddot{y_2} &= - 2 \lambda_2 y_1 + 2 \lambda_2 y_2 - m_2 g.
\end{align}
$$

This can be solved numerically.
In our case, we have used [_the_ Runge-Kutta 4](https://en.wikipedia.org/wiki/Runge–Kutta_methods#The_Runge–Kutta_method) method to calculate values at each time step, which was taken as 0.001 s.







## Animations



### How to read the graphs

The graphs shown in this section have three parts.

The main part is the view of pendula as they swing in the vertical plane.
In all the graphs there are two pendula: a blue one with a larger mass(es) at its end(s), and an orange one with a smaller mass(es) --- the size of a circle is proportional to the mass.

The other parts of a graph are [phase plane](https://en.wikipedia.org/wiki/Phase_plane) plots.

Under the main part is a plot of a relation between a position (on a horizontal axis) and a velocity (on a vertical axis) in x-direction of each pendulum's "bottom" mass.

On the right side is a similar plot of positions (on a vertical axis) and velocities (on a horizontal axis) in y-direction.




### Single pendulum

First it will be shown how two single pendula of different masses swing.

The length of both pendula is 2.5 m.
The blue one has a mass of 5 kg and it is released from a position (1.50 m, -2.00 m).
The orange one has a mass of 2.5 kg and it starts from 10 cm smaller incline (1.40 m, -2.07 m).

<video width="700" height="700" controls="controls">
<source src="/figures/pendulum/01-single-down.mp4" type="video/mp4">
</video>

There are several things to notice here:

1. Even though the blue pendulum has twice the mass of the orange one, they seem to have quite similar periods and frequencies of oscillation.
2. The small difference in the periods of oscillation (by the end of the video the blue pendulum is slightly lagging behind the orange pendulum) is the result of releasing them from a bit different initial positions. For a smaller incline, these differences would be negligible (see [small angle approximation](https://en.wikipedia.org/wiki/Pendulum_(mathematics)#Small-angle_approximation)).
3. Looking at the phase plane plots, we see that each swing is the same as the previous (in our calculations, friction and air resistance are ignored).

Taking all that into account, a single pendulum is quite boring.
Let's see if the situation is improved with double pendula.



### Double pendulum

One of the first things you can read about [double pendula on Wikipedia](https://en.wikipedia.org/wiki/Double_pendulum) is that they are chaotic.
In the next couple of examples, we will try to explain what that means.

The first example are the single pendula from the previous example (the same length, masses, and initial positions) that have another pendulum of the same characteristics attached to their end, starting from a horizontal position.

<video width="700" height="420" controls="controls">
<source src="/figures/pendulum/02-double-down.mp4" type="video/mp4">
</video>

The behaviour of these two pendula is a bit different, but still quite similar to each other.
Phase plots are not as "tidy" as in the case of single pendulum, but there is a clearly visible regularity.

Shouldn't double pendula be chaotic?

Well, for small enough initial angles, double pendula behaves similarly to the single pendula, and the chaotic nature is not pronounced.



### Chaos

Things change dramatically for double pendula released from a larger initial angle.

Take the previous example and mirror it --- now the starting positions are above the fixed point.
All other properties remain the same as before.

<video width="700" height="560" controls="controls">
<source src="/figures/pendulum/03-double-up.mp4" type="video/mp4">
</video>

Even before the pendula have reached their left-most position for the first time we can observe the clear differences in their behaviour.
Phase plots are significantly different.

So we have found the initial positions for which different behaviours can be observed.
But how large is this chaos-effect?

Let's now take two almost identical pendula --- the only difference between them is that the orange one has its rod connecting it to the fixed point 1 milimeter (0.001 m) longer.
The difference in the length between the blue and orange rod is only 0.04 %.

<video width="700" height="560" controls="controls">
<source src="/figures/pendulum/04-small-diff.mp4" type="video/mp4">
</video>

For the first three seconds of the animation, both pendula behave as one (in all three graphs only the orange color is seen).
After three more seconds, they are in completely different positions, like they have never "been together".

This is a true example of chaotic behaviour --- even a very small difference in initial conditions leads to large differences later on.




## Conclusions

A single pendulum has a very predictable motion --- if you know the rod length, you can very simply and relatively accurately predict where it will be at any point in time.

A double pendulum released from a small initial angle behaves similarly to the single pendulum.
On the other hand, releasing it from a large enough initial angle will produce chaotic behaviour which is impossible to predict.

If you would like to see more of chaotic double pendula, take a look at my [double pendulum bot](https://twitter.com/pendulum_bot/) on Twitter.
