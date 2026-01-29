Crackme's link: https://crackmes.one/crackme/5ab77f6333c5d40ad448ca8c

Overview: Simple userid and password checker

Second func in entry() is like basic app initialization. And here is the func main in the end.  (I renamed values and funcs for readability)

```c
returncodeMAIN = main();
```

`main` contains a lot of code, but the most interesting part is where string ` C:\\userid:` located. 
It is printed and by using `gets()` waits for user's input:

```c
  print?((int *)cout_exref,"C:\\userid:"); /* Some custom print or modificated one used, so that I renamed it to `print?` */
  gets(useridINPUT);
```

Same logic with password:

```c
  print?((int *)cout_exref,"C:\\passid:");
  gets((char *)passINPUT);
```

Also there is validation code, you may be sure it is validation because of used strings.

```c
validation:
  if (iVar6 == 0) {
    useridINPUT2 = "ok. welldone.\n";
  }
  else {
    useridINPUT2 = "ops. try harder.\n";
  }
  print?((int *)cout_exref,useridINPUT2);
  gets(useridINPUT);
```

There is strange comprasion, which says "if address `useridINPUT2 + - 6` is placed "lower" than
`0x4` - statement is true. But it does nothing useful in practice and furthemore, `userid` may be everything, but it does not influence on calculations or code, or solution. Likely it is the artifact of compiler or crackme is not completed.

```c
if (useridINPUT2 + -6 < (char *)0x4)
```

Since statement will be false mostly always (because strings are located higher than 0x4 in memory) we move ahead.
If false, the password is following (`invalid input`):

```c
  else {
    invalidi-inputSTRING[0]   = 'i';
    invalidi-inputSTRING[1]   = 'n';
    invalidi-inputSTRING[2]   = 'v';
    invalidi-inputSTRING[3]   = 'a';
    invalidi-inputSTRING[4]   = 'l';
    invalidi-inputSTRING[5]   = 'i';
    invalidi-inputSTRING[6]   = 'd';
    invalidi-inputSTRING[7]   = ' ';
    invalidi-inputSTRING[8]   = 'i';
    invalidi-inputSTRING[9]   = 'n';
    invalidi-inputSTRING[10]  = 'p';
    invalidi-inputSTRING[0xb] = 'u';
    uStack_108 = 0x74; /* aka `t` */
  }
```

Сode checks if password equals to string above:

```c
LAB_00401ff4:
      iVar6 = (1 - (uint)bVar7) - (uint)(bVar7 != 0);
      goto validation;
    }
    if (bVar2 == 0) break;
    bVar2 = pbVar5[1];
    bVar7 = bVar2 < passINPUT2[1];
    if (bVar2 != passINPUT2[1]) goto LAB_00401ff4;
    pbVar5 = pbVar5 + 2;
    passINPUT2 = passINPUT2 + 2;
  } while (bVar2 != 0);
  iVar6 = 0;
```

`iVar6` is used for validation, if it equals to zero then we got congratulations message.

Since the logic is like broken or incomplete (at least supposed so) it happens that userid normally does not matter. So only password must be right. 

### Solution, password: "invalid input"
