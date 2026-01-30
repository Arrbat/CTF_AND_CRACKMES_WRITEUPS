Crackme's link: https://crackmes.one/crackme/678054fd4d850ac5f7dc4f6d

Overview: Begginer-friendly password checker

Loaded the .exe file with Ghidra, then started looking for strings as the initial analysis phas

Intresting strings (highlighted) are:
![изображение](https://github.com/user-attachments/assets/d539f098-c666-4d37-acef-c632de9241c2)

Then I moved to this string and found the related function where it is used:

![изображение](https://github.com/user-attachments/assets/cf37664c-eb59-4ce6-8df3-974f0c9df758)

The most useful for us here is this part of code

```c
  do {
    FUN_140001010((basic_istream<> *)cin_exref,(longlong *)&local_30);
    _Src = &local_30;
    if (0xf < local_18) {
      _Src = (char ***)local_30;
    }
    sscanf((char *)_Src,"%d",local_38); //gets the input
    if (local_38[0] == 10) {
      pcVar1 = "!crackme!"; //right output
    }
    else {
      pcVar1 = " ohh nooo..."; //input is not correct
    }
    this = FUN_140001270((basic_ostream<> *)cout_exref,pcVar1); 
    std::basic_ostream<>::operator<<(this,FUN_140001640); //outputs the pcVar1
  } while( true );
```

As you can see logic is quite simple: app gets the input and stores that as `local_38` variable. If input is `10` so the `pcVar1` (output message, like log) will be changed into `!crackme!` and then it will be outputed with last lines of code, which means that solution is correct in that case.

![изображение](https://github.com/user-attachments/assets/0b5e2798-4f40-444f-994f-dd136d77de6c)


So the solution is `10`
