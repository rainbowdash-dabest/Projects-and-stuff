# Analog Electronics

Started experimenting with random circuits Summer '26 trying to figure out how stylophones work, and wound up stumbling my way through Scherz's *'Practical Electronics'* for these shenanigans.

Ongoing project: NE555-VCO

Below are:
1. A Falstad model of an exponential coverter modulating a NE555 stylophone as an induced VCO.

<p align="center">
  <span style="display: inline-block; width: 80%; vertical-align: top; text-align: center;">
    <img src="analog_VCO-Stylophone/Falstad/modulation.gif" width="100%" />
    <small>Overall Circuit</small>
  </span>
</p>

2. A LT spice config of different mono-BJT exponential converters
<p align="center">
  <span style="display: inline-block; width: 80%; vertical-align: top; text-align: center;">
    <img src="analog_VCO-Stylophone/LT_Spice/anti-log_viability_chart.png" width="100%" />
    <small>LT SPICE simulating exp_converters</small>
  </span>
</p>

3. A [plot](https://www.desmos.com/calculator/tbxkukw6fq) experimentally testing the exponential converter on a 2N2222-LM358
<p align="center">
  <span style="display: inline-block; width: 80%; vertical-align: top; text-align: center;">
    <img src="analog_VCO-Stylophone/Falstad/experimental plot(Vout vs Vin).png" width="100%" />
    <small>experimental plot(Vout vs Vin)</small>
  </span>
</p>

4. Breadboard circuit of a simple stylophone.
<p align="center">
  <span style="display: inline-block; width: 80%; vertical-align: top; text-align: center;">
    <img src="analog_VCO-Stylophone/breadboard_photos/basic_stylophone.jpeg" width="32%" />
    <img src="analog_VCO-Stylophone/MATLAB(trial)/NE555_astable_run.png" width="67%" />
    <small>basic stylophone with MATLAB chart</small>
  </span>
</p>

