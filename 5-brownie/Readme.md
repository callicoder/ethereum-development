# Brownie

**Add account**

```bash
brownie accounts new metamask-kovan
Brownie v1.16.4 - Python development framework for Ethereum

Enter the private key you wish to add: 0xb72a8909b7e7d95434dda39cf30dbe0dcdbb13229adaab0a3c2175353442392c
Enter the password to encrypt this account with:
SUCCESS: A new account '0x4ae110382de86cfC3ac59c06856DE9CBFB096bba' has been generated with the id 'metamask-kovan'
```

**List accounts**

```bash
brownie accounts list
Brownie v1.16.4 - Python development framework for Ethereum

Found 1 account:
 └─metamask-kovan: 0x4ae110382de86cfC3ac59c06856DE9CBFB096bba
```

**Test**

```bash
brownie test
```

```bash
brownie test -k test_update_storage
```

```bash
brownie test --pdb # Debugger
```

```bash
brownie test -s # Show all print lines and detailed logs
```

**Networks**

```bash
brownie networks list
```

```bash
brownie run scripts/deploy.py --network kovan
```

**Console**

```bash
brownie console
```