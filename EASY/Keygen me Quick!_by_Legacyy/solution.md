Crackme's link: https://crackmes.one/crackme/60d65d0833c5d410b8843014

Overview: Serial Keygenme

Note: Key/Password are used there as the same thing

## Initial Analysis

After locating the main function in Ghidra, I renamed functions and variables for clarity. The main function structure reveals the program's flow:

```c
void main(void)
{
  int iVar1;
  char Password[16];
  uint local_8;
  
  local_8 = DAT_00466108 ^ (uint)&stack0xfffffffc;
  _memset(Password, 0, 0xf);
  printf((wchar_t *)s_Welcome_to_KeygenMe_1_sir_:)_Ent_00466040);
  ___acrt_iob_func(0);
  fgetsChar();
  iVar1 = checkFormat(Password);
  if (iVar1 == 0) {
    printf((wchar_t *)s_Invalid_key_format,_must_be_in_t_0046609c);
  }
  else {
    printf((wchar_t *)s_Key_in_correct_format._0046606c);
    iVar1 = checkOne((int)Password);
    if (((iVar1 != 0) && (iVar1 = checkTwo((int)Password), iVar1 != 0)) &&
       (iVar1 = checkThree((int)Password), iVar1 != 0)) {
      printf((wchar_t *)s_Congrats,_you_did_it!_00466084);
    }
  }
  __security_check_cookie(local_8 ^ (uint)&stack0xfffffffc);
  return;
}
```

The program follows a clear validation sequence: it prints a welcome message, requests user input, and then validates the password through four distinct checks.

## Validation Function Analysis

### Format Validation (`checkFormat`)

The first validation function checks the basic structure of the input:

```c
undefined4 __cdecl checkFormat(char *param_1)
{
  size_t sVar1;
  undefined4 uVar2;
  
  sVar1 = strlen(param_1);
  if (((sVar1 == 0xe) && (param_1[4] == '-')) && (param_1[9] == '-')) {
    uVar2 = 1;  // Format is valid
  } else {
    uVar2 = 0;  // Format is invalid
  }
  return uVar2;
}
```

This function validates that the input follows the pattern `XXXX-XXXX-XXXX`:
- The total length must be exactly 14 characters (0xe in hex)
- Character at position 5  (index 4) must be a hyphen
- Character at position 10 (index 9) must be a hyphen

**Important Note**: There's a subtle implementation detail here. The function checks for a length of 14, but due to how the input is processed, the validation can succeed even if the last character is missing, making the minimum effective length 13 characters.

### First Check (`checkOne`)

This function validates the first block of four characters:

```c
int __cdecl checkOne(int param_1)
{
  int local_c;
  int index;
  
  local_c = 1;
  for (index = 0; index < 4; index = index + 1) {
    if ((*(char *)(param_1 + index) < '0') || ('9' < *(char *)(param_1 + index))) {
      local_c = 0;  // Character is not a digit
    }
  }
  if (local_c == 0) {
    printf((wchar_t *)s_Check_one_failed._00466000);
  }
  return local_c;
}
```

This check ensures that first four characters are all digits between '0' and '9'. Each character is compared against the ASCII values of '0' and '9' to verify it falls within the valid digit range.

### Second Check (`checkTwo`)

The second validation function examines the middle block:

```c
int __cdecl checkTwo(int param_1)
{
  int local_c;
  int index;
  
  local_c = 1;
  for (index = 5; index < 9; index = index + 1) {
    if ((*(byte *)(param_1 + index) & 1) != 0) {
      local_c = 0;  // Character has odd ASCII value
    }
  }
  if (local_c == 0) {
    printf((wchar_t *)s_Check_two_failed._00466014);
  }
  return local_c;
}
```

This function performs a bitwise AND operation with 1 on each character indexed by 5-8. To pass the check - all characters in this block must have even ASCII values. Since the ASCII values of digits '0', '2', '4', '6', and '8' are even (48, 50, 52, 54, 56), only these even digits will satisfy this condition.

### Third Check (`checkThree`)

The final validation function checks the last block:

```c
int __cdecl checkThree(int param_1)
{
  int iVar1;
  
  iVar1 = strcmp((char *)(param_1 + 10), "R3KT");
  if (iVar1 == 0) {
    return 1;  // Strings match
  } else {
    printf((wchar_t *)s_Check_three_failed._00466028);
    return 0;  // Strings don't match
  }
}
```

This check compares the substring starting at index 10 (the third block) with the hardcoded string "R3KT". The `strcmp` function returns 0 when the strings are identical, so the check passes only when the third block exactly matches "R3KT".

There is tricky implementation issue:
- Crackme uses `fgets`, which places `\n` in the end of string　(because of pressed enter).
- `strlen` `strcmp` work until `\0` (null terminator), but they also count `\n`. 
- It turns out that we can enter 13 bytes, but got 14. So length check is satisfied, while `strcmp` will check only bytes until null terminator, so that last character of hardcoded string is thrown away.

**But why if we put 14 bytes - it still works?**

- We write 14 bytes + byte "Enter". But code has buffer that can contain only 14 bytes so that `\0` cannot be placed in the end. So that last "Enter char is thrown away, while `\0` is placed. 

## Solution Strategy

Based on the analysis of all validation functions, a valid password must satisfy these requirements:

1. **Format**: Follow the pattern `XXXX-XXXX-XXXX` (with potential flexibility on the last character)
2. **First Block**: Contain exactly four digits (0-9)
3. **Second Block**: Contain exactly four characters with even ASCII values (0, 2, 4, 6, 8)
4. **Third Block**: Must be exactly "R3KT" or "R3K"

The simplest valid password that satisfies all conditions is: `0000-0000-R3KT`

## Default Keygen Implementation


```python
import random

def generate_valid_key():
    first_block = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    
    even_digits = ['0', '2', '4', '6', '8']
    second_block = ''.join([random.choice(even_digits) for _ in range(4)])
    
    third_block = "R3KT"
    
    return f"{first_block}-{second_block}-{third_block}"

if __name__ == "__main__":
    key = generate_valid_key()
    print(f"Generated valid key: {key}")
```

![image](https://github.com/user-attachments/assets/365c551a-45b6-40d4-9970-ac881e9c1ec9)

