# 12 · Testen en debuggen

## Test je controller

Op deze site kun je makkelijk je gamepad testen: <https://hardwaretester.com/gamepad>

Stuurt je controller toetsen? Open dan een leeg tekstbestand en druk op je knoppen.

## Werkt het niet?

- Controleer de code stap voor stap en probeer het opnieuw.
- Herkent de computer je bord als USB-apparaat?
- Kloppen de pinnen in je code met de pinnen waarop je de draadjes hebt aangesloten?
- Raken draadjes op het breadboard elkaar, of zitten ze in dezelfde rij? (zie [het breadboard](../05-drukknop/README.md#het-breadboard))

## Micro:bit

Reageert de Micro:bit niet op je code? Download de `.hex` opnieuw en kopieer hem naar de Micro:bit (zie [stap 03](../03-eerste-code/README.md#code-flashen-hoe-zet-je-de-code-op-de-microbit)).

## RP2040-Zero

De voorbeelden printen wat ze doen (`press. button: …`, `x … y …`). Die tekst zie je in de seriële console van <https://code.circuitpython.org/>.

## Arduino

The examples print their readings with `Serial.print()`. Open the **Serial Monitor** in the Arduino IDE (9600 baud) to see what your sensors are doing.

---

← [Code: je controller programmeren](../11-code/README.md) · [Overzicht](../../README.md) · [Tinkercad: ontwerp je behuizing](../13-tinkercad/README.md) →
