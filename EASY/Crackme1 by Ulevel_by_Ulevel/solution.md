Crackme's link: https://crackmes.one/crackme/66168bfdcddae72ae250c4c2

Overview: Simple crackme, goal is to find right password.

---

Opening any disassembler/decompiler we find the main function so that we can look how program works. 

There is an bool condition in main function, and if it is true, then access is granted

```c
  if (bVar1) {
    uVar4 = 0x26;
    pcVar3 = "The password is valid, access granted.";
    std::__ostream_insert<>((ostream *)&_ZSt4cout,"The password is valid, access granted.",0x26) ;
  }
```

### What is `bVar1`?

`bVar1` is defined as 

```c
bVar1 = IsPassValid((longlong *)&local_48);
```

`IsPassValid` is defined as:

```c
bool IsPassValid(longlong *param_1)
{
  bool bVar1;
  
  if (param_1[1] != 0xb) {
    return false;
  }
  if ((*(longlong *)*param_1 == 0x69206b6f6369614e) && (*(int *)(*param_1 + 7) == 0x6a697269)) {
    bVar1 = false;
  }
  else {
    bVar1 = true;
  }
  return !bVar1;
}
```

First two ifs are the conditions, which must me satisfied to get `bVar1` as true.

First: provided password must be 11 charachers long (0xb = 11 in decimal). Usually any strings (which password is) in apps have some limits, constraints and so on, which are checked in code. Here there is statement which just checks `is parameter equaled to 11?`, we suppose it defines the length, since it is the most common check in the program. 

So, there are two HEX sequences which must be the password's part, otherwise `bVar1=false`

> NOTE: in little-endian memory (which x86/x64 is) will hold these bytes in "reverse" order

> NOTE: param_1+7 means that we start at byte 7 of value (reading the memory where 7th byte is stored)

```c
0x4E → 'N'
0x61 → 'a'
0x69 → 'i'
0x63 → 'c'
0x6F → 'o'
0x6B → 'k'
0x20 → ' ' (space)
0x69 → 'i'
0x69 → 'i'
0x72 → 'r'
0x69 → 'i'
0x6A → 'j'
```


![image](https://github.com/user-attachments/assets/f3c73bb6-a129-491f-be68-de085444d8b6)



### So the password is `Naicok irij`


Notes after later writeup revision:
-  `param_1[1] != 0xb` looks strange, since second byte is used for check (not typical way to calculate string size). Likely decompiler is wrong. While second char is `a` or `0x61`, condition `0x61=0xb` cannot be satisfied.
- Also, decompiler assigned `longlong` type to the parameter, which is not char array (string)