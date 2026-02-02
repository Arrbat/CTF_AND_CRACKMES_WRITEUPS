Crackme's link: https://crackmes.one/crackme/694c3de30c16072f40f5a3d2

Overview: KeyGenMe with basic anti-analysis and permutations techniques

You may start from `7)` if you just want to see how it was solved and how main logic works.

---

## First Execution

Crackme requires to input username and password, if they're wrong - app fails

```bash
./crackme.exe

===========
Welcome
===========
Username:somename
Password:somepassword
Failed.

```

## Static Analysis

Initial analysis with `Detect It Easy`. By looking into strings section interesting information is extracted:
- Anti-debug technique that checks if debugger is attached to the current process is used(`CheckRemoteDebuggerPresent`)
- Anti-debug technique that checks `IsDebugged` field in `PEB` structure is used (`IsDebuggerPresent`)
- Many imports are not used in main code, but still imported (`rdseed` `rdrand` `rdrnd`, mutex functions, sleep and other)

Since both anti-debug techniques usually are used in the way of checking return value (`0` - no debugger, `1` - there is debugger), it turns out that they have same bypassing techniques. Some of them:
- Changing RAX (crackme is x64, on x86 - EAX) register to `0`. RAX typically used to store function's return value
- Changing `PEB.BeingDebugged` field to `0`
- Bypassing call via patching program or simply changing RIP (but depends on how app works)

But, debugging will not be used, since solution appeared while using static-analysis.

---

By using binary-ninga some other info were extracted. `bcrypt` lib is imported, but not used

Now explaing `main()` in details step-by-step:

1) 

`sub_140001740` is function, which calls both `IsDebuggerPresent` and `CheckRemoteDebuggerPresent`

```c
if (sub_140001740() == 0)
```

Where such code is used:

```c
      if (IsDebuggerPresent() == 0)
          CheckRemoteDebuggerPresent(hProcess: GetCurrentProcess(), &pbDebuggerPresent)
          result.b = pbDebuggerPresent != 0
```

2)

Next part of code is initializing variable `i` with `ggggggggggg` string. Since first byte (character) is not zero - `if` statement will be true. In that if-block each byte of `i` string is xored with constant value `0x5a`.

```c
char i = data_140022098[0]; /* "ggggggggggg" */

...

          if (i)
          {
              char* rdx_1 = "ggggggggggg";
              
              do
              {
                  rdx_1 = &rdx_1[1];
                  rdx_1[-1] = i ^ 0x5a;
                  i = *(uint8_t*)rdx_1;
              } while (i);
          }

```

Decompiled code (pseudo-c) may look strange, since if-block tries to change string literal, which is not modifiable (see `string literal on cppreference` for details), but it is just decompiling issue. Dissasembly looks as follows:

```c
mov     rdx, rbx  {data_140022098, "ggggggggggg"}
nop     word [rax+rax]

xor     eax, 0x5a
add     rdx, 0x1
mov     byte [rdx-0x1], al
movzx   eax, byte [rdx]
test    al, al
jne     0x140020b20
```

So, "ggggggggggg" XOR 0x5a equals to "==========".

Then there is `puts()` which prints the decoded value to the cmd

3) 

Second if-block is the same as previous (just another variables used)

```c
          char i_1 = data_140022098[0]; /* "ggggggggggg" */
          
          if (i_1)
          {
              char* rdx_2 = "ggggggggggg";
              
              do
              {
                  rdx_2 = &rdx_2[1];
                  rdx_2[-1] = i_1 ^ 0x5a;
                  i_1 = *(uint8_t*)rdx_2;
              } while (i_1);
          }
```

Then there is `puts()` which prints the decoded value to the cmd

4) Third if-block is logically the same:

```c
          char i_3 = data_140022090[0]; /* "\r?6957?" */
          
          if (i_3)
          {
              char* rdx_4 = "\r?6957?";
              
              do
              {
                  rdx_4 = &rdx_4[1];
                  rdx_4[-1] = i_3 ^ 0x5a;
                  i_3 = *(uint8_t*)rdx_4;
              } while (i_3);
          }

```

where `\r?6957?` XOR 0x5a equals to `Welcome`

Then there is `puts()` which prints the decoded value to the cmd

So we can build welcome message, that we saw

```c
===========
Welcome
===========
```

Need to point out that there are code duplications, but with some other variables used, while we see only 3 puts (but there are 6 if blocks related to welcome message above). It is done for ecnrypting decrypted strings again, so that decoded strings will not stay in memory.

By simplifying it, we see:

```c
xor_decode(line1);
puts(line1);
xor_decode(line1);

xor_decode(line2);
puts(line2);
xor_decode(line2);

xor_decode(line1);
puts(line1);
xor_decode(line1);
```

5)

Next code decrypts variable; we get "sername:" ('u' is "lost").
Also code prints this variable with sub_140014f10.

```c
          char i_6 = data_140022080
          
          if (i_6 != 0)
              char* rdx_7 = &data_140022080
              
              do
                  rdx_7 = &rdx_7[1]
                  rdx_7[-1] = i_6 ^ 0x5a
                  i_6 = *rdx_7
              while (i_6 != 0)
          
          sub_140014f10("%s", &data_140022080)
          char i_7 = data_140022080

```

And encrypts variable again

Then there is similar code that decrypts (and then encrypts again) `\n;))-5(> ^ 0x5a` which equals to `Password`

6) Here is a code that uses scanf inside to allow user to input credentials

```c
          sub_1400209d0("%63s", &string1);
          int64_t string2;
          sub_140001780(&string, &string2);
```

Actually disassembly looks more logically (pseudo-c is faster to read but does not save code-blocks suquences how they really are placed): `decode string -> print -> encode string -> scanf` (same with username and password)


7) function `sub_140001780` does following:

- XORes arg1 (actually it is our string, since in code it appears earlier than second one - we suppose it is inputed username) with `0xd`
- Reverses the xored buffer
- converts each byte to two hex characters (by using `0123456789ABCDEF` string)
- writes result to arg2 (as output buffer); actually output buffer will be used for initializing `string2` (transformed username)

Also from this function we may say that string is <24 bytes long, since the buffer is of this length. Output buffer is `2*UsernameLength`.

By testing we can be sure that this function uses username string. Buffer overflow (app does not allows to write the password and fails):

```bash
./crackme.exe
===========
Welcome
===========
Username:verylongstring
Password:Failed.
```

By testing, username must be 8 chars in length, if more - app fails as shown above.

8) Then `sub_140001740` (anti-debugger) is again called

The following code is just allocator, which can throw error related to string length (`basic_string::_M_create`):

```c
int64_t* rax_12 = sub_14001f0b0(&var_c8, &var_e0, 0);
```

Next code allocates the string anyway (in normal situation) in heap memory. Later string destructor is called. 
```c
sub_14001d4d0(rax_12, "i'm watching you...", &data_14002305c[0x13]);
```

9) If inputs are wrong, string is printed:

```c
sub_14001d4d0(&var_b8, "Failed.", &data_140023070[7]);
```

10) Next, `\t/99?))</6{P` is XORed with 0x5a, which equals to `Successful!\n`

Then there is a code, that does following:
- As we checked already, checks that username is <= 8 chars, if not - we fail.
- **Transformed** username must be the same as raw password 

```c
              int32_t rax_18 = lstrlenA(&string);
              int32_t rax_22;
              
              if (rax_18 <= 8)
                  rax_22 = lstrcmpA(&string1, &string2);
              
              if (rax_18 > 8 || rax_22)
                  puts(&data_140022020);
              else
                  puts("\t/99?))</6{P");

```

It means, that `password = transorm(username)`.

For example let's take `username` as a username. 

So in `sub_140001780` (username tranform function) we have:
- XOR with 0x0D. So we got `0x78, 0x7E, 0x68, 0x7F, 0x63, 0x6C, 0x60, 0x68` sequence
- Reversing sequence of bytes
- HEX encoding. Each byte (in ASCII) is tranformed in its hex form. 

So that we got `68606C637F687E78`

```bash
./crackme.exe
===========
Welcome
===========
Username:username
Password:68606C637F687E78
Successful!
Flag: Congrats{U_Solv3d_1t!}
```

### Solved!

Keygenme:

```python
def keygen(username: str) -> str:
    if len(username) > 8:
        raise ValueError("Username must be <= 8 characters")

    # XOR with 0x0D
    xored = bytes([ord(c) ^ 0x0D for c in username])

    # Reverse
    reversed_bytes = xored[::-1]

    # Hex encode (uppercase)
    password = ''.join(f"{b:02X}" for b in reversed_bytes)

    return password


if __name__ == "__main__":
    user = input("Username: ")
    print("Password:", keygen(user))

```