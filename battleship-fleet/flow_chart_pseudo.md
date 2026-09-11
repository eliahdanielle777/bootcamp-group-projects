Flowchart:

       START
         ↓
   Set up the ships
         ↓
   Ask player for shot
         ↓
     Valid shot?
      ↙       ↘
    NO         YES
    ↓           ↓
 Show error   Apply shot
    ↓           ↓
    └────→ Show result
                ↓
        Are all ships sunk?
           ↙          ↘
         NO            YES
         ↓              ↓
     New shot       Game Over
         ↓
         └──────────────┘

Psuedocode:

**START**

Set up the board and ships

Set shots to empty

WHILE all ships are not sunk:

```
Show available cells

Ask player to enter a cell

IF cell is invalid or already shot:
    Show error
    Continue

Add cell to shots

IF cell hits a ship:
    IF all cells of that ship are shot:
        Show "Ship sunk"
    ELSE:
        Show "Hit"
ELSE:
    Show "Miss"
```

IF all ships are sunk:
Show "Fleet defeated"

**END**
