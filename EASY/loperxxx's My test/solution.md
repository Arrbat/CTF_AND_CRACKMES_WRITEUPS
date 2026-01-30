Crackme's link: https://crackmes.one/crackme/67f960568f555589f3530a6b

Overview: Simple login and password checker with some common anti-debugger

## First execution

App requires login and password, and if they are right - access must be granted.

<img width="749" height="144" alt="Pasted image 20250714142526" src="https://github.com/user-attachments/assets/d03d87b3-d620-46c9-ade4-470e4500edc3" />


## Dynamic Analysis using x64dbg

Usually strings list may contain some useful information, so, let's check it:

`Right Click -> Search for... -> All User Modules -> String References`

After that set breakpoints on the 5-10 strings only, since other not very interesting and mostly are used for exceptions, error handling and other default stuff.

<img width="1709" height="308" alt="Pasted image 20250714142845" src="https://github.com/user-attachments/assets/92cf951a-aa8d-4f45-ae06-16898b83bcff" />

After that reload app and continue until breakpoints, where the cycle is:

<img width="885" height="37" alt="Pasted image 20250714143313" src="https://github.com/user-attachments/assets/af8e35c9-b309-4f2a-b2eb-6bf9325ffec7" />

---

## The execution flow

<img width="1269" height="615" alt="Pasted image 20250714144211" src="https://github.com/user-attachments/assets/b037a46a-c022-433c-8024-52110a781ccd" />


<img width="804" height="56" alt="Pasted image 20250714144455" src="https://github.com/user-attachments/assets/a62f7130-39d8-4274-af1a-e33f3890d58a" />

Crackme calls of `argc` and `argv` mean that app manipulates with provided command line arguments (as expected, since login and password provided...)

So, by using step-by-step execution - we reach default anti-debug technique

<img width="1290" height="396" alt="Pasted image 20250714145321" src="https://github.com/user-attachments/assets/5e30e2c3-8ba8-45bb-8f4a-e49d4f217b32" />

App uses default WinAPI call `IsDebuggerPresent`

The logic of it is simple, just checks `BeingDebugged` field in `PEB (process environment block)` structure.
So return value of this call must be 1 since we run app under debugger. 

There are several common ways to bypass this technique:
1) Manual register patching. In x64 (which crackme is) in default calling conventions (and WINAPI) `RAX` is used to store return value. So that, we can execute the function and then just patch it to zero (aka No Debugger Present)
2) `PEB` hiding in x64/x32dbg (Debug -> Advanced -> Hide Debugger (PEB)). This technique will work every time we execute the app, so that no need in patching registers every time.

First technique will be used, since it teaches how to bypass technique manually and without "hiding" whole PEB

Set the breakpoint on this call.
Of course function sets the register `RAX` to `1`, which means Debugger is present

<img width="286" height="28" alt="Pasted image 20250714145842" src="https://github.com/user-attachments/assets/82af55cc-ddd8-4099-b11b-68fd62e5ed33" />

Change it to 0 right on the next line after call is executed

<img width="1016" height="129" alt="Pasted image 20250714150134" src="https://github.com/user-attachments/assets/0e78b6ac-aeac-43a8-9363-13070ded431e" />

So `DebugBreak` (mechanism of generating exception, often used in debugging) was bypassed, so that debugger is not broken.

---

So now just `Run` it and will see some main logic

<img width="1705" height="341" alt="Pasted image 20250714150650" src="https://github.com/user-attachments/assets/42c5ba9b-860e-4044-a69e-6022da81dae3" />

Keep on execution, while entering login and password

And another `DebugBreak` is here. Maybe like multiple `IsDebuggerPresent` calls
So i just do quickly same things (changing return value of first anti-debugger) and now stand on breakpoints with main logic

There is just another `IsDebuggerPresent` right after the main logic

<img width="1165" height="221" alt="Pasted image 20250714151413" src="https://github.com/user-attachments/assets/5ab5a846-80bb-453b-8fed-88dfc9092dd1" />

I patched registers again

---

App checks if provided arguments are correct:

<img width="1577" height="365" alt="Pasted image 20250714154427" src="https://github.com/user-attachments/assets/60e584e5-42f3-454a-97e9-76bdda1a43bd" />

Put breakpoints on `cmp` instructions before this code

Run it, got `access is denied` and then I reload the app. 

Since there is no practical need to patch registers for preventing debugger detection anymore - just hide PEB (second technique)

There is `cmp` with `rbx` which on that step equals to `5`. It is length checking, login must be 5 chars in length.

<img width="935" height="58" alt="Pasted image 20250714155628" src="https://github.com/user-attachments/assets/11835c7e-045f-4523-b3cc-d49049edf315" />

It fails, because crackme expects another string length (I inputed wrong strings). **Goal is to bypass jne**, cause it launches code with access denying. 

Reload the app and set values length of 5 chars (both password and login, but they are not the same)

<img width="247" height="53" alt="Pasted image 20250714155942" src="https://github.com/user-attachments/assets/be53ec3a-f633-4e4c-ab06-e8e2cc9d965d" />

And after that `jne` with access denying code was not triggered.


---

Now `RIP` is here, where `RSI` is 8

So I assume that login must be equaled to the length of 5 and password must be the length of 8


<img width="820" height="18" alt="Pasted image 20250714160041" src="https://github.com/user-attachments/assets/352ef7f8-189b-4753-a8b6-d6db94c093dd" />

Since password was the length of 5 - I got access denied message.

Reloaded app and provided another arguments.

<img width="303" height="63" alt="Pasted image 20250714160316" src="https://github.com/user-attachments/assets/af3ccfe9-8e62-4671-867f-27cebff72b2b" />


Then i do step-by-step execution in the block where arguments are checked.

At some point register was changed. I assume that it is correct login. Continue execution

<img width="480" height="27" alt="Pasted image 20250714160501" src="https://github.com/user-attachments/assets/2d9e9596-8711-464e-9727-e9476287a31c" />

Correct (on this step didn't know if it is really correct; I suppose it is right*) login and my login were loaded to memory


<img width="383" height="61" alt="Pasted image 20250714160602" src="https://github.com/user-attachments/assets/15ea7ab8-df82-4633-ba47-f8ae1661c537" />


<img width="1195" height="91" alt="Pasted image 20250714160710" src="https://github.com/user-attachments/assets/6acc8740-6f38-4077-b9eb-0110f831243f" />

It is comparing the strings

After that I continued the execution and got access denied (look on `jne` on the screen, if strings are not same it jumps and fails)

So reloaded the app and did same things, but instead of `login` i write `admin`

There was no jump on `jne` (because strings equaled to each other)

---

Same check is with password

<img width="514" height="27" alt="Pasted image 20250714161142" src="https://github.com/user-attachments/assets/5be96e3b-0fd6-446c-8761-ec49212e2e58" />

Correct password was loaded into memory. Also my string-password was `password`. So I just came across correct password. 

Same logic as with login checking (we load the values, checking equality and if they are equaled we bypass jne jump)

---
It is possible to see that "Access granted" used in registers or in execution flow


# Solution

### `Login: admin`

### `Password: password`

<img width="613" height="132" alt="Pasted image 20250714161515" src="https://github.com/user-attachments/assets/f2e0841c-96c8-4534-a48e-f387a9f30e9d" />


Another way to solve it is:
- Patching `jne` so that it will jump to the code with access granting. In real applications it will be more complicated of course, but such patching will be more efficient if we check that app is crackable so that we can find the solution to secure it.
