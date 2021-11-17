# README

## About

This is a custom chording engine. See butterstick:tomas keymap for an example use.

Pure QMK combos were not sufficient as they do not really support overlapping combos. For example. if you define 3 combos `(KC_Q, KC_W)`, `(KC_Z, KC_X)` and `(KC_Q, KC_W, KC_Z, KC_X)` and press Q, W, Z and X at the same time, all three combos will activate. The default butterstick keymap solves this by relying on modified stenografic engine. However, this doesn't allow for comfortable typing in the traditional way. The steno chord activates only when *all* keys are lifted and makes it difficult to implement some advanced features.

To use it, you will need a general purpose preprocessor [pyexpander](http://pyexpander.sourceforge.net/). The reason behind general purpose preprocessor is abstraction when defining the keymap. Every function on this keymap is a chord (combo). Meaning you have to follow syntax similar to pure QMK combos. Furthermore you can not use functions to generate these since you want to store them in PROGMEM. The resulting keymap file is long, difficult to navigate and even more difficult to modify. It is *nearly impossible* to write C preprocessor macros that make it as easy as pure QMK keymap. The general preprocessor makes it relatively easy. Since I use it heavily and since you will be modifying the code for the preprocessor and not the C code, the code is written to be well formatted in the file `keymap.c.in` and *not to produce pretty C code* in `keymap.c`. My `keymap.c` ends up over 7000 lines long and more than half whitespace. To produce C code from the `keymap.c.in` file, run

```sh
python3 expander3.py -f keymap.c.in > keymap.c
```

If you want to have a nice `keymap.c`, use some linter or formatter. I like `indent`:

```sh
indent keymap.c -bad -bap -bbb -br -brf -brs -ce -i4 -l100 -nut -sob
```

I just broke it on my system somehow, so my current `keymap.c` is a mess.

Thanks to the provided macros, you shouldn't have to modify any file except `keymap.c.in`. If you are using a different keyboard, you will have to also create your own `keyboard.inc`.

## Features Overview

The chording engine completely sidesteps QMK's key event processing. Most of QMK's features are reimplemented. A list with short description follow, examples and further details follow later in this README.

### Chords

Once again, *everything* on this keymap is a chord. Even sending `KC_Q` is done by pressing a single key chord. Chord gets activated after all it's keys get pressed. Only the longest chord gets activated. The order of the pressed keys *does not matter*, only the fact they have been pressed within the same time frame. An active chord gets deactivated if *any* of it's keys gets depressed. To activate the same single chord again, *all* it's keys have to be depressed and pressed again. With a few exceptions chords are independent of each other. No matter if some chords are currently active and some not, others can be activated or deactivated without affecting each other's state.

### Tap-Dance

To make it even stranger, all chords are tap-dance chords. They are relatively simple state machines that execute a specific function every time they change state. For simplicity and optimization purposes, there are a few prewritten functions that implement common features like "send a single key" or "lock". Any number of chords can be "in dance" at any given moment without affecting each other's state. Custom dances can be easily added.

### Pseudolayers

Only one QMK layer is used. Following the butterstick's default keymap's example, the chording engine is using pseudolayers. The main difference to QMK's layers is that only one pseudolayer can be active at each time (meaning you can not use `KC_TRANS`, I actually don't know what will happen). Chords can be activated only if they are on the currently active pseudolayer. Chords that are currently active do not get deactivated if the pseudolayer changes and will deactivate if any of their keys gets depressed even no matter the current pseudolayer. Locked chords (see below) and chords on the `ALWAYS_ON` pseudolayer can be activated anytime.

### Lock

Similarly to QMK's lock, the next chord activated after the Lock chord will not deactivate on release of any of its keys, it will deactivate when all its keys get pressed again. Any number of chords can be locked at the same time. To make sure a locked chord can be unlocked, it can activate no matter the current pseudolayer. A chord can be locked mid dance.

### One shots

Chords that send keycodes and chords that turn on pseudolayers can be one shots. If tapped, they will lock (stay active) until the next keycode gets sent, *not necessarily when the next chord gets activated*. If held, they will deactivate on release *even if no keycode got sent*.

### Tap-Hold

Also called key-layer dance and key-key dance. Either sends a defined keycode on tap and temporarily switches pseudolayer on hold *or* sends two different keycodes on tap and hold. 

### Command mode

Works similar to the default keymap's. After getting activated for the first time, the keyboard switches to command mode. All *keycodes* that would get registered get buffered instead. After activating the Command mode chord for the second time, all buffered keycodes get released at the same time allowing for key combination that would be hard or impossible to press. The Command mode only affects keycodes. It is therefore possible to change pseudolayers or activate / deactivate other chords while in Command mode. While multiple Command mode chords can be defined, they would not be independent. The keyboard either is or is not in command mode and there is only one buffer.

### Leader key

Just like pure QMK's Leader key, this allows you to add functions that get executed if the Leader key and a specific sequence of keycodes gets registered in a predefined order in a short timeframe. For example `:wq` can send `Ctrl+S` and `Ctrl+W` in a quick succession. While multiple Leader keys can be defined, they all would access the same list of sequences.

### Dynamic macro

A sequence of keycodes can be recorded and stored in the RAM of the keyboard and replayed.

## Examples and Details

### Implementation

The source files are split into three categories. `keymap.c.in` is the main file. In defines all the chords that you wish to use and includes all the other files. `keyboard.inc` file contains all details specific to the board this should be running on -- timings, keys, macros specific to the amount of keys. Finally everything else is in this folder and contains all the definitions, algorithms and macros. Because all the files here are included by the pyexpander, you do not need to worry about adding the user space in your path, as long as in your `keymap.c.in` file is properly defined the `engine_path` variable.

### Keycodes

I do not have experience with stenography, so the the steno keycodes are hard for me to remember. That is why the keymap is using new keycodes TOP1, TOP2, ... TOP9, TOP0, BOT1, BOT2, ... BOT9 and BOT0.

```c
$internal_keycodes("TOP1, TOP2, TOP3, TOP4, TOP5, TOP6, TOP7, TOP8, TOP9, TOP0, BOT1, BOT2, BOT3, BOT4, BOT5, BOT6, BOT7, BOT8, BOT9, BOT0")
```

in `keyboard.inc`. This macro gets expanded and creates the keycodes definitions (starting at `TOP1 = SAFE_RANGE`), creates a single keymaps layer with these keycodes and finally creates `H_TOP1` to `H_BOT0` (or whatever keycodes you define) macros used for defining which keys have to be pressed for each added chord. In my keymap I also define macros for easy adding a large number of chords.

*The chording engine in it's current implementation can handle up to 64 keys. If you need to support more, contact me (email or u/DennyTom at Reddit).*

When `process_record_user()` gets one of the internal keycodes, it returns `true`, completely bypassing keyboard's and QMK's `process_record` functions. *All other* keycodes get passed down. This means you can mix this custom chording engine and your keyboard's default processing, just pass in your keycodes. My `keyboard_macros.inc` is using the `internal_keycodes` macro in to make it easy to define all the internal keycodes, define my only QMK layer, define the smallest type for hashing keys and macros for hashing.

If you want to add more QMK layers or have a mixed layer, you will have to write it manually. To make that easier, you can set `custom_keymaps_array` to `True` and define your own `keymaps[]` array. Your `keymap.c.in` then should look something like this:

```c
...
$py(custom_keymaps_array = True)
$include("keyboard.inc")

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT_butter (TOP1, TOP2, TOP3, TOP4, TOP5, TOP6, TOP7, TOP8, TOP9, TOP0, BOT1, BOT2, BOT3, BOT4, BOT5, BOT6, BOT7, BOT8, BOT9, BOT0),
    [1] = LAYOUT_butter (KC_Q, KC_W, KC_E, KC_R, KC_T, KC_Y, KC_U, KC_I, KC_O, KC_ENT, KC_A, KC_S, KC_D, KC_F, KC_G, KC_H, KC_J, KC_K, KC_L, TO(0))
};
...
```

This would be useful for a gaming layer (even though my chording engine has pretty low latency), or when you want to send advanced keycodes (steno, lights, sounds, etc).

I provide a `TO()` macro that mimics QMK's layer switching `TO()` macro. I would not recommend implementing more complicated QMK layer switching functions unless necessary.

### Chords

Each chord is defined by a constant structure, a function and two non-constant `int` variables keeping the track of the chord's state:

```c
struct Chord {
    uint32_t keycodes_hash;
    uint8_t pseudolayer;
    uint8_t* state;
    uint8_t* counter;
    uint16_t value1;
    uint8_t value2;
    void (*function) (const struct Chord*);
};

uint8_t state_0 = IDLE;
uint8_t counter_0 = 0;
void function_0(struct Chord* self) {
    switch (*self->state) {
        case ACTIVATED:
            register_code(self->value1);
            break;
        case DEACTIVATED:
            unregister_code(self->value1);
            break;
        case FINISHED:
        case PRESS_FROM_ACTIVE:
            break;
        case RESTART:
            unregister_code(self->value1);
            break;
        default:
            break;
    }
}
const struct Chord chord_0 PROGMEM = {H_TOP1, QWERTY, &state_0, &counter_0, KC_Q, 0, function_0};
```

All chords have to be added to `list_of_chord` array that gets regularly scanned and processed. The function doesn't actually activate on all state changes, there are a few more like `IDLE` (nothing is currently happening to the chord) or `IN_ONE_SHOT` (the chord is one shot and is currently locked). Those are all necessary for internal use only. The ones you have to worry about are

* `ACTIVATED`: Analogous to a key being pressed (this includes repeated presses for tap-dance)
* `DEACTIVATED`: Analogous to a key being depressed (also can be repeated)
* `FINISHED`: Happens if the chord got deactivated and then the dance timer expired.
* `PRESS_FROM_ACTIVE`: Happens if the chord was active when the dance timer expired. Meaning you at least once activated the chord and then kept holding it down. Useful to recognize taps and holds.
* `FINISHED_FROM_ACTIVE`:  Happens *after* `PRESS_FROM_HOLD` if the chord is still active when the dance timer expires for the second time. Can be combined with the `counter` to recognize even longer presses. Useful if you want to recognize long presses, for example for autoshift functionality. In `keyboard.inc` you can set `LONG_PRESS_MULTIPLIER` to set how many times does dance timer have to expire for the autoshift to trigger.
* `RESTART`: The dance is done. Happens immediately after `FINISHED` or on chord deactivation from `FINISHED_FROM_ACTIVE`. Anything you have to do to get the chord into `IDLE` mode happens here.

The chords change states based on external and internal events. Anytime a chord's function is activated, it may change it's own state. Also, on certain events, the chording engine will trigger the functions of all chords in a specific state and *if the chords' state hasn't changed* it will then change it appropriately. In this folder is a diagram of the chord's state machine and it's state changes based on external events. The diagram assumes only a single chord, the chord can also be affected by other chords, but that is rare, study the code or contact me for details.

### Macros

The file `macros.inc` contains pyexpander macros that simplify adding the chords. The same chord can be added using this line: `$KC("QWERTY", "H_TOP1", "KC_Q")`.

In my keymap, I also have macros `butterstick_rows` and `butterstick_cols` (in process of getting cleaned up) that allow to add all standard butterstick combos in a syntax similar to QMK's layer syntax:

```c
$butterstick_rows("QWERTY",
    "Q, W, E, R, T, Y, U, I, O, P,\
     A, S, D, F, G, H, J, K, L, ;,\
     Z, X, C, V, B, N, M, ,, ., /")
$butterstick_cols("QWERTY",
    "ESC, , TAB, , O(RGUI), , INS, DEL, BSPC,\
        , ,    , ,        , ,    ,    , ENTER,\
     O(LSFT), O(LCTL), O(LALT), O(NUM), O(LGUI), O(NUM), O(RALT), O(RCTL),  O(RSFT)")
```

The first macro defines single key chords and the logical middle row. The second one defines the logical columns (`TOP1 + TOP2 = KC_ESC`, `TOP9 + TOP0 + BOT9 + BOT0 = KC_ENTER` ).

The arguments have to come in a string so they can be parsed. Not sure if I can work around that. Take a look on how these are implemented, they are using a `$add_key` macro that you can use even if you don't want to use these keyboard specific macros.

You might notice that the macros try to do a few clever things:

* If the keycode would be just a character basic keycode, it tries to allow the use of shortcuts. `Q` will get replaced with `KC_Q`, `,` becomes `KC_COMMA`. *To allow simple string splitting, you have to put a whitespace after the separating commas and no whitespace after the commas you want to expand into `KC_COMMA`.* I will see if I figure out a more flexible solution. This really works only for basic keycodes. However, because of the order of preprocessors you can not use strings defined using `#define` in these strings. Pyexpander substitutions and macros will work:

  ```c
  $py(key1 = "Q")
  $butterstick_rows("QWERTY",
      key1 + ", W, E, R, T, Y, U, I, O, P,\
       A, S, D, F, G, H, J, K, L, ;,\
       Z, X, C, V, B, N, M, ,, ., /")
  ```

* `MO()` and `DF()` macros work the same way for pseudolayers as they would for layers in pure QMK.

* `O()` define a one shot key but it also supports pseudolayers!

* `STR('...')` sends a string. Careful with quoting.

* Special chords like Command mode have their own codes like `CMD`.

* The empty strings `""` get ignored.

These two macros take care of most chords, you need to manually add only chords with non-standard (from butterstick's point of view) keys like `$KC("QWERTY", "H_BOT1 + H_BOT0", "KC_SPACE")`. And that can be done with the `secret_chord` macro (see bellow). I also have a macro for ASETNIOP style layout but that one is much more WIP. Follow it's example to make any more complex chorded input macros.

The complete list of strings that these macros can accept is:

* `KC_X`: Send code `KC_X` just like a normal keyboard. Often the parser will be able to deal even without the `KC_` at the beginning. Basic keycodes and US ANSI shifted keycodes are supported. Most quantum and advanced keycodes *do not*. I will be adding these as needed.

* `STR("X")`: Send string "x" on each activation of the chord. Once again, watch out for quoting and escaping characters. If you want special characters (especially quotes) in your string, look up Python reference for string literals and experiment. Also, because of how the string gets parsed, it is not possible to use `(` in the string. 

* `MO(X)`: Temporary switch to pseudolayer `X`. Because only one pseudolayer can be active at any moment, this works by switching back to the pseudolayer the chord lives on on deactivation. If you chain `MO()`s on multiple pseudolayers and deactivate them in a random order, you might end up stranded on a pseudolayer. I recommend adding `CLEAR` somewhere on `ALWAYS_ON` pseudolayer just in case.

* `DF(X)`: Permanent switch to pseudolayer `X`.

* `TO(X)`: Switches the QMK layer to `X`.

* `O(X)`: One-shot key `X` (if `X` starts with `"KC_"`) or one-shot layer `X` (otherwise) . Both have retro tapping enabled.

* Tap-holds

  * `KK(X, Y)`: Pulses code `X` on tap and code `Y` on hold.
  * `KL(X, Y)`: Pulses code `X` on tap and switches to pseudolayer `Y` on hold. If during the hold no key gets registered, the code `X` will get sent instead (similar to QMK's retro tapping). 
  * `KM(X, Y)`: Same as `KK()` but meant for modifiers on hold. Instead of a timer to figure out tap-hold, uses retro tapping like behavior just like `KL()`.
  * The chording engine determines if you are holding a chord based on a *global* timer. If you start holding a tap-hold chord and very quickly start tapping other chords, the hold might not activate until a short moment *after the last* chord when the timer expires. If you are running into this, adjust timeouts or wait a brief moment after pressing the chord to make sure it switches into the hold state before pressing other chords.

* Autoshift

  * `AS(X)`: Pulses code `X` on tap and Pulses left shift + `X` on hold. 
  * `AT` : Toggles autoshift for all autoshift chords. If off, all `AS` chords act like `KC` chords.

* `LOCK`: The lock key. Since tap-dances of chords are independent, it is possible to lock a chord *anywhere in it's dance if you time it right!*.

* `CMD`: The command mode. The number of keycodes that can be buffered is defined in `keyboard.inc` in `COMMAND_MAX_LENGTH` (works but needs cleanup).

* `LEAD`: The leader key. The maximum length of the sequences needs to be defined in `keyboard.inc`. You can use the `add_leader_combo` macro to add sequences:

  ```c
  void fnc_L1(void) {
      SEND(KC_LCTL);
      SEND(KC_LALT);
      SEND(KC_DEL);
  }
  $add_leader_combo("{KC_Q, KC_Z, 0, 0, 0}", "fnc_L1")
  ```

  This is the only instance the function called is not associated to a chord. That is why the function `fnc_L1` does not accept any inputs.

* `M(X, VALUE1, VALUE2)` A custom macro. Adds a chord that will use function `X` and with `chord.value1 = VALUE1; chord.value2 = VALUE2;`. The function `X` can be arbitrary C function, go crazy. The only constraint is that the function has to follow the same syntax as in the previous example of adding a chord manually. The following example will register a macro that acts exactly like `KC_MEH` (the chording engine *should* support `KC_MEH`, this is just an example):

  ```c
  void fn_M1(const struct Chord* self) {
      switch (*self->state) {
          case ACTIVATED:
              key_in(KC_LCTL);
              key_in(KC_LSFT);
              key_in(KC_LALT);
              break;
          case DEACTIVATED:
              key_out(KC_LCTL);
              key_out(KC_LSFT);
              key_out(KC_LALT);
              break;
          case FINISHED:
          case FINISHED_FROM_ACTIVE:
              break;
          case RESTART:
              key_out(KC_LCTL);
              key_out(KC_LSFT);
              key_out(KC_LALT);
              break;
          default:
              break;
      }
  }
  $butterstick_rows("QWERTY",
      "M(fnc_M1, 0, 0), W, E, R, T, Y, U, I, O, P,\
       A, S, D, F, G, H, J, K, L, ;,\
       Z, X, C, V, B, N, M, \,, ., /")
  ```

  Since this feels like it would be the most common way to use this feature, I wrote a macro for this:

* `MK(X1, X2, ...)`: Acts like `KC()` except it registers / unregisters all `X1`, `X2`, ... codes at the same time.

* `D(X1, X2, ...)`: A basic keycode dance. If tapped (or held), registers `X1`. If tapped and then tapped again (or held), registers `X2`, ... It *cannot* recognize between tapping and holding to register different keycodes (however holding will result in repeat). You can put in as many basic keycodes as you want, but the macro will break if you go beyond 256. Just like the `butterstick_rows` and `butterstick_cols` macros, it will try to expand shortened keycodes. Advanced keycodes are not *yet* supported.

* `DM_RECORD`, `DM_NEXT`, `DM_END`, `DM_PLAY`: Start recording a dynamic macro. Once you start recording, basic keycodes will get stored. When replaying the macro, all keys you press before `DM_NEXT` or `DM_END` will get pressed at the same time. For example the sequence `DM_RECORD`, `KC_CTRL`, `KC_A`, `DM_NEXT`, `KC_BSPC`, `DM_END` will record a macro that when played will execute the sequence Ctrl+a, Backspace. In `keyboard.inc` is defined macro `DYNAMIC_MACRO_MAX_LENGTH` that defines the maximum length of the macro to be recorded. You can increase it for the price of RAM. The example above requires 4 units of length to be saved (Ctrl, A, next, Backspace).

* `CLEAR_KB`: clears keyboard, sets all chords to the default state and switches the pseudolayer to the default one. Basically the emergency stop button.

* `RESET`: Go to the DFU flashing mode.


Macro `secret_chord` allows you to add a single chord while utilize the smart string parsing and defining the chord's keys visually. For example

```c
$secret_chord("QWERTY", "DF(ASETNIOP)",
    "X, , , , , , , , , X,\
     X, , , , , , , , , X")
```

adds chord on the `QWERTY` pseudolayer that gets activated with `TOP1 + TOP0 + BOT1 + BOT0` and on activation permanently switches to the `ASETNIOP` layer.

I also have `asetniop_layer` (see [http://asetniop.com](asetniop.com)) macro to define chorded input on the 4 top-left and 4 top-right keys:

```c
$asetniop_layer("ASETNIOP",
    "A,  S,  E,  T,  N,  I,  O,  P,\
       W,  D,  R,  B,  H,  L,  ;,\
         X,  C,  Y,  V,  U,  ,\
           F,  J, \,,  G,  M,\
             Q,  K,  -,  BSPC,\
               Z,  .,  ',\
                 [,  ],\
                   /")
```

This macro can also parse strings like `butterstick_rows`.

All these macros are defined in `macros.inc` and look something like this:

```c
$macro(butterstick_rows, PSEUDOLAYER, K1, K2, K3, K4, K5, K6, K7, K8, K9, K10, K11, K12, K13, K14, K15, K16, K17, K18, K19, K20, K21, K22, K23, K24, K25, K26, K27, K28, K29, K30)
    $nonlocal(NUM_OF_CHORDS)
    $add_key(PSEUDOLAYER, "H_TOP1", K1)
...
    $add_key(PSEUDOLAYER, "H_TOP0", K10)
    $add_key(PSEUDOLAYER, "H_TOP1 + H_BOT1", K11)
    $add_key(PSEUDOLAYER, "H_TOP2 + H_BOT2", K12)
...
    $add_key(PSEUDOLAYER, "H_BOT9", K29)
    $add_key(PSEUDOLAYER, "H_BOT0", K30)
$endmacro
```

On the input are all the actions (`K1` to `K30`) and each line runs the `$add_key` macro (parses the action string and adds a new chord). If you want the macro to create more chords, add more arguments and a new `$add_key` chord for each of them. The `secret_chord` macro uses variable `T1 ... T0` and `B1 ... B0` on the input. I am not sure if those names have to be unique.

### Leader Key

To add a new sequence, in your `keymap.c.in` use the macro `add_leader_combo`:

```c
void test(void) {
    SEND_STRING("Hello!");
}
$add_leader_combo("{KC_Q, KC_Z, 0, 0, 0}", "test")
```



Notice that the sequences are not defined by the *keys* you press but by the *keycodes* that get intercepted. The length of the sequence must be equal to the maximum (defined in `keyboard.inc`), if you want it to be shorter than the defined maximum, you have to pad it with zeros. Currently, the timeout for the leader sequence refreshes after each key pressed. If the sequence is not in the database, nothing will happen.

### Tests

In my keymap folder (for now) are automated tests. I tried to use a ready test framework but struggled so I wrote something tiny based on the minunit test framework and pyexpander. Sadly, I didn't write the tests from the beginning,  so I am not 100% confident in the stability of the system, but at least I should have a full coverage. If you have any recommendations on how to improve these, I am listening.

## Caveats

Each chord stores as much as possible in `PROGMEM` and unless it needs it, doesn't allocate `counter`. However it still has to store it's `state` and sometimes the `counter` in RAM. If you keep adding more chords, at one point you will run out. If your firmware fits in the memory and your keyboard crashes, try optimizing your RAM usage.

Also, the code is not perfect. I keep testing it, but can not guarantee that it is stable. Some functions take (very short but still) time and if you happen to create keypress event when the keyboard can not see it, a chord can get stuck in a funny state. That is especially fun if the pseudolayer changes and you can not immediately press it again. Just restart the keyboard or push the key a few times.

The use of `pyexpander` is a bit double-edged sword. It shortens the code *dramatically*, I can not imagine writing the keymap without it. Defining just the alphas would be 72 lines of code instead of the current 4. On the other hand, the code `pyexpander` produces is functional but ugly. It preserves too much whitespace (that is technically avoidable but then the code for preprocessor becomes ugly). It also introduces another language and another tool to the project. Macros rarely offer autocompletion, so you have to rely on documentation and existing code. But worst of all, it can be difficult to debug. The lines in the error log have lost their meaning and you don't get to see the source code that produced the error. And you get no static analysis. I *tried* keeping it in pure C with the help of some boost preprocessor magic but even that quickly ran into issues. Soon I was `#include`-ing dozens of files just to simulate functions and the error messages were just as cryptic.