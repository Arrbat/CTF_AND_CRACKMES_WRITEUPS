
Crackme's link: https://crackmes.one/crackme/66a4193c90c4c2830c82113e

Overview: Key validator

## First Execution

It is a GUI application that simply requires to enter key. If key is invalid - app closes

<img width="435" height="367" alt="Pasted image 20250722084322" src="https://github.com/user-attachments/assets/fab212a0-120f-42df-95d6-581d21640878" />

## Static Analysis

### Detect it Easy

<img width="2324" height="256" alt="Pasted image 20250722084534" src="https://github.com/user-attachments/assets/a46fc522-7e61-437b-a497-a8095046b156" />

So it is .NET application with some custom obfuscation technique. 

##### Strings

There is evidence of some custom protection

```
VaultVM-Protect-776LGF6950
...
CrackMarcuza-Protect-DB89GFLG42
...
VaultVM-Protect-H1HHB6L197
```

There are lot of similar strings that are related to protection technique

Also there is string that is related to method with succeed message

```
You Win!
```

##### Entropy


<img width="1940" height="250" alt="Pasted image 20250722085303" src="https://github.com/user-attachments/assets/5fab6d01-f23a-49b8-80f9-16a7245c2578" />


High entropy confirms that there is obfuscation (or more exactly encryption/packing, which without any additional techniques will generate high-entropy because of crypto-algorithm nature)

##### Imports

There is only one import called as `mscoree.dll` . Nothing special, it is default import for .NET applications

### dnSpy

Opening this crackme in the dnSpy tool to see its C# (.NET) code. 

Overall methods, strings and other values are obfuscated. So it is harder to analyze the code, because we do not have readable names.

Since we are working with `Form` where we submit the key - there is a need to find `Form class`.
It is called `CrackMarcuza-Protect-9DD71ADEL2`.
There is a interesting method:

```csharp
bool flag = 
CrackMarcuza-Protect-9DD71ADEL2.CrackMarcuza-Protect-224C999FHE (
	this.CrackMarcuza-Protect-2E9E89G659.Text,
	CrackMarcuza-Protect-0L69ACE66B.CrackMarcuza-Protect-4G3C3EA4G0(
		CrackMarcuza-Protect-0L69ACE66B.VaultVM-Protect-HEA399LELD, 
		CrackMarcuza-Protect-0L69ACE66B.VaultVM-Protect-DC9G166B72
	)
);
```
Little bit  further there is condition
```csharp
if (flag){...}
```

The goal is to discover the flag. Placed the breakpoint on those statements and run debugger


# Dynamic Analysis

App opens the form and now it is time to enter the key. F.e. `123456789`.

Then I stepped into the method `4G3C3EA4G0`. It builds the string and returns it. 

```csharp
public static string CrackMarcuza-Protect 4G3C3EA4G0(string A_0, int A_1) {
	if (Assembly.GetExecutingAssembly().FullName == Assembly.GetCallingAssembly().FullName){

	StringBuilder stringBuilder = new StringBuilder();

	foreach (char c in A_0) {
		stringBuilder.Append((char)((int)((ulong)((ushort)((short)c))) ^ A_1));
	}
	return stringBuilder.ToString();
	}        
	return null;    
}
``` 

**Note:** `Assembly.GetExecutingAssembly().FullName == Assembly.GetCallingAssembly().FullName` is like simplest anti-tampering protection. But since we do not patch anything - there is no problem

It builds the string and XORes it with some int. By looking into `locals` we will see both arguments of this method

<img width="1473" height="66" alt="Pasted image 20250722100326" src="https://github.com/user-attachments/assets/18906bd4-6890-442b-b683-5afd9d29937d" />

so this string is xored with `17`

If we do this we will get another string:
`k2tes|Etgem`

I tried to put it as a key, but the `flag` is still `false`, so let's step into another method right after `4G3C3EA4G0`

```csharp
public static bool CrackMarcuza-Protect-224C999FHE (string A_0, string A_1){
	return A_0 == A_1;
}
```

`224C999FHE` just checks two strings. `Locals`:

<img width="1775" height="74" alt="Pasted image 20250722101512" src="https://github.com/user-attachments/assets/3c947b74-a0e4-4ebf-b822-40bdc593d330" />

Second value is the right key!

<img width="499" height="364" alt="Pasted image 20250722101203" src="https://github.com/user-attachments/assets/491f90e6-e254-46bb-afe2-d375cbf364ef" />

