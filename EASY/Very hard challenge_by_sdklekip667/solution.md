
Crackme's link: https://crackmy.app/crackmes/very-hard-challenge-by-sdklekip667-59585


Overview: Password checker

---

`main()` initializes the program and prints "please enter the key:".

The user input is stored in key and later compared to a generated expected value.

So main logic is like in

```
/* It takes the string "331" and an integer 22.

   For each digit in the string, it adds 22, takes modulo 10, and converts it back to a character.

   "331" → '3' + 22 = 25 % 10 = 5 (twice)           '1' + 22 = 23 % 10 = 3

   Result: "553"
*/
```
```c

longlong * FUN_00401639(longlong *param_1,undefined8 *param_2,int param_3)

{
  undefined8 uVar1;
  int iVar2;
  longlong local_28;
  longlong local_20;
  char *local_18;
  longlong *local_10;
  
  FUN_00490ba0(param_1,param_2);
  local_10 = param_1;
  local_20 = FUN_0048f4e0(param_1);
  local_28 = FUN_0048f3a0(local_10);
  while (uVar1 = FUN_0041eed0(&local_20,&local_28), (char)uVar1 != '\0') {
    local_18 = (char *)FUN_0041fdd0(&local_20);
    if ((int)*local_18 - 0x30U < 10) {
      iVar2 = *local_18 + -0x30 + param_3;
      *local_18 = (char)iVar2 + (char)(iVar2 / 10) * -10 + '0';
    }
    FUN_0041dea0(&local_20);
  }
  return param_1;
}
```

Once the transformation is complete, the result is compared with the correct answer using FUN_0049fbe0.

```c

undefined8 FUN_0049fbe0(undefined8 *param_1,undefined8 *param_2)

{
  int iVar1;
  longlong lVar2;
  longlong lVar3;
  size_t sVar4;
  void *pvVar5;
  void *pvVar6;
  
  lVar2 = FUN_0042a9c0((longlong)param_1);
  lVar3 = FUN_0042a9c0((longlong)param_2);
  if (lVar2 == lVar3) {
    sVar4 = FUN_0042a9c0((longlong)param_1);
    pvVar5 = (void *)FUN_0042a820(param_2);
    pvVar6 = (void *)FUN_0042a820(param_1);
    iVar1 = FUN_0046d320(pvVar6,pvVar5,sVar4);
    if (iVar1 == 0) {
      return 1;
    }
  }
  return 0;
}

```

First, it checks if the lengths match (FUN_0042a9c0)

Then, it compares contents byte-by-byte using FUN_0046d320 

Returns 1 (success) if strings match, else 0


So the password is `553`
