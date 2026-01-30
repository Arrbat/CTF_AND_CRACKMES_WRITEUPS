
Crackme's link: https://crackmy.app/crackmes/tweetys-serialme-by-tweety100-by-crackmes-de-97185

Overview: GUI Serial checker

---

Logic description shortly: app waits for input for 3 fields - Name, First Serial, Second Serial. Handles it and then must say if input is valid or not. 

>Also i renamed some variables and funcs for better understanding. `?` is there because i suppose that variable of func does some thing or plays concrete role, but we can not be sure before checking it

---

## Loaded in PE-BEAR (same may be done in Ghidra or any other similar tool)

Based on strings it was built with GCC. And main strings related to where input is handled - are not hidden. Also this program is old - year 2010.

Imports:
-KERNEL32.dll
-msvcrt.dll

Conclusion: nothing special.

## Loaded in Ghidra:

Completed auto-analysis.

In entry there is only one called func. 
This func just makes system init like. In the end there is main() function, which is the most interesting

```c++
uExitCode = FUN_004013bc(); //main() called
```

Before checking input, app uses custom printf/scanf implementation (or wrapper).

In main we see where our input is proceed and most likely being correct. The "correct" block of code is:

```c++
  if (local_84 == uVar3) { // inputed_first_serial == calculated_first_serial
    if (local_88 == uVar2) { //inputed_second_serial == calculated_second_serial
      local_7c = 9;
      FUN_00440ddc((int *)&DAT_004483c0,"Input correct. Unlocking features");
      FUN_0044214c((int *)&DAT_00448460,local_2c);
      iVar1 = local_3c;
      puVar4 = (undefined *)(local_3c + -0xc);
      FUN_0042a56c();
      if (puVar4 != &DAT_00444260) {
        local_7c = 2;
        iVar1 = FUN_0040361c((int *)(iVar1 + -4),-1);
        if (iVar1 < 1) {
          FUN_0043198c(puVar4);
        }
      }
      FUN_0042a5ac();
      FUN_0042a5bc();
      iVar1 = local_2c[0];
      puVar4 = (undefined *)(local_2c[0] + -0xc);
      FUN_0042a56c();
      if (puVar4 != &DAT_00444260) {
        local_7c = 1;
        iVar1 = FUN_0040361c((int *)(iVar1 + -4),-1);
        if (iVar1 < 1) {
          FUN_0043198c(puVar4);
        }
      }
      FUN_0042a5ac();
      FUN_0042a5bc();
      local_8c = 0;
```

I suppose that `local_2c` is the `Name`, because before condition statement this variable was used in getting input from user after printing the "Name:". 

Also program ends with `Wrong input.` - if first serial is incorrect, without checking the second (because first is used to calculate the second, so if first is not correct - second will be incorrect automatically). So, suppose `local_84` is First Serial, `local_88` is Second Serial; `uVar3` and `uVar2` are correct precalculated serials. 

So let\`s come back to what was before these statements:

```c++
  equals_to_inputed_name? = FUN_0040138e(name_inputed?);
  for (correct_first_serial? = (uint)(equals_to_inputed_name? * 0x1f) / 0x275 + 0x2a5f828;
      999999999 < correct_first_serial?; correct_first_serial? = correct_first_serial? / 10) {
  }
  for (correct_second_serial? = correct_first_serial? * 0x52 - 3; 99999 < correct_second_serial? ;
      correct_second_serial? = correct_second_serial? / 10) {
  }
```

We can see that `Name` is used for calculations. And seems like `FUN_0040138e` returns something based on name.

```c++

int __cdecl FUN_0040138e(undefined4 *param_1)

{
  int iVar1;
  char *pcVar2;
  char *pcVar3;
  
  iVar1 = 0;
  pcVar2 = (char *)*param_1;
  pcVar3 = pcVar2 + *(int *)(pcVar2 + -0xc);
  for (; pcVar2 != pcVar3; pcVar2 = pcVar2 + 1) {
    iVar1 = iVar1 + *pcVar2;
  }
  return iVar1;
}
```

It could be understood like "The sum of the ASCII character values of the name."

So now I can rewrite logic like that (we do not patching the program logic):

```c++
//First serial
uVar3 = (sum * 0x1f) / 0x275 + 0x2a5f828;

while (uVar3 > 999999999)
  uVar3 /= 10;
```
```c++
//Second serial
uVar2 = uVar3 * 0x52 - 3;

while (uVar2 > 99999)
  uVar2 /= 10;
```

So the main statement is like this:

```c++
if (first_serial == uVar3 && second_serial == uVar2)
```

Now we know how logic of creating serials works - so it is possible to write script (in Python for example) which will create correct serials due to inputed name.

```Python
def generate_serials(name):
    sum_ascii = sum(ord(c) for c in name)

    firstSerial = (sum_ascii * 0x1f) // 0x275 + 0x2a5f828
    while firstSerial > 999_999_999:
        firstSerial //= 10

    secondSerial = firstSerial * 0x52 - 3
    while secondSerial > 99_999:
        secondSerial //= 10

    return firstSerial, secondSerial

# example
name = "admin"
serial1, serial2 = generate_serials(name)

print(f"Name: {name}")
print(f"Serial 1: {serial1}")
print(f"Serial 2: {serial2}")
```

After running the script i got:
```python
Name: admin
Serial 1: 44431425
Serial 2: 36433
```

Let\`s check if it is valid:
```
C:\Users\home\Downloads>tweetys.exe
Name: admin
Serial: 44431425
Second Serial: 36433
Input correct. Unlocking features
```


---
So the solution is to calculate serials manually or to use script.