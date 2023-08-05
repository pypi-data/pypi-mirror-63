# pwnedpasswds

A python wrapper for the [Pwned Passwords](https://haveibeenpwned.com/Passwords) API.


## Usage

You can either use pwnedpasswds in your python code or as a command line utility.

### Inside python

```python
>>> from pwnedpasswds import check_passwd
>>> count = check_passwd("Password1")
>>> count
116789
```

### Inside the commandline

You can supply passwords to pwnedpasswds as a command line argument, or thorugh stdin.


```bash
$ pwnedpasswds correcthorsebatterystaple
120
```

```bash
$ echo "linux4life" | pwnedpasswds
44
```

```bash
$ cat passwds.txt
troyhunt
p455w0rd
14m501337

$ cat passwds.txt | pwnedpasswds
11
15611
14
```

