## ANALOG VCO - Stylophone
*[In progress]*

An [analog exponential converter and op amp system](https://www.falstad.com/s.php?s=r9WHL7) that turns a NE555 into a multi-octave switching VCO with a stylophone input and simple amp output.

<p align="center">
  <span style="display: inline-block; width: 80%; vertical-align: top; text-align: center;">
    <img src="Falstad/modulation.gif" width="100%" />
    <small>Voltage controlled-Frequency Change in overall circuit</small>
  </span>
</p>

I wanted to make a stylophone and the [fist NE555 model](https://www.instructables.com/A-Stylophone/) I saw had a pretty big (though not complicated) restriction. Since music scales exponentially, the resistor ladder that dictates the frequency modulation has to be non-linear.

What that means is that you need to design a separate circuit for every octave, and since i wanted to have a single set of notes which i could electronically move up and down, I was dissatisfied.
(+ I didn't have enough resistors for a stable dual octave).

So, I went ahead and designed a way to take a voltage from a ladder, feed it through a couple converters and op amps to get the input i want and turn the ne555-timer into a makeshift VCO. It might not match the EU Standard of 1V/octave (yet), but it allows for octave switching completely from the powered input wire, though the current iteration a bit temperature unstable without a thermistor.

<p align="center">
  <span style="display: inline-block; width: 80%; vertical-align: top; text-align: center;">
    <img src="LT_Spice/anti-log_viability_chart.png" width="100%" />
    <small>LT SPICE simulating exp_converters</small>
  </span>
  <br>
  <span style="display: inline-block; width: 80%; vertical-align: top; text-align: center;">
    <img src="breadboard_photos/basic_stylophone.jpeg" width="38%" />
    <img src="MATLAB(trial)/NE555_astable_run.png" width="59%" />
    <small>basic stylophone with MATLAB chart</small>
  </span>
</p>

Currently [testing](https://www.desmos.com/calculator/tbxkukw6fq) on-hand chips, but otherwise ready for assembly.
<p align="center">
  <span style="display: inline-block; width: 70%; vertical-align: top; text-align: center;">
    <img src="Falstad/experimental plot(Vout vs Vin).png" width="100%" />
    <small>experimental plot(Vout vs Vin) 2N2222-LM358 antilog</small>
  </span>
</p>

#### Software:
LT Spice, Falstad, MATLAB (coz why not), Fusion 360.