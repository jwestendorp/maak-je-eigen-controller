# 07 · Bedenk je eigen input signaal

Anything can be an input for a controller! As long as it can be perceived by our Arduino as either an analog or a digital signal.

## Arduino libraries

We can use external packages to have our Arduino interpret the signals of some more complex electrical components. Some nice people on the internet have already done most of the work for us and published functions we can use to interface with other hardware. More examples: <https://github.com/softpack6ix/shapeshifters-winterschool/tree/main?tab=readme-ov-file#code-examples>

## Examples

| Example | Sensor | Sends |
| --- | --- | --- |
| [touch](./arduino/touch/touch.ino) | 2× TTP223 touch sensor | Mouse: moves the cursor left/right |
| [infrared-remote](./arduino/infrared-remote/infrared-remote.ino) | IR receiver + any remote (library: *IRremote*) | Keyboard: types the received code |
| [motion-sensor](./arduino/motion-sensor/motion-sensor.ino) | PIR motion sensor | Serial only, a starting point |
| [vape](./arduino/vape/vape.ino) | Puff/airflow switch | Keyboard: types "inhale", `*` while puffing, "exhale" |

All examples except the IR remote only need *HID-Project* (see [04-bord-opzetten](../04-bord-opzetten/README.md#arduino)).

---

← [Breadboard: prototype potmeter (analoog)](../06-potmeter/README.md) · [Overzicht](../../README.md) · [Schets je controller en pitch je idee](../08-schetsen-pitch/README.md) →
